# Create your tests here.
import base64
import os
import uuid

import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site.settings')
django.setup()
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from django.db.models import Count
from captcha.views import CaptchaStore
import time

from Blog.models import *
from Blog.modelserializer import TypeModelSerializer
from Blog.modelserializer import TagModelSerializer
from Blog.modelserializer import BriefBlogModelSerializer
from Blog.modelserializer import UserModelSerializer
from Blog.modelserializer import CommentModelSerializer
from Blog.modelserializer import LikeModelSerializer
from Blog.modelserializer import BlogModelSerializer
from Blog.models import Blog

# class TestType(TestCase):
#     def get_type(self):
#         query_set = Type.objects.all()
#         ser_obj = TypeModelSerializer(query_set, many=True)
#         print(ser_obj.data)
#
#     def add_type(self, type):
#         ser_obj = TypeModelSerializer(data=type)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#     def update_type(self, type):
#         type_obj = Type.objects.filter(id=type.get('id')).first()
#         ser_obj = TypeModelSerializer(instance=type_obj, data=type, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()


# if __name__ == '__main__':
#     # TestType().get_type()
#
#     # type = {
#     #     'category': 1,
#     #     'name': 'C++',
#     # }
#     # TestType().add_type(type)
#
#     type = {
#         'id': 7,
#         'category': 1,
#         'name': " Oracle"
#     }
#     TestType().update_type(type)

# class TestTag(TestCase):
#     def get_tag(self):
#         query_set = Tag.objects.all()
#         ser_obj = TagModelSerializer(query_set, many=True)
#         print(ser_obj.data)
#
#     def add_tag(self, tag):
#         ser_obj = TagModelSerializer(data=tag)
#         if ser_obj.is_valid():
#             ser_obj.save()
#         print(ser_obj.data)
#
#     def update_tag(self, tag):
#         print(tag)
#         tag_obj = Tag.objects.filter(id=tag.get('id')).first()
#         ser_obj = TagModelSerializer(instance=tag_obj, data=tag, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#
# #
# if __name__ == '__main__':
#     # TestTag().get_tag()
#
#     tag = {
#         'name': '心得体会',
#         'order': 8,
#         'user': 1
#     }
#     TestTag().add_tag(tag)
# tag = {
#     'id': 4,
#     'name': '标签4_1',
#     'order': 4,
# }
# # TestTag().update_tag(tag)
# print(Tag.objects.get(id=4).order)

# class TestBriefBlog(TestCase):
#     def get_blog(self):
#         query_set = Blog.objects.get(id=1)
#         Blog.objects.values('text')
#         # query_set = Blog.objects.all()
#         ser_obj = BriefBlogModelSerializer(query_set)
#         print(ser_obj.data)
#
# if __name__ == '__main__':
#     TestBriefBlog().get_blog()


# class TestUser(TestCase):
#     def get_user(self, id):
#         query_set = User.objects.get(id=id)
#         ser_obj = UserModelSerializer(query_set)
#         print(ser_obj.data)
#
#     def add_user(self, user):
#         ser_obj = UserModelSerializer(data=user)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#     def update_user(self, user, id):
#         user_obj = User.objects.get(id=id)
#         ser_obj = UserModelSerializer(instance=user_obj, data=user, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()
#             print(1)
#
#
# #
# if __name__ == '__main__':
#     # user = {
#     #     'username':'John',
#     #     'password':'123456',
#     #     'sex': 0,
#     #     'email':'123sfasfasfas45@163.com',
#     #     'role': 2,
#     # }
#     #     # TestUser().add_user(user)
#     user = {
#         "username": "Jacky1",
#         "email": "1234456789@163.com",
#         "img_url": "media/user/2020-02/header_2.jpg"
#     }
#     TestUser().update_user(user, 3)
#     TestUser().get_user(3)

#

#
# class TestComments(TestCase):
#     def get_comment(self):
#         query_set = Comment.objects.get(id=1)
#         ser_obj = CommentModelSerializer(query_set)
#         print(ser_obj.data)
#
#     def add_comment(self,comment):
#         ser_obj = CommentModelSerializer(data=comment)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#
#
# if __name__ == '__main__':
#     TestComments().get_comments()
#
#     # comment = {
#     #     'user': 1,
#     #     'content':'测试_1_2',
#     #     'blog':1,
#     #     'parent':2
#     # }
#     # TestComments().add_comment(comment)

