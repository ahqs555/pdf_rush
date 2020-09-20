import os
import time
import json
import base64
import requests

dir = 'pdfs'
file = '1ParaOS-Gairon.pdf'
file_path = os.path.join(os.getcwd(), dir, file)
topath = os.path.join(os.getcwd(), dir, 'output.pdf')
def get_base64str(file_path):
    """获取base64位字符串
       bytes字节 -->base64字节 --> base64字符串
    """
    str_base64 = None
    with open(file_path,'rb') as f:
        bytes_base64 = base64.b64encode(f.read())
        str_base64 = bytes_base64.decode('utf-8')
        print(str_base64.encode("utf-8"))
    assert str_base64 is not None
    return str_base64

def save_file(str_base64,topath):
    """将base64还原存储为文件,
       查看文件是否能正常打开,
       以确认编码正确.
    """
    bytes_base64 = str_base64.encode('utf-8')
    with open(topath,'wb') as f:
        _bytes = base64.b64decode(bytes_base64)
        f.write(_bytes)


str_base64 = get_base64str(file_path)

save_file(str_base64, topath)
