import yaml
from web3 import Web3, HTTPProvider


def login(url):
    '''login to send transaction
    param url: ethereum server url:port
    :return: HTTPProvider
    '''
    w3 = Web3(HTTPProvider(url))
    return w3


def get_contract(w3):
    '''get contract instance
    :param w3: w3 HTTPProvider
    :return: contract instance
    '''

    with open('./config.yaml', 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file)

    contract_instance = w3.eth.contract(
        address=yaml_data['contract']['address'],
        abi=yaml_data['contract']['abi'],
    )
    return contract_instance


def _get_path(url, item_key):
    '''get item path
    both get_path and get_first_time need this function
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :return: item path string
    '''
    print('login ethereum server...')
    w3 = login(url=url)
    print('geting contract...')
    contract_instance = get_contract(w3)
    print('sending trasaction...')
    ret = contract_instance \
        .functions \
        .query(item_key) \
        .call()
    return ret

def _get_first_time(url, item_key):
    '''get item first submit time
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :return: string first time
    '''
    ret = _get_path(url, item_key)
    ret_list = ret.split('+')
    _item_path = ret_list[1:-1]
    ret = _item_path[0].split(';')[0]
    return ret

def _get_last_time(url, item_key):
    '''get item last submit time
        :param url: ethereum server url:port
        :param item_key: item QRcode
        :return: string first time
        '''
    ret = _get_path(url, item_key)
    ret_list = ret.split('+')
    _item_path = ret_list[1:-1]
    ret = _item_path[-1].split(';')[0]
    return ret