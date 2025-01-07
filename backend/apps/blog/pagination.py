from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class PostPagination(PageNumberPagination):
    """
        Pagination class for handling paginated responses for posts.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': "Posts have been retrieved successfully",
            'timestamp': datetime.now().isoformat(),
            'data': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }
        })

