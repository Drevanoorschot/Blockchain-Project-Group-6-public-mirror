import os
import sqlite3

from db.dbconnection import GenericDbConnection


class SqliteConnection(GenericDbConnection):
    def add_run(self, address, contract_name, duration, result, found, failed):
        return self.add_run_generic(address, contract_name, duration, result,
                                    1 if found else 0, 1 if failed else 0,
                                    sql='INSERT INTO run VALUES (?, ?, ?, ?, ?, ?)')

    def add_contracts(self, contracts, block_no, index):
        return self.add_contracts_generic(contracts, block_no, index,
                                          sql='INSERT INTO contract VALUES (?, ?, ?)')

    def get_amount(self, index):
        return self.get_amount_generic(index, sql='SELECT COUNT(*) FROM contract WHERE TIMESTAMP = (?)')

    def __enter__(self):
        self._conn = sqlite3.connect(os.getenv('DBNAME'))
        return self
