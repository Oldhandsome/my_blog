# from django.core.signals import request_finished #请求到来前
# from django.core.signals import request_started # 请求到来后
# from django.core.signals import got_request_exception #请求异常
# from django.core import signals
#
# from django.db.models.signals import class_prepared
# from django.db.models.signals import pre_init, post_init
# from django.db.models.signals import pre_save, post_save
# from django.db.models.signals import pre_delete, post_delete
# from django.db.models.signals import pre_save, post_save
# from django.db.models.signals import pre_migrate, post_migrate
# from django.db.models.signals import m2m_changed
#
# from django.test.signals import setting_changed
# from django.test.signals import template_rendered
# from django.db.utils import ConnectionHandler

# connections = ConnectionHandler()
#
#
# def reset_queries(**kwargs):
#     path = kwargs.get("environ").get("PATH_INFO")
#     print(path)
#     # print(kwargs.get("environ"))
#     # for conn in connections.all():
#     #     print(conn.__dict__)
#     #     conn.queries_log.clear()
# signals.request_started.connect(reset_queries)

# def close_old_connections(**kwargs):
#     print("哇哈哈")
#     for conn in connections.all():
#         conn.close_if_unusable_or_obsolete()
#
#
# signals.request_started.connect(close_old_connections)
# signals.request_finished.connect(close_old_connections)

