from django.urls import path

from .views import AirdropClaimsAPIView, AirdropLeavesAPIView, AllAirdropsAPIView, UploadAirdropLeavesAPIView

urlpatterns = [
    path('', AllAirdropsAPIView.as_view(), name='all-airdrops'),
    path('<id>/leaves', AirdropLeavesAPIView.as_view(), name='airdrop-claims'),
    path('<id>/claims', AirdropClaimsAPIView.as_view(), name='airdrop-claims'),
    path('<id>/upload-leaves', UploadAirdropLeavesAPIView.as_view(), name='upload-airdrop-leaves'),
]
