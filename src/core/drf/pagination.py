"""
Custom pagination for django rest framework
"""
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination as OrignalPageNumberPagination


class PageNumberPagination(OrignalPageNumberPagination):
    """
    Wrap results with pagination data: current_page, number_of_pages, number_of_records
    """
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'current_page': self.page.number,
                'number_of_pages': self.page.paginator.num_pages,
                'number_of_records': self.page.paginator.count,
            },
            'results': data
        })

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'page_size': {
                    'type': 'integer',
                    'example': 10,
                },
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'total_pages': {
                    'type': 'integer',
                    'example': 13,
                },
                'current_page_number': {
                    'type': 'integer',
                    'example': 1,
                },
                'next': {
                    'type': 'integer',
                    'example': 1,
                },
                'results': schema,
            },
        }


