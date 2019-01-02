import zxing
import os


def _qr_decode_one_file(img_file):
    '''
    compute signal file
    :param img_file: QR code path
    :return: string decoded code
    '''
    reader = zxing.BarCodeReader()
    print('decode img {}...'.format(img_file))
    barcode = reader.decode('./upload/{}'.format(img_file))
    ret = barcode.parsed
    print('root is {}'.format(ret))
    return ret

def _qr_decode_all_file():
    '''
    compute all file under './upload'
    :return: string list decoded code
    '''
    reader = zxing.BarCodeReader()
    barcode_list = []
    qrcode_img_list = next(os.walk('upload'))[2]
    for qrcode_img in qrcode_img_list:
        print('decode img {}...'.format(qrcode_img))
        barcode = reader.decode('./upload/{}'.format(qrcode_img))
        barcode_list.append(barcode.parsed)
    return barcode_list
