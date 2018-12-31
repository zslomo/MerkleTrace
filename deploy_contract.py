#coding=utf-8
__author__ = "Bin Tan"
__date__ = "2017.11.6"

import time
import yaml
from web3 import Web3, HTTPProvider
from solc import compile_source

class Deploy():
    '''deploy contract
    Attributes:
        contract_file: contract file dist path
        address: user address
        passwd: user passwd
        url: ethereum server url:port
    Args:
        login: login to send transaction for contract deploying
        deploy: deploy contract, In this method we will modify the
                yaml file, write the address and abi of contract
    '''
    def __init__(self, address, passwd, url, contract_file):
        self.contract_file = contract_file
        self.address = address
        self.passwd = passwd
        self.url = url
    def login(self):
        '''login to send transaction for contract deploying
        :return: HTTPProvider
        '''
        w3 = Web3(HTTPProvider(self.url))
        return w3
    def deploy(self):
        '''deploy contract
        In this method we will modify theyaml file, write the address and abi of contract
        :return: bool
        '''
        try:
            print('login ethereum...')
            w3 = self.login()
            print('read contract file...')
            with open(self.contract_file, 'r') as sol_file:
                contract_source_code = sol_file.read()
            print('compile contract...')
            compiled_sol = compile_source(contract_source_code)  # Compiled source code
            contract_interface = compiled_sol['<stdin>:MerkleTrace']
            w3.eth.defaultAccount = self.address
            w3.personal.unlockAccount(self.address, 'user1')
            contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
            # Get transaction hash from deployed contract
            print('deploy contract...')
            tx_hash = contract.constructor().transact()
            print('transaction hash is {}'.format(tx_hash.hex()))
            #mining
            print('start miner...')
            w3.miner.start(1)
            time.sleep(10)
            w3.miner.stop()
            print('writing contract config...')
            contract_tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            contractAddress = contract_tx_receipt.contractAddress
            with open('./config.yaml','r') as yaml_file:
                yaml_data = yaml.load(yaml_file)
            yaml_data['contract']['address'] = contractAddress
            yaml_data['contract']['abi'] = contract_interface['abi']
            with open('./config.yaml', 'w') as yaml_file:
                yaml.dump(yaml_data,yaml_file)
            return 'contract address is {}'.format(contractAddress)
        except Exception as e:
            return 'get Exception {}'.format(str(e))



