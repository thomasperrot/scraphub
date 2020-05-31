import urllib
import urllib.parse
from datetime import datetime, timedelta
import re
from typing import Generator, Union

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from scraphub.items import Video, Tag


class VideoSpider(scrapy.Spider):
    name = "videos"
    start_urls = ["https://www.pornhub.com/video?page=1"]

    def parse(self, response: HtmlResponse) -> Generator[Union[Video, Request], None, None]:
        for video in response.xpath("//li[contains(@class, 'pcVideoListItem')]"):
            duration = video.xpath(".//var[contains(@class, 'duration')]/text()").get()
            hd = video.xpath(".//span[contains(@class, 'hd-thumbnail')]/text()").get() == "HD"
            video_data = video.xpath(".//div[contains(@class, 'thumbnail-info-wrapper')]")
            video_title = video_data.xpath("./span[contains(@class, 'title')]/a[@title]")
            title = video_title.xpath("@title").get()
            href = video_title.xpath("@href").get()
            user_row = video_data.xpath("./div[contains(@class, 'videoUploaderBlock')]")
            user = user_row.xpath("./div[contains(@class, 'usernameWrap')]/a/text()").get()
            tag_class = user_row.xpath("./span[contains(@class, 'main-sprite')]/@class").get()
            tag = None
            if tag_class:
                if "channel-icon" in tag_class:
                    tag = Tag.CHANNEL.value
                elif "own-video-thumbnail" in tag_class:
                    tag = Tag.AMATEUR.value
            details = video_data.xpath(".//div[contains(@class, 'videoDetailsBlock')]")
            views = details.xpath("./span[contains(@class, 'views')]/var/text()").get()
            likes = details.xpath("./div[contains(@class, 'rating-container')]/div[contains(@class, 'value')]/text()").get()
            published_at = video_data.xpath(".//var[contains(@class, 'added')]/text()").get()

            yield Video(
                title=title,
                href=href,
                user=user,
                published_at=self._parse_published_at(published_at),
                duration=self._parse_duration(duration),
                views=self._parse_views(views),
                likes=self._parse_likes(likes),
                tag=tag,
                hd=hd,
            )
        next_url = self._get_next_page(response)
        yield response.follow(next_url, callback=self.parse)

    @staticmethod
    def _parse_published_at(published_at: str) -> datetime:
        if match := re.match(r"(?P<duration>\d+) (?P<unit>\w+) ago", published_at):
            if match.group("unit") in ("minute", "minutes"):
                difference = timedelta(minutes=int(match.group("duration")))
            elif match.group("unit") in ("hour", "hours"):
                difference = timedelta(hours=int(match.group("duration")))
            elif match.group("unit") in ("day", "days"):
                difference = timedelta(days=int(match.group("duration")))
            elif match.group("unit") in ("week", "weeks"):
                difference = timedelta(weeks=int(match.group("duration")))
            elif match.group("unit") in ("month", "months"):
                difference = timedelta(days=30 * int(match.group("duration")))
            elif match.group("unit") in ("year", "years"):
                difference = timedelta(days=365 * int(match.group("duration")))
            else:
                raise Exception(published_at)
        elif published_at == "Yesterday":
            difference = timedelta(days=1)
        else:
            raise Exception(published_at)
        return datetime.now() - difference

    @staticmethod
    def _parse_duration(duration: str) -> int:
        minutes, seconds = duration.split(":")
        return int(minutes) * 60 + int(seconds)

    @staticmethod
    def _parse_views(views: str) -> int:
        if views.endswith("M"):
            factor = 1e6
            base = float(views[:-1])
        elif views.endswith("K"):
            factor = 1e3
            base = float(views[:-1])
        else:
            factor = 1
            base = float(views)
        return int(factor * base)

    @staticmethod
    def _parse_likes(likes: str) -> int:
        return int(likes[:-1])

    @staticmethod
    def _get_next_page(response: HtmlResponse) -> str:
        current_url = urllib.parse.urlparse(response.request.url)
        current_page = int(urllib.parse.parse_qs(current_url.query)["page"][0])
        next_page_query = urllib.parse.urlencode({"page": current_page + 1})
        next_url = current_url._replace(query=next_page_query)
        return urllib.parse.urlunparse(next_url)
