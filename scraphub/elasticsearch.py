from elasticsearch_dsl import Document, Text, Keyword, Integer, Boolean, Date
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])


class Video(Document):
    title = Text(analyzer="english", fields={"raw": Keyword()})
    user = Keyword()
    href = Keyword()
    published_at = Date()
    duration = Integer()
    views = Integer()
    likes = Integer()
    tag = Keyword()
    hd = Boolean()

    class Index:
        name = "videos"
        settings = {
            "number_of_shards": 4,
        }


Video.init()
