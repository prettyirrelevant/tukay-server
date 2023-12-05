import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from django.conf import settings

from services.evm.client import EVMClient

from apps.tokens.models import Token

logger = logging.getLogger(__name__)


@db_periodic_task(crontab(minute='*/2'))
@lock_task('populate-tokens-info')
def populate_tokens_information():
    client = EVMClient(rpc_endpoints=settings.RPC_ENDPOINTS)
    for token in Token.objects.filter(is_complete=False):
        try:
            token_info = client.get_erc20_contract_info(
                contract_address=token.address,
                multicall_address=settings.MULTICALL_CONTRACT_ADDRESS,
            )
        except:  # noqa: E722
            logger.exception('Unable to get ERC20 information for token %s', token.address)
            continue

        token.is_complete = True
        token.symbol = token['symbol']
        token.name = token_info['name']
        token.decimals = token['decimals']
        token.save()
