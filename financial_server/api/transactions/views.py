from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.response import ErrorResponse
from financial_server.api.views import SessionAPIView

from financial_server.core.serializers import serialize_transactions

class Sync(SessionAPIView):
    
    def get(self, request: Request) -> Response:
        response = {
            'transactions': [serialize_transactions(transaction)
                             for transaction in request.user.transactions.all()]
        }

        return Response(response, status=status.HTTP_200_OK)
