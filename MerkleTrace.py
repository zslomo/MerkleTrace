# coding=utf-8

# API
__author__ = "Bin Tan"
__date__ = "2017.11.6"

import time

from flask import Flask, jsonify, request

from deploy_contract import Deploy
from utils import login, get_contract, _get_path, _get_first_time, _get_last_time
from flask_cors import CORS
from MerkleTree import MerkleTree
app = Flask(__name__)
# cross origin
CORS(app, supports_credentials=True)

@app.route('/deployContract', methods=['POST'])
def deploy_contract():
    '''deploy contract
    :param address: user address
    :param passwd: user passwd
    :param url: ethereum server url:port
    :return: json status
    '''

    values = request.get_json()
    required = ['address', 'passwd', 'url']
    if not all(k in values for k in required):
        return 'Missing values', 400
    contract_file = './MerkleTrace.sol'
    deploy_obj = Deploy(address=values['address'],
                        passwd=values['passwd'],
                        url=values['url'],
                        contract_file=contract_file)
    deploy_status = deploy_obj.deploy()
    response = {'result': deploy_status}
    return jsonify(response), 200


@app.route('/addItem', methods=['POST'])
def add_item():
    '''
    :param address: user address
    :param passwd: user passwd
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :param item_name: item name
    :return: json status
    '''

    values = request.get_json()
    required = ['address', 'passwd', 'url', 'item_key', 'item_name']
    if not all(k in values for k in required):
        return 'Missing values', 400
    _item_name = values['item_name'] + '+'
    print('login ethereum server...')
    w3 = login(url=values['url'])
    w3.personal.unlockAccount(values['address'], values['passwd'])
    print('geting contract...')
    contract_instance = get_contract(w3)
    print('sending trasaction...')
    tx_hash = contract_instance \
        .functions \
        .add_item(values['item_key'], _item_name) \
        .transact({'from': values['address']})
    print('start miner...')
    w3.eth.defaultAccount = values['address']
    w3.miner.start(10)
    time.sleep(10)
    w3.miner.stop()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    response = {'result': '{}'.format(tx_receipt)}
    return jsonify(response), 200


@app.route('/addPath', methods=['POST'])
def add_path():
    '''
    :param address: user address
    :param passwd: user passwd
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :param item_path: item apth
    :return: json status
    '''

    values = request.get_json()
    required = ['address', 'passwd', 'url', 'item_key', 'item_path']
    if not all(k in values for k in required):
        return 'Missing values', 400
    last_time = _get_last_time(values['url'],values['item_key'])
    if time.strptime(last_time,'%Y-%m-%d  %H:%M:%S') > \
        time.strptime(values['item_path']['time'],'%Y-%m-%d  %H:%M:%S'):
        return 'time before last submit time', 500

    _item_path = ';'.join([values['item_path']['time'],
                           values['item_path']['node_name'],
                           values['item_path']['location']]) \
                 + '+'
    print('login ethereum server...')
    w3 = login(url=values['url'])
    w3.personal.unlockAccount(values['address'], values['passwd'])
    print('geting contract...')
    contract_instance = get_contract(w3)
    print('sending trasaction...')
    tx_hash = contract_instance \
        .functions \
        .add_path(values['item_key'], _item_path) \
        .transact({'from': values['address']})
    print('start miner...')
    w3.eth.defaultAccount = values['address']
    w3.miner.start(10)
    time.sleep(10)
    w3.miner.stop()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    response = {'result': "{}".format(tx_receipt)}
    return jsonify(response), 200


@app.route('/getPath', methods=['POST'])
def get_path():
    '''
    get tiem path
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :return: json item path
    '''

    values = request.get_json()
    required = ['url', 'item_key']
    if not all(k in values for k in required):
        return 'Missing values', 400
    ret = _get_path(values['url'], values['item_key'])
    ret_list = ret.split('+')
    _item_name = ret_list[0]
    _item_path = ret_list[1:-1]
    item_path = []
    for path in _item_path:
        tmp = path.split(';')
        dic = {
            'time': tmp[0],
            'node_name': tmp[1],
            'location': tmp[2]
        }
        item_path.append(dic)
    ret = {
        'item_name': _item_name,
        'iterm_path': item_path
    }
    response = {'result': ret}
    return jsonify(response), 200


@app.route('/getFirstTime', methods=['POST'])
def get_first_time():
    '''get item first submit time, for merkle sort
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :return: json first time
    '''
    values = request.get_json()
    required = ['url', 'item_key']
    if not all(k in values for k in required):
        return 'Missing values', 400
    ret = _get_first_time(values['url'], values['item_key'])
    response = {'result': ret}
    return jsonify(response), 200

@app.route('/getLastTime', methods=['POST'])
def get_last_time():
    '''get item last submit time, for merkle sort
    :param url: ethereum server url:port
    :param item_key: item QRcode
    :return: json first time
    '''
    values = request.get_json()
    required = ['url', 'item_key']
    if not all(k in values for k in required):
        return 'Missing values', 400
    ret = _get_last_time(values['url'], values['item_key'])
    response = {'result': ret}
    return jsonify(response), 200

@app.route('/verify', methods=['POST'])
def verify():
    '''verify item is real or not
    :param url: ethereum server url:port
    :param leaf_list: item QRcode list
    :param MerkleRoot: MerkleRoot to be verified
    :return: bool
    '''
    values = request.get_json()
    required = ['url', 'leaf_list', 'MerkleRoot']
    if not all(k in values for k in required):
        return 'Missing values', 400
    merkleTree = MerkleTree()
    ret = merkleTree.verify(_leaf_list=values['leaf_list'],
                      url=values['leaf'],
                      _MerkleRoot=values['MerkleRoot'])
    response = {'result': ret}
    return jsonify(response), 200

@app.route('/compute', methods=['POST'])
def compute():
    '''compute the Merkle Root
    :param url: ethereum server url:port
    :param leaf_list: item QRcode list
    :return: string Merkle Root
    '''
    values = request.get_json()
    required = ['url', 'leaf_list']
    if not all(k in values for k in required):
        return 'Missing values', 400
    merkleTree = MerkleTree()
    ret = merkleTree.compute(_leaf_list=values['leaf_list'], url=values['leaf'])
    response = {'result': ret}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
