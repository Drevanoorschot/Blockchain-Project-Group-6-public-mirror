import os
import subprocess
import time
from multiprocessing import Pool

from db import DbConnection
from download_contract import download_contract
from util import logger, ContractNotFoundException, InvalidEtherscanKeyException,\
    get_out_filename, filter_mythril_result


def analyze(contracts):
    amount_cores = min(int(os.getenv('MAX_CORES')), len(contracts))
    with Pool(amount_cores) as p:
        p.map(run, contracts)


def run(address):
    contract_name = None
    try:
        contract_name = download_contract(address)
    except InvalidEtherscanKeyException as e:
        logger.warning('Etherscan key was invalid (error %s), not downloading the contract '
                       'of address %s, but still analyzing it', e, address)
    except ContractNotFoundException:
        logger.error('Contract with address %s not found, quitting analysis.', address)
        _save_db(address, address, 0, b'', found=False)
        return
    _analyze_contract(address, contract_name)


def _analyze_contract(address, contract_name):
    out_filename = get_out_filename(address, contract_name)
    logger.info('Analyzing contract %s, output file is %s', contract_name or address, out_filename)

    result, duration = _execute_mythril(address)
    logger.info('Finished analyzing for contract %s, took %ss', contract_name or address, duration)

    failed = bool(result.stderr)
    if failed:
        logger.warning('Mythril failed on contract %s', address)
    _save_db(address, contract_name, duration, result, failed=failed)
    _save_file(out_filename, address, result)


def _execute_mythril(address):
    infura = f'--infura-id={os.getenv("INFURA_ID")}'
    t = os.getenv('TRANSACTION_COUNT')
    timeout = os.getenv('MAX_SYMBOLIC_TIME')

    start = time.time()
    return (subprocess.run(["myth", "analyze", "-a", address,
                            infura,
                            "-t", t,
                            "--execution-timeout", timeout],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE),
            time.time() - start)


def _save_db(address, contract_name, duration, result, found=True, failed=False):
    with DbConnection() as db:
        db.add_run(address, contract_name, duration,
                   filter_mythril_result(result) if found else '',
                   found, failed)


def _save_file(filename, address, result):
    with open(filename, 'wb') as f:
        s = f'Contract with address {address}\n'.encode('utf-8')
        f.write(s)
        f.write(result.stdout or result.stderr)
