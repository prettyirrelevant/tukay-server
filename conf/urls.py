"""
URL configuration for tukay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from common import views

urlpatterns = [
    path('', views.ping_view, name='ping-endpoint'),
    path('api/airdrops/', include('apps.airdrops.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/giveaways/', include('apps.giveaways.urls')),
    path('api/crowdfunds/', include('apps.crowdfunds.urls')),
    path('docs', views.schema_view.with_ui(), name='api-schema'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'common.views.handler_400'

handler404 = 'common.views.handler_404'

handler500 = 'common.views.handler_500'
