import os

from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from captcha.views import CaptchaStore
from captcha.views import captcha_image
from time import time, strftime, localtime
import base64
from uuid import uuid4

from .models import Blog
from .models import Tag
from .models import User
from .models import Type

from .modelserializer import BriefBlogModelSerializer
from .modelserializer import BlogModelSerializer
from .modelserializer import TagModelSerializer
from .modelserializer import TypeModelSerializer
from .modelserializer import UserModelSerializer

from utils.mypaginator import MyPaginator
from utils.token import create_token
from utils.es import ES
from middleware.auth import authenticate_user
import logging

logger = logging.getLogger()


# code 1000 请求成功
# code 1001 请求失败
# code 1002 token 即将过期
# code 1003 token失效
# code 1004 token认证失败
# code 1005 token非法
# code 1007 邮箱不存在或是密码不正确
# code 1008 验证码未通过
# code 1009 验证通过
# code 1010 验证码过期
# code 1011 图片上传成功
# code 1011 图片上传失败
# code 1012 图片删除成功
# code 1013 图片删除失败
# class TokenView(APIView):
#     def get(self, request):
#         ip = request.META.get("REMOTE_ADDR")
#         token = create_token({'ip': ip}, exp=30)
#         return Response({"code": 1000, 'data': token, "message": None})


class AllBlogListView(APIView):
    """获得全部的blog"""

    def get(self, request):
        email = request.query_params.get("email", "over_flowing@163.com")
        return Response(
            {"code": 1000, "data": Blog.objects.filter(user__email=email).count(), "message": None})

    def post(self, request):
        email = request.data.get("email", "over_flowing@163.com")
        query_set = Blog.objects.filter(user__email=email)
        paginator = MyPaginator()
        page_query_set = paginator.paginate_queryset(queryset=query_set, request=request, view=None)
        ser_obj = BriefBlogModelSerializer(page_query_set, many=True)
        return Response({"code": 1000, "data": ser_obj.data, "message": None})


