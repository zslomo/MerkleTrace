import hashlib
import math
import time
from queue import Queue

from utils.bc_utils import _get_first_time


class MerkleTree():
    '''compute Merkle Root and verify item
    first, sort item QRcode by first commit time
    second, use the list element fill the leaf list to the power of 2 one by one
    third, compute Merkle Root
    '''

    def compute(self, _leaf_list, url):
        '''compute the Merkle Root
        :param _leaf_list: item QRcode list
        :param url: ethereum server url:port
        :return: string Merkle Root
        '''
        leaf_list = []
        # get first commit time
        for leaf in _leaf_list:
            first_time = _get_first_time(url=url,item_key=leaf)
            first_time = time.strptime(first_time, '%Y-%m-%d  %H:%M:%S')
            tmp = [first_time,leaf]
            leaf_list.append(tmp)
        # sort
        leaf_list.sort(key=lambda x:x[0])
        leaf_list = [row[1] for row in leaf_list]

        #fill the list
        new_length = 1 << int(math.log(len(leaf_list), 2)) + 1
        leaf_queue = Queue()
        tmp_l = []
        for i in range(new_length):
            leaf_queue.put(leaf_list[i % len(leaf_list)])
            tmp_l.append(leaf_list[i % len(leaf_list)])
        # compute Merkle Root

        while not leaf_queue.qsize() == 1:
            first = leaf_queue.get()
            second = leaf_queue.get()
            sha256 = hashlib.sha256()
            print((first + second))
            sha256.update((first + second).encode('utf-8'))
            res = sha256.hexdigest()
            print('sha----->{}'.format(res))
            leaf_queue.put(res)
        ret = leaf_queue.get()
        print('compute MerkleRoot should be {}'.format(ret))
        return ret

    def verify(self,_leaf_list, url, _MerkleRoot):
        '''verify item is real or not
        :param _leaf_list: item QRcode list
        :param url: ethereum server url:port
        :param _MerkleRoot: MerkleRoot to be verified
        :return: bool
        '''

        MerkleRoot = self.compute(_leaf_list,url)

        return MerkleRoot == _MerkleRoot