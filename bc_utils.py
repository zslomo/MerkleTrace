import time

import yaml
from web3 import Web3, HTTPProvider

from qr_utils import _qr_decode_all_file, _qr_decode_one_file


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
    # item_key = _qr_decode_one_file(img_file)
    print('item_key is {}'.format(item_key))
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
    print('path is {}'.format(ret))
    ret_list = ret.split('+')
    _item_path = ret_list[1:-1]
    ret = _item_path[-1].split(';')[0]
    return ret


def _add_item(address, passwd, url, img_file, item_name):
    '''
    :param address: user address
    :param passwd: user passwd
    :param url: ethereum server url:port
    :param img_file: item QRcode
    :param item_name: item name
    :return: string
    '''
    item_key = _qr_decode_one_file(img_file)
    _item_name = item_name + '+'
    print('login ethereum server...')
    w3 = login(url=url)
    w3.personal.unlockAccount(address, passwd)
    print('geting contract...')
    contract_instance = get_contract(w3)
    print('sending trasaction...')
    tx_hash = contract_instance \
        .functions \
        .add_item(item_key, _item_name) \
        .transact({'from': address})
    print('start miner...')
    w3.eth.defaultAccount = address
    w3.miner.start(10)
    time.sleep(10)
    w3.miner.stop()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return '{}'.format(tx_receipt)


def _add_path(address, passwd, url, img_file, item_name, item_path):
    '''
    :param img_file: user img file
    :param passwd: user passwd
    :param url: ethereum server url:port
    :param item_name: item name
    :param img_file: item QRcode
    :param item_path: item apth
    :return: json status
    '''

    item_key = _qr_decode_one_file(img_file)
    _path = _get_path(url=url, item_key=item_key)
    if len(_path) == 0:
        print('this item is new, start to add it...')
        _add_item(address, passwd, url, img_file, item_name)
        print('down')
    else:
        last_time = _get_last_time(url, item_key)
        if time.strptime(last_time, '%Y-%m-%d  %H:%M:%S') > \
                time.strptime(item_path['time'], '%Y-%m-%d  %H:%M:%S'):
            return 'time before last submit time', 500

    _item_path = ';'.join([item_path['time'],
                          item_path['node_name'],
                          item_path['location']]) \
                 + '+'
    print('login ethereum server...')
    w3 = login(url=url)
    w3.personal.unlockAccount(address, passwd)
    print('geting contract...')
    contract_instance = get_contract(w3)
    print('check if item is new one...')


    print('sending trasaction...')
    tx_hash = contract_instance \
        .functions \
        .add_path(item_key, _item_path) \
        .transact({'from': address})
    print('start miner...')
    w3.eth.defaultAccount = address
    w3.miner.start(10)
    time.sleep(10)
    w3.miner.stop()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt


