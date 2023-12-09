from django.http import HttpRequest, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def handler_400(request, exception, *args, **kwargs):
    return JsonResponse(
        data={'message': 'Bad request', 'errors': None},
        status=status.HTTP_400_BAD_REQUEST,
    )


def handler_404(request, exception):
    return JsonResponse(data={'message': 'Not found', 'errors': None}, status=status.HTTP_404_NOT_FOUND)


def handler_500(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        data={
            'message': "We're sorry, but something went wrong on our end",
            'errors': None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@api_view()
def ping_view(request):
    return Response(status=status.HTTP_200_OK)
