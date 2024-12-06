from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ExpressBigPageResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'pSize'
    page_query_param = 'page'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })


class ExpressStdPageResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'pSize'
    page_query_param = 'page'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
