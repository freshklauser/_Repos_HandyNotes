# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/9 14:19
# @FileName : crawl_demo.py
# @SoftWare : PyCharm
import io
import sys
from pprint import pprint

import requests
from bs4 import BeautifulSoup
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from config.logger import helper
from config.params import BASE_URL, headers

# print(sys.getdefaultencoding())  # utf-8
resp = requests.get(BASE_URL, headers=headers)
# resp.encoding = 'GBK'
# # resp.encoding = 'utf-8'
resp.encoding = 'gbk'
# pprint(resp.encoding)
helper.info(resp.text.encode())
print('\ufffd'.encode('utf-8'))
print('\xbd')
print('0xfb'.encode('gbk'))



# resp.encoding = resp.apparent_encoding
# resp.encoding = 'utf-8-sig'
# html = resp.text.encode("ISO-8859-1'").decode('utf-8-sig')
# html = resp.text.encode('gbk').decode('utf-8-sig')
# html= resp.text.replace('\ufffd','')
# resp.encoding = 'gbk'
# html = resp.text
# soup = BeautifulSoup(resp.text,"lxml")
# print(resp.encoding)
# print(resp.apparent_encoding)
# pprint(headers)
# resp.encoding = 'ISO-8859-1'
# resp.encoding = 'gbk'
# html = resp.text.encode("ISO-8859-1'")
# pprint(html)
#
# bf = BeautifulSoup(html)
# texts = bf.find_all('div', id='content')
# print(texts)

# with open('demo/html.txt', 'w', encoding='utf-8-sig') as f:
#     f.write(html)


