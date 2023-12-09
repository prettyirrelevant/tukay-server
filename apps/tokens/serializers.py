from rest_framework import serializers

from apps.tokens.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'id',
            'name',
            'symbol',
            'address',
            'decimals',
            'created_at',
            'updated_at',
            'is_complete',
            'coingecko_id',
        )
