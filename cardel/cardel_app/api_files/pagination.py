from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class ReviewListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'pa'
    page_size_query_param = 'record'
    max_page_size = 2
    last_page_strings = 'last'

class ReviewListOffSetPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 3
    offset_query_description = 'start'
    limit_query_param = 'limitss'

class ReviewListCursorPagination(CursorPaginationPagination):
    page_size = 3
    ordering = '-rating'