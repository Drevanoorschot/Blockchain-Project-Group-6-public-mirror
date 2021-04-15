from abc import ABC

from db.abstractdbconnection import AbstractDbConnection
from util import InvalidDbException, logger


class GenericDbConnection(AbstractDbConnection, ABC):
    def __init__(self):
        self._conn = None
        self._cursor = None
        self._existing_contracts = None

    def get_existing_contracts(self):
        self.cursor.execute('SELECT address FROM contract')
        return {result[0] for result in self.cursor.fetchall()}

    def get_amount_generic(self, index, sql):
        self.cursor.execute(sql, (index,))
        return self.cursor.fetchone()[0]

    def add_contracts_generic(self, contracts, block_no, index, sql):
        new_contracts = contracts.difference(self.existing_contracts)
        self._existing_contracts.update(new_contracts)

        logger.info("Adding %s contracts to the db belonging to timestamp index %s (block_no %s)"
                    % (len(new_contracts), index, block_no))

        values = [(contract, block_no, index) for contract in new_contracts]
        self.cursor.executemany(sql, values)

    def add_run_generic(self, address, contract_name, duration, result, found, failed, sql):
        self.cursor.execute(sql, (address, contract_name, duration, result, found, failed))

    def get_non_analyzed_contracts(self):
        self.cursor.execute('SELECT c.address '
                            'FROM contract c '
                            'LEFT JOIN run r ON r.contract_address = c.address '
                            'WHERE r.contract_address IS NULL')
        return {result[0] for result in self.cursor.fetchall()}

    @property
    def existing_contracts(self):
        if self._existing_contracts is None:
            self._existing_contracts = self.get_existing_contracts()
        return self._existing_contracts

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self._conn.cursor()
        return self._cursor

    def __enter__(self):
        raise InvalidDbException('Using generic DbConnection as a concrete interface, '
                                 'use SqliteConnection or PostgresConnection!')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()
