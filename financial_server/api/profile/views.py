from rest_framework import status
from rest_framework.response import Response

from financial_server.api.views import SessionAPIView


class HelloWorldView(SessionAPIView):

    def get(self, request):
        return Response(data={"hello": "hello world"}, status=status.HTTP_200_OK)
