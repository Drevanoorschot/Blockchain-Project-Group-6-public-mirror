import os
import re


def get_out_filename(address, contract_name):
    root = os.getenv('FILE_LOCATION')
    return f'{root}{contract_name}.out' if contract_name is not None else f'{root}{address}.out'


def filter_mythril_result(result):
    pattern = r'SWC ID: (?P<id>\d+)\n'
    swc_ids = re.findall(pattern, result.stdout.decode('utf-8'))
    ordered_unique = sorted(set(swc_ids))
    return ','.join(ordered_unique)
