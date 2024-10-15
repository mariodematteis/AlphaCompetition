from ibapi.client import *
from ibapi.wrapper import *

from utils.settings import get_settings

from log.log import Logger

class InteractiveBrokersApiSingleton(type):
    _instance = None

    def __call__(self, *args, **kwds):
        if not self._instance:
            self._instance = super().__call__(*args, **kwds)
        
        return self._instance
    
class IBInterface(
    EClient,
    EWrapper,
    metaclass=InteractiveBrokersApiSingleton):
    def __init__(self,):
        EClient.__init__(self, self)
        self._account_settings = get_settings()
        self._logger = Logger('TWSAPI')
        self._logger.info('App launched.')

    def __contract_str__(self, 
                         contractDetails: ContractDetails) -> str:
        return 'Contract Details\n\n' \
            f'MarketName -> {contractDetails.marketName}'

    def execDetails(self, reqId, contract, execution):
        ...


    def contractDetails(self, 
                        reqId: int, 
                        contractDetails: ContractDetails):
        
        ...

    def __str__(self) -> str:
        return f'IP Address -> {self._account_settings.ipaddress}\n' \
        f'Account Username -> {self._account_settings.username}\n' \
        f'Account Client ID -> {self._account_settings.clientid}'
    
    def __repr__(self) -> str:
        ...
 
class App(IBInterface):
    def __init__(self, ):
        super().__init__()\
    