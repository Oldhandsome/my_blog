from django.contrib import admin
from django.urls import path

from .views import DetailedBlogView
from .views import AllBlogListView
from .views import TokenView
from .views import TagListView
from .views import TagView
from .views import SearchView
from .views import UserView
from .views import AuthenticationView
from .views import TypeView
from .views import ImgUpload

urlpatterns = [
    path('get_token/', TokenView.as_view()),
    path('blog/', DetailedBlogView.as_view()),
    path('bloglist/', AllBlogListView.as_view()),
    path('tags/', TagListView.as_view()),
    path('tag/', TagView.as_view()),
    path("type/", TypeView.as_view()),
    path("search/", SearchView.as_view()),
    path("user/", UserView.as_view()),
    path("get_validate_code/", AuthenticationView.as_view()),

    path("blog/img/", ImgUpload.as_view()),
]
