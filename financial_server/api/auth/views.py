from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from financial_server.api.response import ErrorResponse
from financial_server.api.utils import force_login
from financial_server.api.views import FinancialAPIView
from financial_server.apps.users.models import User
from financial_server.core.serializers import serialize_user

from .forms import AuthenticationForm


class AuthLogin(FinancialAPIView):

    def post(self, request: Request) -> Response:
        form = AuthenticationForm(data=request.data)

        if form.is_valid():
            force_login(request, form.get_user())
            user: User = request.user

            if not request.session.session_key:
                request.session.create()

            response = {
                'session_key': request.session.session_key,
                'user': serialize_user(user)
            }

            return Response(response, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
