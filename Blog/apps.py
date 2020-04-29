from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'Blog'

    def ready(self):
        from utils.es import ES
        ES.run_shell()
        es = ES()
        es.init_es_blog()
        es.init_es_suggestion()
        pass
