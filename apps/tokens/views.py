from rest_framework.generics import ListAPIView

from common.responses import success_response

from .models import Token
from .serializers import TokenSerializer


class AllTokensAPIView(ListAPIView):
    serializer_class = TokenSerializer
    queryset = Token.objects.get_queryset()

    def list(self, request, *args, **kwargs):  # noqa: A003
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)
