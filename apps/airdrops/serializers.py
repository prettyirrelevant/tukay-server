from typing import Literal

from eth_utils import to_checksum_address

from rest_framework import serializers

from apps.accounts.serializers import AccountSerializer
from apps.airdrops.models import Airdrop, Claim
from apps.tokens.serializers import TokenSerializer


class AirdropSerializer(serializers.ModelSerializer):
    token = TokenSerializer(read_only=True)
    owner = AccountSerializer(read_only=True)
    claim_status = serializers.SerializerMethodField()
    actual_claims = serializers.SerializerMethodField()

    def get_actual_claims(self, obj):
        return obj.claimed_airdrops.count()

    def get_claim_status(self, obj) -> Literal['claimable', 'claimed', 'invalid']:
        addr = self.context['request'].query_params.get('address', None)
        if not addr:
            return 'claimable'

        checksum_addr = to_checksum_address(addr)
        if obj.claimed_airdrops.filter(account__address=checksum_addr).exists():
            return 'claimed'

        if checksum_addr in obj.merkle_leaves:
            return 'claimable'

        return 'invalid'

    class Meta:
        model = Airdrop
        fields = (
            'id',
            'name',
            'token',
            'owner',
            'amount',
            'created_at',
            'updated_at',
            'merkle_root',
            'tx_reference',
            'claim_status,' 'actual_claims',
            'contract_index',
            'expected_claims',
        )


class ClaimSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Claim
        fields = ('id', 'account', 'amount', 'tx_reference', 'created_at', 'updated_at')
