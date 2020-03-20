# 我的博客

始于2020年1月，经历过了2个半月，基本功能都算健全

- 首页

- 博客浏览页面
- 标签页面
- 博客搜索页面
- 后台管理页面

想做的（原本打算只有自己可以登录，其他人当成游客，但发现评论和点赞不知道要由什么做主键。）

- 评论功能
- 点赞功能

前端页面和数据的渲染由Vue.js编写，而后端的数据提供端由python的DRF框架完成

用到的组件由

- Django

- DRF

  - 提供了丰富的视图类，例如APIVIew，将原有的Request对象进行了封装，并且豁免了CSRF_TOKEN，

  - 提供了定义序列化器的类和方法，根据Django ORM提供的数据进行自动序列化或是反序列化。

  而我用了ModelSerializer将Django ORM提供的数据进行序列化，提供给前端；在表单传入之后，通过ModelSerializer将数据反序列化，并校验保存。

  - 认证模块

    结合JWT模块，对X-TOKEN和A-TOKEN进行验证

  - 权限模块

  - 限流模块

    该限流模块为手写，没有用rest_framework自带的，并且将该限流模块是放入中间件中的。

  - 分页模块

    自定义一个分页类，继承了pagination.LimitOffsetPagination,只要确定重写四个属性即可

    

- django-simple-captcha

  用于登录后台管理页面的生成验证码。在登录时，页面会像后端请求一个验证码。而后端的数据字段返回以下的数据结构

  ```
  {
  	id:id,
  	img:"",
  }
  # img是将产生的图片进行base64加密之后的字符串（需要将字节类型的字符串解码成UTF-8），将这个数据结构返回给前端。
  # 验证时，返回表单以及上面的id即可。
  ```

- elasticsearch

  用于操作elasticsearch，因此在启动项目前需要保证elasticsearch的开启。在第一次启动时，会将数据库中的blog的标题和正文加载进elasticsearch，除此之外还有dictionary.txt（用爬虫爬的柯金斯字典）数据完成以英文字母为开头的提示的生成（用来当做英文的提示，本来还想来本新华辞典的做中文提示的），因此第一次执行该项目可能启动会有点久。

- PyJWT

  用于生成json web token值的。第一个token值是在第一次进入首页时，前端js会自动请求一个token用于后端数据的普通访问。第二个token值是存储登录的邮箱的。

文件目录结构

```
——| Site
——|——| Blog # 应用
——|——|——| apps.py
——|——|——| models.py
——|——|——| modelserializer.py
——|——|——| urls.py
——|——|——| views.py
——|——| media # 用于存放头像等
——|——| middleware
——|——|——| auth.py
——|——|——| crossorigin.py
——|——|——| throttle.py
——|——| Site
——|——|——| settings.py # 配置文件
——|——| util
——|——|——| es.py # 结合ES与自己的文档搜索需求做的一个类，便于视图类调用
——|——|——| mypagination.py # 继承自LimitOffsetPagination，重写了四个属性，用作分页。
——|——|——| token.py # 结合PyJWT模块，创建json web token,用作验证
——|——| dictionary.txt # 用爬虫爬的柯金斯字典
```

