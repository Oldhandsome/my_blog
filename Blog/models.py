from django.db import models

# Create your models here.
__all__ = ['Type', 'Blog', 'Like', 'Comment', 'Tag', 'Role', 'User']


class Type(models.Model):
    """table of detailed category"""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Blog(models.Model):
    """table of Blog"""
    title = models.CharField(max_length=100, verbose_name="标题")
    text = models.TextField(verbose_name="正文")
    type = models.ForeignKey(to="Type", verbose_name="文章的类别", on_delete=models.PROTECT)
    view_times = models.IntegerField(default=0, verbose_name="浏览人数")
    ARTICLE_TYPE = ((1, "公开"), (2, "私密"))
    article_type = models.IntegerField(choices=ARTICLE_TYPE, verbose_name="文章是否公开")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 该blog 所拥有的标签 应与标签表多对多
    tag = models.ManyToManyField(to="Tag")
    # 用户 应与用户表 构成外键关系 （1个用户可以拥有多篇blog）
    user = models.ForeignKey(to="User", on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Like(models.Model):
    """table of like"""
    blog = models.ForeignKey(to="Blog", on_delete=models.PROTECT)
    user = models.ForeignKey(to="User", on_delete=models.PROTECT)

    def __str__(self):
        return "%s-%s" % ("blog", "user")

    class Meta:
        unique_together = ("blog", "user")


class Comment(models.Model):
    """table of comments"""
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    # 与blog构成 多对1 的关系（1篇文章有多个评论）
    blog = models.ForeignKey(to="Blog", on_delete=models.PROTECT)
    # 该评论的父id
    parent = models.ForeignKey(to="self", on_delete=models.PROTECT, blank=True, null=True)
    # 与user表构成 多对1的关系 （1个用户可以有多个评论）
    user = models.ForeignKey(to="User", on_delete=models.PROTECT)

    def __str__(self):
        return self.content


class Tag(models.Model):
    """table of tag"""
    order = models.IntegerField()
    name = models.CharField(max_length=32, verbose_name="标签名称")
    # 不同的用户有不同的标签
    user = models.ForeignKey(to="User", on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Role(models.Model):
    """table of role"""
    level = models.CharField(max_length=32)

    def __str__(self):
        return self.level


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=255)
    SEX_CHOICE = ((0, "男"), (1, "女"))
    sex = models.IntegerField(choices=SEX_CHOICE)
    email = models.CharField(max_length=32, unique=True, db_index=True)
    last_land = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)
    self_introduce = models.TextField(default="这个人很懒，他什么也没留下~~~")
    img_url = models.ImageField(upload_to='user/%Y-%m', null=True)
    role = models.ForeignKey(to="Role", on_delete=models.PROTECT)

    def __str__(self):
        return "%s" % (self.username)
