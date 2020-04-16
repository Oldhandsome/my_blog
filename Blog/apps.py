from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'Blog'

    def ready(self):
        from utils.es import ES
        ES().init_es_blog()
        ES().init_es_suggestion()
        pass
