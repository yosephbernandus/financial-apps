from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.views import FinancialAPIView
from financial_server.core.serializers import serialize_financial_goals


class Sync(FinancialAPIView):

    def get(self, request: Request) -> Response:
        response = {
            'goals': [serialize_financial_goals(goal)
                      for goal in request.financial_goals.all()]
        }

        return Response(response, status=status.HTTP_200_OK)
