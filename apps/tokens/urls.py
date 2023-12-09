from django.urls import path

from .views import AllTokensAPIView

urlpatterns = [path('', AllTokensAPIView.as_view(), name='all-tokens')]
