from rest_framework import serializers
from Blog import models


class TypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = "__all__"


class TagModelSerializer(serializers.ModelSerializer):
    # user_name = serializers.SerializerMethodField(read_only=True)
    # def get_user_name(self,obj):
    #     return obj.user.username

    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'order', 'user']
        extra_kwargs = {
            'id': {'read_only': True},
            "user": {"write_only": True}
        }


class BriefBlogModelSerializer(serializers.ModelSerializer):
    """get the brief information of blog"""
    updated_time = serializers.DateTimeField(read_only=True)
    tag = TagModelSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.like_set.count()

    class Meta:
        model = models.Blog
        fields = ['id', 'title', "type", 'view_times', 'likes', 'updated_time', "article_type", 'tag']
        # 'view_times','likes','comments','img_url'
        read_only_fields = (
            'id', 'title', "type", 'view_times', 'likes', "article_type", "article_type", 'updated_time')
        # 'view_times','likes','comments'


class BlogModelSerializer(serializers.ModelSerializer):
    """get the detailed,add,update the blog"""
    tag = TagModelSerializer(many=True, read_only=True)

    def validate_tag_list(self, tag_list):
        if len(tag_list) == 0:
            raise serializers.ValidationError("请选择至少一个标签")
        return tag_list

    tag_list = serializers.ListField(write_only=True)

    type_text = serializers.SerializerMethodField(read_only=True)

    def get_type_text(self, obj):
        return obj.type.name

    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return obj.user.username

    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.like_set.count()

    comment_list = serializers.SerializerMethodField(read_only=True)

    def get_comment_list(self, obj):
        query_set = obj.comment_set.all()
        ser_obj = CommentModelSerializer(query_set, many=True)
        return ser_obj.data

    created_time = serializers.DateTimeField(read_only=True)

    updated_time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        tag_list = validated_data.get('tag_list')
        if tag_list is not None:
            del validated_data['tag_list']
        instance = super(BlogModelSerializer, self).create(validated_data=validated_data)
        if tag_list is not None:
            instance.tag.add(*tag_list)
        return instance

    def update(self, instance, validated_data):
        tag_list = validated_data.get('tag_list')
        if tag_list is not None:
            del validated_data['tag_list']
        instance = super(BlogModelSerializer, self).update(instance=instance, validated_data=validated_data)
        if tag_list is not None:
            instance.tag.set(tag_list)
        return instance

    class Meta:
        model = models.Blog
        exclude = []
        extra_kwargs = {
            'id': {'read_only': True},
            'created_time': {'read_only': True},
            "type": {"write_only": True},
            "user": {"write_only": True},
        }


class UserModelSerializer(serializers.ModelSerializer):
    sex_text = serializers.CharField(source="get_sex_display", read_only=True)
    last_land = serializers.DateTimeField(read_only=True)
    role_text = serializers.SerializerMethodField(read_only=True)

    def get_role_text(self, obj):
        return obj.role.level

    def update(self, instance, validated_data):
        instance = super(UserModelSerializer, self).update(instance=instance, validated_data=validated_data)
        return instance

    class Meta:
        model = models.User
        fields = ["id", "username", "password", "sex", "sex_text", "email", "last_land", "self_introduce",
                  "img_url", "role_text"]
        extra_kwargs = {
            'id': {'read_only': True},
            'sex': {'write_only': True},
            "email": {'read_only': True},
            "password": {"read_only": True},
        }


class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ["blog", "user"]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class CommentModelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = models.Comment
        fields = ['id', 'user', 'username', 'content', 'created_time', 'parent']
        # read_only_fields = ['created_time']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'write_only': True},
        }
