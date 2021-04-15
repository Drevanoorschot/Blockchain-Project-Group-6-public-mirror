from abc import ABC, abstractmethod


class AbstractDbConnection(ABC):
    @abstractmethod
    def get_existing_contracts(self):
        pass

    @abstractmethod
    def get_amount(self, index):
        pass

    @abstractmethod
    def add_contracts(self, contracts, block_no, index):
        pass

    @abstractmethod
    def add_run(self, address, contract_name, duration, result, found, failed):
        pass

    @abstractmethod
    def get_non_analyzed_contracts(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
