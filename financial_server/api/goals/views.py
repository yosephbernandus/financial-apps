from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.views import FinancialAPIView

from financial_server.apps.financial_goals.models import FinancialGoal

from financial_server.core.serializers import serialize_financial_goals


class Sync(FinancialAPIView):

    def get(self, request: Request) -> Response:
        response = {
            'goals': [serialize_financial_goals(goal)
                      for goal in request.financial_goals.all()]
        }

        return Response(response, status=status.HTTP_200_OK)


class Details(FinancialAPIView):

    def get(self, request: Request, id: int) -> Response:
        goal = get_object_or_404(FinancialGoal, user=request.user, id=id)
        return Response(serialize_financial_goals(goal), status=status.HTTP_200_OK)
