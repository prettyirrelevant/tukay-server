import logging

from eth_utils import to_text
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task
from web3.constants import ADDRESS_ZERO

from django.conf import settings
from django.core.cache import cache
from django.db import transaction

from services.evm.client import EVMClient

from apps.accounts.models import Account
from apps.airdrops.models import Airdrop, Claim
from apps.tokens.models import Token

logger = logging.getLogger(__name__)


@db_periodic_task(crontab(minute='*/3'))
@lock_task('constantly-fetch-airdrop-contract-events')
def fetch_airdrop_contract_events():
    client = EVMClient(rpc_endpoints=settings.RPC_ENDPOINTS)
    last_queried_block = cache.get('airdrop:last-queried-block') or settings.AIRDROP_CONTRACT_CREATION_BLOCK
    latest_block = client.get_latest_block()
    events = client.query_contract_events(
        name='Airdrop',
        to_block=latest_block,
        from_block=last_queried_block,
        address=settings.AIRDROP_CONTRACT_ADDRESS,
    )
    try:
        with transaction.atomic():
            for event in events:
                if event.event == 'NewAirdrop':
                    process_new_airdrop_event(event)
                elif event.event == 'AirdropDistributed':
                    process_airdrop_distributed_event(event)
                else:
                    logger.warning('Unknown event encountered: %s. Skipping...', event.event)
                    continue
    except Exception:
        logger.exception('Exception occurred while fetching airdrop contract events')
    else:
        cache.set('airdrop:last-queried-block', latest_block)


def process_new_airdrop_event(event):
    account, _ = Account.objects.get_or_create(
        address=event.args.owner,
        defaults={'address': event.args.owner},
    )
    token, _ = Token.objects.get_or_create(
        address=event.args.token,
        defaults=(
            {'address': event.args.token}
            if event.args.token != ADDRESS_ZERO
            else {
                'decimals': 18,
                'symbol': 'AVAX',
                'name': 'Avalanche',
                'is_complete': True,
                'address': event.args.token,
                'coingecko_id': 'avalanche-2',
            }
        ),
    )
    Airdrop.objects.create(
        token=token,
        owner=account,
        amount=event.args.amount,
        merkle_root=event.args.proof,
        name=to_text(event.args.name),
        expected_claims=event.args.claims,
        tx_reference=event.transactionHash,
        contract_index=event.args.identifier,
    )


def process_airdrop_distributed_event(event):
    account, _ = Account.objects.get_or_create(address=event.args.owner, defaults={'address': event.args.owner})
    airdrop = Airdrop.objects.get(contract_index=event.args.identifier)
    Claim.objects.create(
        account=account,
        airdrop=airdrop,
        amount=event.args.amount,
        tx_reference=event.transactionHash,
    )
