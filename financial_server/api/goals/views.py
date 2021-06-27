from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import response
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.response import ErrorResponse
from financial_server.api.views import SessionAPIView
from financial_server.apps.financial_goals.models import FinancialGoal
from financial_server.core.serializers import serialize_financial_goals

from .forms import AddSavingsGoal, AddSavingGoalsTransaction


class Sync(SessionAPIView):

    def get(self, request: Request) -> Response:
        import pdb; pdb.set_trace()
        response = {
            'goals': [serialize_financial_goals(goal)
                      for goal in request.user.financial_goals.all()]
        }

        return Response(response, status=status.HTTP_200_OK)


class Details(SessionAPIView):

    def get(self, request: Request, id: int) -> Response:
        goal = get_object_or_404(FinancialGoal, user=request.user, id=id)
        return Response(serialize_financial_goals(goal), status=status.HTTP_200_OK)


class AddSavings(SessionAPIView):
    
    def post(self, request: Request) -> Response:
        form = AddSavingsGoal(data=request.data, user=request.user)

        if form.is_valid():
            goal = form.save()
            return response(serialize_financial_goals(goal), status=status.HTTP_200_OK)

        return ErrorResponse(form=form)


class AddSavingsTransaction(SessionAPIView):

    def post(self, request: Request) -> Response:
        form = AddSavingGoalsTransaction(data=request.data)

        if form.is_valid():
            form.save()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)

        return ErrorResponse(form=form)
