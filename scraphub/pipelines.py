from scrapy import Item

from scraphub.elasticsearch import Video


class ScraphubPipeline:
    def process_item(self, item: Item, _) -> Item:
        video = Video(meta={"id": item["href"].split("=")[-1]}, **item)
        video.save()
        return item
