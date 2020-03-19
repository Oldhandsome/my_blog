from elasticsearch import Elasticsearch
from Blog.models import Blog
from elasticsearch import helpers


class ES(object):
    es = Elasticsearch()

    def create_blog(self, blog_id, new_blog):
        self.es.create(index="blog", id=blog_id, body=new_blog)

    def update_blog(self, blog_id, blog_obj):
        updated_blog = {
            "doc": {
                "title": blog_obj.get("title"),
                "text": blog_obj.get("text"),
            }
        }
        result = self.es.update(index="blog", id=blog_id, body=updated_blog, filter_path=["_shards.successful"])
        return result['_shards']['successful']

    def search(self, keyword, current_position):
        body = {
            "from": current_position,
            "size": 7,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "title": keyword,
                            }
                        },
                        {
                            "match": {
                                "text": keyword,
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "pre_tags": '<u style="color:red;">',
                "post_tags": "</u>",
                "fields": {
                    "title": {"number_of_fragments": 1, "no_match_size": 50},
                    "text": {"number_of_fragments": 1, "no_match_size": 50}
                }
            }
        }
        return self.es.search(index="blog", body=body,
                              filter_path=['hits.total', "hits.hits._id", "hits.hits.highlight"])

    def suggest(self, keyword):
        body = {
            "suggest": {
                "my_suggestion": {
                    "text": keyword,
                    "completion": {
                        "field": "word",
                        "skip_duplicates": "true",
                        "size": 4
                    }
                }
            }
        }
        try:
            suggestion = \
                self.es.search(index="suggestion_db", body=body, filter_path=["suggest.my_suggestion.options.text"])[
                    'suggest']['my_suggestion']
        except Exception:
            suggestion = [{"options": []}]
        return suggestion

    def init_es_blog(self):
        if self.es.ping():
            if self.es.indices.exists("blog"):
                self.es.indices.delete(index="blog")
            body = {
                "mappings": {
                    "properties": {
                        "title": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},
                        "text": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"}
                    }
                }
            }
            self.es.indices.create(index="blog", body=body)
            blog_objs = (
                {
                    '_index': "blog",
                    "_id": blog.id,
                    "_source": {
                        "title": blog.title,
                        "text": blog.text,
                    }
                }
                for blog in Blog.objects.all()
            )
            helpers.bulk(self.es, blog_objs)
        else:
            raise Exception("ElasticSearch未能成功Ping通！")

    def init_es_suggestion(self):
        if self.es.ping():
            if self.es.indices.exists("suggestion_db"):
                self.es.indices.delete(index="suggestion_db")
            body = {
                "mappings": {
                    "properties": {
                        "word": {"type": "completion", "analyzer": "ik_smart", "search_analyzer": "ik_smart"},
                    }
                }
            }
            self.es.indices.create(index="suggestion_db", body=body)
            f = open("dictionary.txt", "r", encoding="utf-8")
            try:
                actions = ({
                    "_index": "suggestion_db",
                    "_type": "_doc",
                    "_source": {
                        "word": i.strip(),
                    }
                } for i in f.readlines())
                helpers.bulk(self.es, actions=actions)
            except Exception:
                raise Exception("英文建议未能成功初始化")
            finally:
                f.close()
        else:
            raise Exception("ElasticSearch未能成功PING通！")
