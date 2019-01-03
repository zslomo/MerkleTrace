from src.MerkleTree import MerkleTree
from utils.qr_utils import _qr_decode_all_file, _qr_decode_one_file


def _verify(url, merkle_root_img):
    '''verify item is real or not
    :param url: ethereum server url:port
    :param merkle_root_img: merkle root img file
    :return: bool
    '''

    leaf_list = _qr_decode_all_file()
    MerkleRoot = _qr_decode_one_file('root/{}'.format(merkle_root_img))
    merkleTree = MerkleTree()
    ret = merkleTree.verify(_leaf_list=leaf_list,
                            url=url,
                            _MerkleRoot=MerkleRoot)
    return ret

def _compute(url):
    '''compute the Merkle Root
    :param url: ethereum server url:port
    :return: string Merkle Root
    '''
    leaf_list = _qr_decode_all_file()
    merkleTree = MerkleTree()
    ret = merkleTree.compute(_leaf_list=leaf_list, url=url)
    return ret