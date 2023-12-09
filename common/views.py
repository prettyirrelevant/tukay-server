from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view

from django.http import HttpRequest, JsonResponse

from rest_framework import permissions, status
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


class HttpAndHttpsOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):  # noqa: FBT002
        schema = super().get_schema(request, public)
        schema.schemes = ['http', 'https']
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title='Tukay Indexer API',
        default_version='v1',
        license=openapi.License(name='AGPLv3 License'),
        contact=openapi.Contact(email='support@tukayapp.vercel.app'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=HttpAndHttpsOpenAPISchemaGenerator,
)
