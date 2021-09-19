from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden

from financial_server.api.authentication import JSONSingleTokenAuthentication
from financial_server.api.response import ErrorResponse
from financial_server.api.utils import force_login
from financial_server.api.views import FinancialAPIView, SessionAPIView
from financial_server.apps.users.models import User
from financial_server.core.serializers import serialize_user

from .forms import AuthenticationForm, RegistrationForm, EditProfileForm


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


class Register(FinancialAPIView):

    def post(self, request: Request) -> Response:
        if request.data.get('token') != JSONSingleTokenAuthentication.token:
            return HttpResponseForbidden()

        form = RegistrationForm(data=request.data, files=request.FILES or None)

        if form.is_valid():
            form.save()

            response = {
                'message': 'Successfull registered'
            }
            return Response(response, status=status.HTTP_200_OK)

        return ErrorResponse(form=form)


class Logout(SessionAPIView):
    
    def post(self, request: Request) -> Response:
        logout(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ChangePassword(SessionAPIView):
    
    def post(self, request: Request) -> Response:
        form = PasswordChangeForm(data=request.data, user=request.user)
        if form.is_valid():
            user = form.save()
            return Response(serialize_user(user), status=status.HTTP_200_OK)  # type: ignore
        return ErrorResponse(form=form)


class EditProfile(SessionAPIView):

    def post(self, request: Request) -> Response:
        form = EditProfileForm(data=request.data, user=request.user)
        if form.is_valid():
            user = form.save(user=request.user)
            return Response(serialize_user(user), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
