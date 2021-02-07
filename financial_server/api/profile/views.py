from rest_framework import status
from rest_framework.response import Response

from financial_server.api.views import FinancialAPIView


class HelloWorldView(FinancialAPIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)
