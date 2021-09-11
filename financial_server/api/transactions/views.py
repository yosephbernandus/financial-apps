from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.response import ErrorResponse
from financial_server.api.views import SessionAPIView

from financial_server.core.serializers import serialize_transactions

from .forms import EditTransactionForm

class Sync(SessionAPIView):
    
    def get(self, request: Request) -> Response:
        response = {
            'transactions': [serialize_transactions(transaction)
                             for transaction in request.user.transactions.all()]
        }

        return Response(response, status=status.HTTP_200_OK)


class EditTransaction(SessionAPIView):
    
    def post(self, request: Request) -> Response:
        form = EditTransactionForm(data=request.data, user=request.user)

        if form.is_valid():
            transaction = form.save()
            return Response(serialize_transactions(transaction), status=status.HTTP_200_OK)

        return ErrorResponse(form=form)
