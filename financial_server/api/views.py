from typing import Any, Tuple

from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, MultiPartParser, FormParser)
from rest_framework.views import APIView
from rest_framework.request import Request

from .authentication import (JSONSingleTokenAuthentication,
                             APISessionAuthentication)
from .exceptions import APIError

from .permissions import IsSecure


class FinancialAPIView(APIView):

    permission_classes: Tuple[Any, ...] = (IsSecure,)
    authentication_classes = (JSONSingleTokenAuthentication,)

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @csrf_exempt
    def dispatch(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        # Hit the method for API
        response = super().dispatch(request, *args, **kwargs)
        return response

    def handle_exception(self, exc: Exception) -> Response:
        """ Override the exception handler to handle APIError first
        """
        if isinstance(exc, APIError):
            return Response({'detail': exc.detail}, status=exc.status_code,
                            exception=True)
        return super(FinancialAPIView, self).handle_exception(exc)


class SessionAPIView(FinancialAPIView):

    authentication_classes = (JSONSingleTokenAuthentication,
                              APISessionAuthentication)  # type: ignore
