# coding=utf-8

# API
__author__ = "Bin Tan"
__date__ = " 2018.12.28"

import time

from flask import Flask, jsonify, request, redirect,url_for, render_template, make_response

from deploy_contract import Deploy
from bc_utils import login, get_contract, _get_path, _get_first_time, _get_last_time
from flask_cors import CORS
from MerkleTree import MerkleTree
app = Flask(__name__)
# cross origin
CORS(app, supports_credentials=True)



@app.route('/upload', methods=['POST','GET'])
def img_upload():
    img = request.files.get('file')
    img.save('./upload/{}'.format(img.filename))

    response = {'result': '{}'.format('success')}
    return jsonify(response), 200

@app.route('/add_path', methods=['POST'])
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
    last_time = _get_last_time(values['url'], values['item_key'])
    if time.strptime(last_time, '%Y-%m-%d  %H:%M:%S') > \
            time.strptime(values['item_path']['time'], '%Y-%m-%d  %H:%M:%S'):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)