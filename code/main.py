from dotenv import load_dotenv

from analyze_contracts import analyze
from db import DbConnection
from get_contracts import get_new_contracts
from util import logger

load_dotenv()

BLOCKS = {
    0: 1719240,
    1: 2178175,
    2: 4832455,
    3: 5534412,
}


def main():
    get_new_contracts(BLOCKS)
    analyze_contracts()


def analyze_contracts():
    with DbConnection() as db:
        contracts = db.get_non_analyzed_contracts()

    logger.info('Using contracts: %s', contracts)
    analyze(contracts)


if __name__ == '__main__':
    main()
