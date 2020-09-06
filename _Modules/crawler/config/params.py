# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/8 15:43
# @FileName : params.py
# @SoftWare : PyCharm


import random

from utils.general import standard_path

ROOT_DIR = r'E:\_Jun\_Python\_Repos_HandyNotes\_Modules\crawler'

# file path
DEST_DIR = standard_path(ROOT_DIR, './output_chimera')
LOG_DIR = standard_path(ROOT_DIR, './logs')

# db params
DB_CONFIGS = {
    'type': 'mongo',
    'host': '192.168.13.132',
    'port': 27018,
    "user": "mongo",
    'db_name': 'spider'
}
COLLECTIONS = ['cnmo']


# async params
TIME_OUT = 30
ATTEMPTS = 3
MAX_DOCS_RETURN = 10
SEMA_AMOUNT = 5     # 并发量？？

# user-agent pool
UA_POOL = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
]

# website information
BASE_URL = "http://product.cnmo.com/manu.html"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Host": "product.cnmo.com",
    "Referer": "http://product.cnmo.com/all/product.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
}

# headers = {"User-Agent": random.choice(UA_POOL)}


# chimeratool
CHIMERA_BASE_URL = "https://chimeratool.com/zh/models"
CHIMERA_URL = "https://chimeratool.com/zh/models?q=&p={}&scroll=1"
CHIMERA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
CHIMERA_PROXY = None
NUMBER_PER_PAGE = 30


if __name__ == '__main__':
    print(headers.get("User-Agent"))
    print(DEST_DIR)
    # request headers from website
    """
    Host: product.cnmo.com
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Cookie: Hm_lvt_04fab3def376a222f35762aa47e96232=1596723798; ip_ck=5MSD5P3/j7QuMzMyMzc4LjE1OTY3MjM3OTg%3D; lv=1596883365; vn=2; cnmo_e476_post_seccode=a442lPvIhiF4KqGjK3CPj4%2FMHl3Fjcx%2FaMeyQvzElfaK1csct5wbRkrcIqA; Hm_lpvt_04fab3def376a222f35762aa47e96232=1596883365; z_pro_city=s_provice%3Dguangdong%26s_city%3Dguangzhou
    Upgrade-Insecure-Requests: 1
    Cache-Control: max-age=0
    """
    print(CHIMERA_URL.format(25))