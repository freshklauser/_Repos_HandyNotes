# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/7/19 21:04
# @FileName : read_sqlyog.py
# @SoftWare : PyCharm

"""
https://www.cnblogs.com/gayhub/p/python3-sqlyog-password.html
"""
import base64
import os

from Crypto import Random
from cryptography.hazmat.primitives.ciphers.algorithms import AES


def to_decode(base64str):
    tmp = base64.b64decode(base64str)
    print(type(tmp), tmp)
    return bytearray([(b<<1&255)|(b>>7) for b in tmp]).decode("utf8")


def to_encode(string):
    tmp = ''.join([b for b in string])
    print(tmp, '-----')
    return base64.b64encode(tmp.encode('utf-8'))


def encrypt(originalPassword):
    # 加密函数
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    paddPassword = pad(originalPassword)
    iv = Random.OSRNG.new().read(bs)
    key = os.urandom(32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptPassword = base64.b64encode(iv + cipher.encrypt(paddPassword) + key)
    return encryptPassword


def decrypt(encryptPassword):
    # 解密函数
    base64Decoded = base64.b64decode(encryptPassword)
    bs = AES.block_size
    unpad = lambda s: s[0:-s[-1]]
    iv = base64Decoded[:bs]
    key = base64Decoded[-32:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    originalPassword = unpad(cipher.decrypt(base64Decoded[:-32]))[bs:]
    return originalPassword


if __name__ == '__main__':
    # s = 'asd123456654321'
    # b64_passwd = to_encode(s)
    # print(b64_passwd)
    # passwd = to_decode(b64_passwd)
    # print(passwd)

    org_pwd = 'asd123456'
    print(encrypt(org_pwd))