class TypeView(APIView):

    def get(self, request):
        query_set = Type.objects.all()
        ser_obj = TypeModelSerializer(query_set, many=True)
        return Response({"code": 1000, "data": ser_obj.data, "message": None})

    @method_decorator(authenticate_user)
    def post(self, request):
        type_obj = request.data
        ser_obj = TypeModelSerializer(data=type_obj)
        if ser_obj.is_valid():
            ser_obj.save()
        return Response({"code": 1000, "data": ser_obj.data.get("id"), "message": None})

    @method_decorator(authenticate_user)
    def put(self, request):
        type_obj = Type.objects.filter(id=request.data.get('id')).first()
        ser_obj = TypeModelSerializer(instance=type_obj, data=request.data, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
        return Response({"code": 1000, "data": None, "message": None})

    @method_decorator(authenticate_user)
    def delete(self, request):
        try:
            type_id = request.query_params.get("t_id")
            Type.objects.get(id=type_id).delete()
        except Exception:
            return Response({"code": 1000, "data": None, "message": "此类型关联博客，请先修改相关博客的类型！"})
        return Response({"code": 1000, "data": None, "message": None})


class DetailedBlogView(APIView):

    def get(self, request):
        uid = request.query_params.get("id")
        obj = Blog.objects.get(id=uid)
        obj.view_times += 1
        obj.save()
        ser_obj = BlogModelSerializer(obj)
        # 未作：判断当前用户是否对此篇文章进行了 点赞
        return Response({"code": 1000, "data": ser_obj.data, "message": None})

    @method_decorator(authenticate_user)
    def post(self, request):
        blog = request.data
        ser_obj = BlogModelSerializer(data=blog)
        if ser_obj.is_valid():
            ser_obj.save()
            ES().create_blog(blog_id=ser_obj.data.get("id"),  # ser_obj.data.get("text")
                             new_blog={"title": ser_obj.data.get("title"), "text": "请输入博客内容~~~"})
            return Response({"code": 1000, "data": ser_obj.data.get("id"), "message": None})
        return Response({"code": 1001, "data": None, "message": "未成功创建"})

    @method_decorator(authenticate_user)
    def put(self, request, *args, **kwargs):
        updated_type = request.data.get("updated_type")
        blog_id = request.data.get("id")
        if updated_type == 0:
            blog = {'id': blog_id, 'title': request.data.get("title"),
                    'tag_list': request.data.get("tag_list"), 'article_type': request.data.get("article_type"),
                    "type": request.data.get("type")}
        elif updated_type == 1:
            blog = {'id': blog_id, "text": request.data.get("text")}

        query_set = Blog.objects.get(id=blog_id)
        ser_obj = BlogModelSerializer(instance=query_set, data=blog, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
            if updated_type == 1:
                ES().update_blog(blog_id=ser_obj.data.get("id"), blog_obj={
                    "title": ser_obj.data.get("title"),
                    "text": ser_obj.data.get("text")
                })
            return Response({"code": 1000, "data": None, "message": "修改博客成功"})
        return Response({"code": 1001, "data": None, "message": "未能成功修改博客"})

    @method_decorator(authenticate_user)
    def delete(self, request):
        """该删除 只是将文章类型变成 不公开的"""
        blog_id = request.query_params.get("id")
        blog = Blog.objects.get(id=int(blog_id))
        blog.article_type = 2
        blog.save()
        return Response({"code": 1000, "data": None, "message": None})


class TagListView(APIView):
    """获得标签列表"""

    def get(self, request):
        email = request.query_params.get("email", "over_flowing@163.com")
        query_set = Tag.objects.filter(user__email=email)
        ser_obj = TagModelSerializer(query_set, many=True)
        return Response({"code": 1000, "data": ser_obj.data, "message": None})


class TagView(APIView):
    """根据tag_id 拿到博客"""

    def get(self, request):
        t_id = request.query_params.get("t_id")
        bloglist = Blog.objects.filter(tag__id=t_id).all()
        ser_obj = BriefBlogModelSerializer(bloglist, many=True)
        return Response({"code": 1000, "data": ser_obj.data, "message": None})

    @method_decorator(authenticate_user)
    def post(self, request):
        tag = request.data
        ser_obj = TagModelSerializer(data=tag)
        if ser_obj.is_valid():
            ser_obj.save()
        return Response({"code": 1000, "data": ser_obj.data.get("id"), "message": None})

    @method_decorator(authenticate_user)
    def put(self, request):
        tag_obj = Tag.objects.filter(id=request.data.get('id')).first()
        ser_obj = TagModelSerializer(instance=tag_obj, data=request.data, partial=True)
        if ser_obj.is_valid():
            ser_obj.save()
        return Response({"code": 1000, "data": None, "message": None})

    @method_decorator(authenticate_user)
    def delete(self, request):
        t_id = request.query_params.get("id")
        try:
            Tag.objects.get(id=t_id).delete()
        except Exception:
            return Response({"code": 1000, "data": None, "message": "该标签关联博客，请先修改博客的标签！"})
        return Response({"code": 1000, "data": None, "message": None})


class SearchView(APIView):

    def get(self, request):
        word = request.query_params.get("word")
        es = ES()

        return Response({"code": "1000", "data": es.suggest(keyword=word), "message": None})

    def post(self, request):
        es = ES()
        keyword = request.data.get("keyword")
        position = request.data.get("position")
        result = es.search(keyword=keyword, current_position=position)
        return Response({"code": 1000, "data": result, "message": None})


class UserView(APIView):

    def get(self, request):
        email = request.query_params.get("email")
        query_set = User.objects.filter(email=email).first()
        ser_obj = UserModelSerializer(query_set)
        return Response({"code": 1000, "data": ser_obj.data, "message": None})

    def post(self, request):
        img_id = request.data.get("id")
        email = request.data.get("email")
        password = request.data.get("pwd")
        validate_code = request.data.get("validate_code")
        try:
            img_obj = CaptchaStore.objects.filter(id=img_id)[0]
        except IndexError:
            return Response({"code": 1007, "data": None, "message": "该验证码不存在！"})
        try:
            if validate_code.lower() != img_obj.response:
                return Response({"code": 1008, "data": None, "message": "验证码不正确！"})
            if time() > img_obj.expiration.timestamp():
                return Response({"code": 1010, "data": None, "message": "验证码过期！"})
            user = User.objects.filter(email=email)[0]
            if user.password != password:
                return Response({"code": 1007, "data": None, "message": "邮箱或密码不正确！"})
        except IndexError:
            return Response({"code": 1007, "data": None, "message": "邮箱或密码不正确！"})
        # 更新 登录时间
        user.save()
        token = create_token({'email': email}, exp=60)
        return Response({"code": 1009, 'data': {"token": token, "uid": user.id}, "message": None})

    @method_decorator(authenticate_user)
    def put(self, request):
        try:
            email = request.data.get("email")
            user = User.objects.filter(email=email)[0]
            ser_obj = UserModelSerializer(instance=user, data=request.data, partial=True)
            if ser_obj.is_valid():
                ser_obj.save()
            return Response({"code": 1000, "data": None, "message": None})
        except IndexError:
            return Response({"code": 1001, "data": None, "message": "更新用户信息失败"})


class AuthenticationView(APIView):
    """获取验证码"""

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        try:
            # 获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=hashkey).first().id
            image = captcha_image(request, hashkey)
            # 将图片转换为base64 字节类型的数据，需要解码成字符串
            image_base = base64.b64encode(image.content)
            data = {"id": id_, "image": image_base.decode("utf-8")}
            return Response({"code": 1000, "data": data, "message": None})
        except:
            return Response({"code": 1001, "data": None, "message": "请求失败"})


class ImgUpload(APIView):

    @method_decorator(authenticate_user)
    def post(self, request):
        uid = uuid4()
        c_time = strftime("%Y-%m-%d", localtime())
        img = request.data.get("img")
        img_type = img.content_type.split("/")[1]
        img_path = os.path.join("media", "blog", "img", c_time, "%s.%s" % (uid, img_type))
        if not os.path.isdir(os.path.dirname(img_path)):
            os.makedirs(os.path.dirname(img_path))
        with open(img_path, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)

        return Response({"code": 1011, "data": {"img_path": img_path.replace("\\", "/")}, "message": "上传成功！"})

    @method_decorator(authenticate_user)
    def delete(self, request):
        img_path = request.data.get("img_path")
        try:
            os.remove(img_path)
        except Exception as e:
            logger.error(e)
        return Response({"code": 1013, "data": None, "message": "图片删除成功"})
