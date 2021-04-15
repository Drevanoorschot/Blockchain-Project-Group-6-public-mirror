import os

from etherscan import Etherscan

from util import ContractNotFoundException, InvalidEtherscanKeyException


def download_contract(address):
    try:
        eth = Etherscan(os.getenv('KEY'))
        filename, source = _get_source_code(eth, address)
    except AssertionError as e:
        raise InvalidEtherscanKeyException(e)

    _save_file(filename, source)
    return filename[:-4]


def _get_source_code(eth, address):
    result = eth.get_contract_source_code(address)[0]
    sourcecode = result['SourceCode']
    if sourcecode:
        filename = f"{result['ContractName']}__{address[-5:]}.sol"
        return filename, sourcecode
    else:
        raise ContractNotFoundException(address)


def _save_file(filename, source):
    with open(os.getenv('FILE_LOCATION') + filename, 'w') as f:
        f.write(source)
