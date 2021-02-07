from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView


class FinancialAPIView(APIView):

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
