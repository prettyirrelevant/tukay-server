import json

from django.db.models import Q

from rest_framework import generics, status

from common.responses import error_response, success_response

from .models import Airdrop, Claim
from .serializers import AirdropSerializer, ClaimSerializer


class AllAirdropsAPIView(generics.ListAPIView):
    serializer_class = AirdropSerializer
    queryset = Airdrop.objects.get_queryset()

    def list(self, request, *args, **kwargs):  # noqa: A003
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)


class AirdropClaimsAPIView(generics.ListAPIView):
    serializer_class = ClaimSerializer
    queryset = Claim.objects.get_queryset()

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(Q(airdrop__contract_index=int(self.kwargs['id'])) | Q(airdrop__id=self.kwargs['id']))
        return qs

    def list(self, request, *args, **kwargs):  # noqa: A003
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)


class AirdropLeavesAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = AirdropSerializer
    queryset = Airdrop.objects.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(data=response.data, status_code=response.status_code)


class UploadAirdropLeavesAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            airdrop = Airdrop.objects.get(contract_index=self.kwargs['id'])
        except Airdrop.DoesNotExist:
            return error_response(message='Airdrop not found', status_code=status.HTTP_404_NOT_FOUND, errors=[])

        if len(airdrop.merkle_leaves) != 0:
            return success_response(
                status_code=status.HTTP_200_OK,
                data={'message': 'Merkle leaves for Airdrop updated successfully'},
            )

        json_file = request.FILES.get('file', None)
        if not json_file:
            return error_response(
                errors=[],
                message='json file missing from form data',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            airdrop.merkle_leaves = json.loads(json_file.read())
            airdrop.save(['merkle_leaves'])
        except Exception as e:  # noqa: BLE001
            return error_response(errors=[], message=str(e), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return success_response(
            status_code=status.HTTP_200_OK,
            data={'message': 'Merkle leaves for Airdrop updated successfully'},
        )
