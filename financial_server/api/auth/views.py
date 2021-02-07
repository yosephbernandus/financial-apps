from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer

from financial_server.api.views import FinancialAPIView


class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(FinancialAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
