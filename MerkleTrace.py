# coding=utf-8

# API
from query_utils import _verify, _compute

__author__ = "Bin Tan"
__date__ = " 2018.12.28"
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import qrcode
from io import BytesIO
from bc_utils import _get_path, _get_first_time, \
    _get_last_time, _add_path, _add_item
from deploy_contract import Deploy
from qr_utils import _qr_decode_one_file, _qr_decode_all_file
app = Flask(__name__)
# cross origin
CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')

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
    :param img_file: item QRcode
    :param item_name: item name
    :return: json status
    '''

    values = request.get_json()
    required = ['address', 'passwd', 'url', 'img_file', 'item_name']
    if not all(k in values for k in required):
        return 'Missing values', 400
    tx_receipt = _add_item(address=values['address'],
                           passwd=values['passwd'],
                           url=values['url'],
                           img_file=values['img_file'],
                           item_name=values['item_name'])
    response = {'result': '{}'.format(tx_receipt)}
    return jsonify(response), 200


@app.route('/addPath', methods=['POST'])
def add_path():
    '''
    :paramimg_file: user img file
    :param passwd: user passwd
    :param url: ethereum server url:port
    :param img_file: item QRcode
    :param item_path: item apth
    :return: json status
    '''
    values = request.get_json()
    required = ['address', 'passwd', 'url', 'img_file', 'item_name', 'item_path']
    if not all(k in values for k in required):
        return 'Missing values', 400
    tx_receipt = _add_path(address=values['address'],
                           passwd=values['passwd'],
                           url=values['url'],
                           img_file=values['img_file'],
                           item_name=values['item_name'],
                           item_path=values['item_path'])
    response = {'result': "{}".format(tx_receipt)}
    return jsonify(response), 200


@app.route('/getPath', methods=['POST'])
def get_path():
    '''
    get tiem path
    :param url: ethereum server url:port
    :param img_file: item QRcode
    :return: json item path
    '''

    values = request.get_json()
    required = ['url', 'img_file']
    if not all(k in values for k in required):
        return 'Missing values', 400
    item_key = _qr_decode_one_file(values['img_file'])
    ret = _get_path(values['url'], item_key)
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
        'item_path': item_path
    }
    print(ret)
    response = {'result': ret}
    return jsonify(response), 200


@app.route('/getFirstTime', methods=['POST'])
def get_first_time():
    '''get item first submit time, for merkle sort
    :param url: ethereum server url:port
    :param img_file: item QRcode
    :return: json first time
    '''
    values = request.get_json()
    required = ['url', 'img_file']
    if not all(k in values for k in required):
        return 'Missing values', 400
    item_key = _qr_decode_one_file(values['img_file'])
    ret = _get_first_time(values['url'], item_key)
    response = {'result': ret}
    return jsonify(response), 200


@app.route('/getLastTime', methods=['POST'])
def get_last_time():
    '''get item last submit time, for merkle sort
    :param url: ethereum server url:port
    :param img_file: item img file
    :return: json first time
    '''
    values = request.get_json()
    required = ['url', 'img_file']
    if not all(k in values for k in required):
        return 'Missing values', 400
    item_key = _qr_decode_one_file(values['img_file'])
    ret = _get_last_time(values['url'], item_key)
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
    required = ['url', 'merkle_root_img']
    if not all(k in values for k in required):
        return 'Missing values', 400
    ret = _verify(url=values['url'], merkle_root_img=values['merkle_root_img'])
    response = {'result': ret}
    print(response)
    return jsonify(response), 200


@app.route('/compute', methods=['POST'])
def compute():
    '''compute the Merkle Root
    :param url: ethereum server url:port
    :param leaf_list: item QRcode list
    :return: string Merkle Root
    '''
    values = request.get_json()
    required = ['url']
    if not all(k in values for k in required):
        return 'Missing values', 400
    ret = _compute(values['url'])
    byte_io = BytesIO()
    qrcode.make(ret).save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

@app.route('/leaf_upload', methods=['POST','GET'])
def leaf_img_upload():
    '''upload root
    upload to './upload/'
    :return: success
    '''
    img = request.files.get('file')
    img.save('./upload/{}'.format(img.filename))

    response = {'result': '{}'.format('success')}
    return jsonify(response), 200

@app.route('/root_upload', methods=['POST','GET'])
def root_img_upload():
    '''upload leaf
    upload to './upload/root/'
    :return: success
    '''
    img = request.files.get('file')
    img.save('./upload/root/{}'.format(img.filename))

    response = {'result': '{}'.format('success')}
    return jsonify(response), 200
@app.route('/delete',methods=['GET'])
def delete_img():
    list = os.walk('./upload')
    for img_dir in list:
        for img in img_dir[2]:
            print('remove {}'.format(os.path.join(img_dir[0], img)))
            os.remove(os.path.join(img_dir[0], img))
    response = {'result': '{}'.format('success')}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
