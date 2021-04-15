import os
import time

from etherscan import Etherscan

from db import DbConnection
from util import InvalidEtherscanKeyException, logger


def get_new_contracts(blocks):
    with DbConnection() as db:
        for index, block_no in blocks.items():
            eth = Etherscan(os.getenv('KEY'))
            logger.info("Searching for contracts starting with block %s, index %s", block_no, index)
            prev_call = time.time()

            while db.get_amount(index) < int(os.getenv('CONTRACTS_PER_TIMESTAMP')):
                time.sleep(time.time() - (prev_call - 0.2))  # Max 5 api calls per second
                contracts, block_no = get_contracts_from_block_range(eth, block_no)
                prev_call = time.time()
                logger.debug("For block_nos %s-%s (timestamp index %s), found %s contracts.",
                             block_no, block_no + 100, index, len(contracts))

                db.add_contracts(contracts, block_no, index)


def get_block_no_by_timestamp(eth, timestamp):
    try:
        return eth.get_block_number_by_timestamp(timestamp=timestamp, closest="after")
    except AssertionError as e:
        raise InvalidEtherscanKeyException(e)


def get_contracts_from_block_range(eth, start):
    end = start + 1000
    try:
        contracts = eth.get_internal_txs_by_block_range_paginated(start, end, 1,
                                                                  os.getenv('CONTRACTS_PER_TIMESTAMP'), sort='asc')
        return {contract['from'] for contract in contracts}, end
    except AssertionError as e:
        if '[] -- No transactions found' in e.args:
            logger.warning('No transactions in block range, skipping.')
            return set(), end
        raise InvalidEtherscanKeyException(e)
