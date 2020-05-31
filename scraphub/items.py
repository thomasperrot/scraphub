import enum

import scrapy


class Tag(enum.Enum):
    AMATEUR = "AMATEUR"
    CHANNEL = "CHANNEL"


class Video(scrapy.Item):
    title = scrapy.Field()
    user = scrapy.Field()
    href = scrapy.Field()
    published_at = scrapy.Field()
    duration = scrapy.Field()
    views = scrapy.Field()
    likes = scrapy.Field()
    tag = scrapy.Field()
    hd = scrapy.Field()
