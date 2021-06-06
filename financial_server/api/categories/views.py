from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.views import FinancialAPIView
from financial_server.apps.categories.models import Category
from financial_server.core.serializers import serialize_category


class Index(FinancialAPIView):

    def get(self, request: Request) -> Response:
        response = {
            'categories': [serialize_category(category)
                           for category in Category.objects.order_by('name')]
        }

        return Response(response, status=status.HTTP_200_OK)
