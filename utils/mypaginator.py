from rest_framework import pagination
from collections import OrderedDict


class MyPaginator(pagination.LimitOffsetPagination):
    # 一页数据的数目的请求参数名称
    limit_query_param = 'l'
    # offset 指的是当前索引位置的名称
    offset_query_param = 'o'

    # 请求参数的一页数据最大数目
    max_limit = 10
    # 默认一页的数据条数
    default_limit = 2

