import json
import logging
import secrets
from functools import wraps
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

from eth_abi import abi
from eth_utils import event_abi_to_log_topic, function_abi_to_4byte_selector
from requests import RequestException
from web3 import HTTPProvider, Web3
from web3.exceptions import TransactionNotFound, Web3Exception
from web3.middleware.cache import construct_simple_cache_middleware
from web3.middleware.geth_poa import geth_poa_middleware
from web3.utils.caching import SimpleCache

logger = logging.getLogger(__name__)
DEFAULT_RPC_TIMEOUT = 20


def query_all_nodes():
    def wrapper(fn):
        @wraps(fn)
        def decorator(self, *args, **kwargs):
            for endpoint, w3 in self.connected_nodes.items():
                try:
                    response = fn(self, w3, *args, **kwargs)
                except (Web3Exception, RequestException, ValueError) as e:
                    if isinstance(e, TransactionNotFound):
                        raise

                    logger.exception(f'Failed to query {endpoint} for {fn.__name__!r} due to:')
                    continue

                return response

            raise RuntimeError(
                f'Unable to query {fn.__name__!r} with kwargs: {kwargs} after attempting {self.connected_nodes}',
            )

        return decorator

    return wrapper


class EVMClient:
    def __init__(self, rpc_endpoints, timeout=DEFAULT_RPC_TIMEOUT):
        self.timeout = timeout
        self.connected_nodes = {}
        self.abi_dir = Path(__file__).resolve().parent / 'abis'

        self._connect_to_nodes(rpc_endpoints)

    def get_web3(self):
        return secrets.choice(list(self.connected_nodes.values()))

    @query_all_nodes()
    def get_latest_block(self, w3: Web3):
        return w3.eth.block_number

    @query_all_nodes()
    def get_transaction_receipt(self, w3, tx_hash):
        return w3.eth.get_transaction_receipt(tx_hash)

    @query_all_nodes()
    def get_transaction(self, w3, tx_hash):
        return w3.eth.get_transaction(tx_hash)

    def get_contract(self, name: Literal['Airdrop', 'ERC20', 'Multicall'], address):
        abi_path = self.abi_dir / f'{name}.abi'
        with abi_path.open('r') as abi_file:
            abi_content = json.load(abi_file)

        w3 = self.get_web3()
        return w3.eth.contract(address=address, abi=abi_content)

    @query_all_nodes()
    def get_events(self, w3, topics, to_block, from_block, address):  # noqa: PLR0913 PLR0917
        filter_params = {
            'topics': [topics],
            'address': address,
            'toBlock': to_block,
            'fromBlock': from_block,
        }
        return w3.eth.get_logs(filter_params)

    def query_contract_events(self, name: Literal['Airdrop', 'ERC20'], address, from_block, to_block):
        contract = self.get_contract(name, address)
        log_topics_to_event_decoders = {event_abi_to_log_topic(e._get_event_abi()): e() for e in contract.events}
        events = self.get_events(
            address=address,
            to_block=to_block,
            from_block=from_block,
            topics=list(log_topics_to_event_decoders.keys()),
        )

        decoded_events = []
        for event in events:
            if event.topics[0] not in log_topics_to_event_decoders:
                continue

            decoder = log_topics_to_event_decoders[event.topics[0]]
            decoded_events.append(decoder.process_log(event))

        return decoded_events

    def get_erc20_contract_info(self, contract_address, multicall_address):
        erc20_contract = self.get_contract('ERC20', contract_address)
        multicall_contract = self.get_contract('Multicall', multicall_address)
        calls = [
            [contract_address, True, function_abi_to_4byte_selector(fn.abi)]
            for fn in [
                erc20_contract.functions.name(),
                erc20_contract.functions.symbol(),
                erc20_contract.functions.decimals(),
            ]
        ]
        result = multicall_contract.functions.aggregate3(calls).call()
        decoded_result = {'name': '', 'symbol': '', 'decimals': 18}
        for entry, fn_name in zip(result, decoded_result.keys()):
            if not entry[0]:
                continue

            if fn_name == 'decimals':
                decoded_result[fn_name] = abi.decode(['uint8'], entry[1])[0]
            else:
                decoded_result[fn_name] = abi.decode(['string'], entry[1])[0]

        return decoded_result

    def _connect_to_nodes(self, endpoints):
        for endpoint in endpoints:
            if endpoint in self.connected_nodes:
                logger.debug(f'{endpoint} is already connected. Skipping...')
                continue

            try:
                self._validate_endpoint(endpoint)
            except Exception:
                logger.exception(f'Unable to connect to {endpoint}. Skipping...')
                continue

            web3 = Web3(HTTPProvider(endpoint, request_kwargs={'timeout': self.timeout}))
            web3.middleware_onion.remove('validation')  # makes an additional rpc call
            web3.middleware_onion.remove('name_to_address')  # ens is not needed
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)

            simple_cache_middleware = construct_simple_cache_middleware(SimpleCache(1024))
            web3.middleware_onion.add(simple_cache_middleware)

            try:
                web3.is_connected()
            except RequestException:
                logger.warning(f'Failed to connect to rpc node with url {endpoint}. Skipping...')
                continue

            self.connected_nodes[endpoint] = web3

        if len(self.connected_nodes) == 0:
            raise ConnectionError(f'Unable to connect to any of the rpc nodes {endpoints}')

    @staticmethod
    def _validate_endpoint(endpoint):
        parsed_url = urlparse(endpoint)
        if parsed_url.scheme != 'https' or not parsed_url.netloc:
            raise ValueError('Provided URL is not secured or invalid')