# class TestLike(TestCase):
#     def get_like(self):
#         like = Like.objects.get(user=1,blog=1)
#         ser_obj = LikeModelSerializer(like)
#         print(ser_obj.data)
#     def add_like(self,like):
#         ser_obj = LikeModelSerializer(data=like)
#         if ser_obj.is_valid():
#             ser_obj.save()
#     def get_likelist(self):
#         query_set = Like.objects.filter(blog__article_type=1).values('blog').annotate(count=Count('blog')).order_by("-count")[0:5]
#         li = []
#         for i in query_set:
#             li.append(i.get('blog'))
#         query_set = Blog.objects.filter(id__in=li)
#         ser_obj = BriefBlogModelSerializer(query_set,many=True)
#         for i in ser_obj.data:
#             print(i)
#
# if __name__ == '__main__':
#     # TestLike().get_like()
#     #
#     # like = {
#     #     'user': 3,
#     #     'blog': 1,
#     # }
#     # TestLike().add_like(like)
#     TestLike().get_likelist()


# blog_text = """
# #### 二.高阶函数
#
# ##### 1.reduce
#
# reduce()函数也是Python内置的一个高阶函数。
# 传递的参数和map()函数类似分别是：一个函数function，一个list,第三个参数是可选参数-计算初值。
# # 但行为和 map()不同，reduce()传入的函数
# # 条件：f 必须接收两个参数，
# # reduce()的作用：将list中的前两个元素取出，后经过function函数，返回结果再加入list集合的头中；然后在取出list集合中的前两个元素，经过function函数，返回结果......并返回最终结果值。
#
# ```python
# from functools import reduce
# def f(x, y):
#     return x + y
# print(reduce(f, [1, 3, 5, 7, 9]))
# #reduce()还可以接收第3个可选参数，作为计算的初始值。
# print(reduce(f, [1, 3, 5, 7, 9],100))
# ```
#
# ##### 2.map函数
#
# map（function_name,list) 取出list中每个元素并经过函数function的处理并返回另一个元素加入list之中， 条件：function函数只有一个参数，最终map函数返回一个新的 list。
#
# ```python
# def format_name(s):
#     return s[0:1].upper()+s[1:] .lower()
# for value in map(format_name, ['adam', 'LISA', 'barT']):   		print(value)
# ```
#
# ##### 3.filter函数
#
#  filter()函数参数：一个函数的名字 function 和一个list，这个函数 f 的作用是对每个元素进行判断，返回 True或 False。 filter()根据判断结果自动过滤掉不符合条件的元素，返回由符合条件元素组成的新list。并不会改变元素
#
# ```python
# def is_odd(x):
#     return x % 2 == 1
# for odds in filter(is_odd,[1,2,3,4,5,6,7,8,9]):
#     print(odds)
# ```
# """
#
# class TestBlog(TestCase):
#     def getDetailBlog(self):
#         query_set = Blog.objects.get(id=1)
#         ser_obj = BlogModelSerializer(query_set)
#         print(ser_obj.data)
#
#     def add_blog(self, blog):
#         ser_obj = BlogModelSerializer(data=blog)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#     def update_blog(self, blog):
#         query_set = Blog.objects.get(id=blog.get('id'))
#         ser_obj = BlogModelSerializer(instance=query_set, data=blog, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#     def update_blog_attr(self, blog):
#         query_set = Blog.objects.get(id=blog.get('id'))
#         ser_obj = BlogModelSerializer(instance=query_set, data=blog, partial=True)
#         if ser_obj.is_valid():
#             ser_obj.save()
#
#     def getBlogList(self, t_id):
#         bloglist = Blog.objects.filter(tag__id=t_id).all();
#         ser_obj = BriefBlogModelSerializer(bloglist, many=True)
#         for i in ser_obj.data:
#             print(i)
#
#
if __name__ == '__main__':
    # TestBlog().getDetailBlog()
    # TestBlog().getBlogList(1);
    # blog = {
    #     "id": 10,
    #     "text": "1Django之CBV123456",
    # }
    # TestBlog().update_blog_attr(blog)
    # blog = Blog.objects.get(id=10)
    #
    # # print(blog.tag.all())
    # print("内容是", blog.text)
    #
    # blog = {
    #     'title': 'DRF之路由封装',
    #     'type': 1,
    #     'tag_list': [1, 2, 3],
    #     'article_type': 1,
    #     'text': "猜猜我是谁",
    #     'user': 1,
    #     'view_times': 0,
    # }
    # TestBlog().add_blog(blog)
    from datetime import datetime
    user = User.objects.get(id=1)
    user.password = "77058@cc"
    user.save()
