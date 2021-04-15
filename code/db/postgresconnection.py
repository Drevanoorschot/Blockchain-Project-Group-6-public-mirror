import os
import psycopg2

from db.dbconnection import GenericDbConnection


class PostgresConnection(GenericDbConnection):
    def add_run(self, address, contract_name, duration, result, found, failed):
        return self.add_run_generic(address, contract_name, duration, result, found, failed,
                                    sql='INSERT INTO run VALUES (%s, %s, %s, %s, %s, %s)')

    def add_contracts(self, contracts, block_no, index):
        return self.add_contracts_generic(contracts, block_no, index,
                                          sql='INSERT INTO contract VALUES (%s, %s, %s)')

    def get_amount(self, index):
        sql = 'SELECT COUNT(*) ' \
              'FROM contract c ' \
              'LEFT JOIN run r on c.address = r.contract_address ' \
              'WHERE contract_address IS NULL OR ' \
              '(timestamp = (%s) AND failed = false AND found = true)'
        return self.get_amount_generic(index, sql=sql)

    def __enter__(self):
        self._conn = psycopg2.connect(host=os.getenv('POSTGRESQL_HOST'),
                                      port=os.getenv('POSTGRESQL_PORT'),
                                      database=os.getenv('POSTGRESQL_DB'),
                                      user=os.getenv('POSTGRESQL_USER'),
                                      password=os.getenv('POSTGRESQL_PW'))
        return self