# blog = {
#     'id': 8,
#     'tag_list': [1,2],
#     'type': 1,
#     'user': 1,
#     'title':'高阶函数的使用',
#     'text':blog_text,
#     'view_times':0,
#     'article_type':1,
# }
# TestBlog().update_blog(blog)


# if __name__ == '__main__':
#     uid = uuid.uuid4()
#     c_time = time.strftime("%Y-%m-%d", time.localtime())
#     img_type = "png"
#     from django.conf import settings
#
#     # img_path = +"/media/blog/img/%s/%s.%s" % (c_time, )
#     img_path = os.path.join(settings.BASE_DIR, "media", "blog", 'img', c_time)
#     if not os.path.isdir(img_path):
#         os.makedirs(img_path)
#     # print(os.path.join(img_path, "%s.%s" %(uid,img_type)))
#     with open(os.path.join(img_path, "%s.%s" % (uid, img_type)), "wb") as f:
#         f.write(base64.b64encode(img.encode("utf-8")))
    # with open(img_path, "wb") as f:
    #     f.write(base64.b64decode(img.encode()))

    # es = Elasticsearch()
    # print(es.ping())
    # print(es.indices.exists("blog"))
    # body = {
    #     "mappings": {
    #         "properties": {
    #             "title": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"},
    #             "text": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word"}
    #         }
    #     }
    # }
    # print(es.indices.create(index="blog", body=body))
    # print(es.indices.get_mapping(index="blog"))

    # blog_objs = (
    #     {
    #         '_index': "blog",
    #         "_id": blog.id,
    #         "_source": {
    #             "title": blog.title,
    #             "text": blog.text,
    #         }
    #     }
    #     for blog in Blog.objects.all()
    # )
    # helpers.bulk(es, blog_objs)

    # keyword = "python"
    # current_position = 0
    # body = {
    #     "size": 5,
    #     "from": current_position,
    #     "query": {
    #         "bool": {
    #             "should": [
    #                 {
    #                     "match": {
    #                         "text": keyword,
    #                     }
    #                 },
    #                 {
    #                     "match": {
    #                         "title": keyword,
    #                     }
    #                 }
    #             ]
    #         }
    #     },
    #     "highlight": {
    #         "pre_tags": '<b style="color:red;">',
    #         "post_tags": "</b>",
    #         "fields": {
    #             "title": {"number_of_fragments": 1, "no_match_size": 50},
    #             "text": {"number_of_fragments": 1, "no_match_size": 50}
    #         }
    #     }
    # }
    #
    # print(es.search(index="blog", body=body, filter_path=['hits.total', "hits.hits._id", "hits.hits.highlight"]))
    # print(es.get(index="blog", id=1))
    # print(es.indices.exists("blog"))

    # print(es.indices.delete(index="blog"))

    # import datetime
    #
    # if __name__ == '__main__':
    #     # img_obj = CaptchaStore.objects.filter(id="100")[0]
    #     print(time.time() - CaptchaStore.objects.filter(id="56")[0].expiration.timestamp() > 180)
    #     print(time.time() - CaptchaStore.objects.filter(id="56")[0].expiration.timestamp())
    #     now = datetime.datetime.now()
    #     print(now.timestamp())

    # blog_obj = {
    #     "title": "你好么",
    #     "text": "是的，我很好"
    # }
    # print(es.create(index="blog", id=99, body=blog_obj))
    # updated_blog = {
    #     "doc": {
    #         "title": "啊哈12345y5dasd123",
    #         "text": "你在干什么126das64312315"
    #     }
    # }
    # result = es.update(index="blog", id=99, body=updated_blog, filter_path=["_shards.successful"])
    # print(result['_shards']['successful'])
    # print(es.get(index="blog", id=99))
    # es.get(index="blog",id=99)
