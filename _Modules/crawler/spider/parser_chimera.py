# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/9/6 16:25
# @FileName : parser_chimera.py
# @SoftWare : PyCharm

"""
XHR获得真实请求地址：
    每页设备数 30， 不足30的则是最后一夜
page: [0, 292] 前闭后闭 数量：30*293， page=294设备数量10， 总数：8800
总数与首页列出的每个厂商的数量之和相等
page_ = divmod(sum(*list_count), 30)   # (293, 10), 则page_range = [0, page_[0] + 1]
"""

import asyncio
import re
import time
from itertools import chain

import aiofiles
import aiohttp
from async_retrying import retry
from bs4 import BeautifulSoup

from config.params import ATTEMPTS, TIME_OUT, CHIMERA_URL, CHIMERA_HEADERS, CHIMERA_PROXY, CHIMERA_BASE_URL, \
    NUMBER_PER_PAGE

url_success = []
url_failure = []
sema = asyncio.Semaphore(100)
loop = asyncio.get_event_loop()


@retry(attempts=ATTEMPTS)
async def get_web_content(url, headers=CHIMERA_HEADERS, proxy=CHIMERA_PROXY):
    """
    Obtain web content for a specified url
    :param configuration: dict
    :return:
    """
    async with sema:
        time_out = aiohttp.ClientTimeout(total=TIME_OUT)
        async with aiohttp.connector.TCPConnector(limit=300, force_close=True, enable_cleanup_closed=True, verify_ssl=False) as tc:
            async with aiohttp.ClientSession(connector=tc, timeout=time_out) as session:
                async with session.get(url=url, headers=headers, proxy=proxy) as resp:
                    status = resp.status
                    if status == 200:
                        web_content = await resp.text()
                        url_success.append(url)
                    else:
                        web_content = ''
                        url_failure.append(url)
    return web_content, url_success, url_failure


async def init_page_number():
    """
    Obtain total number of devices in the web
    :return:
    """
    web_content, _, _ = await get_web_content(url=CHIMERA_BASE_URL)
    soup = BeautifulSoup(web_content, 'lxml')
    device_number = soup.find('span', class_='opac-1').get_text()
    return device_number


async def init_page_number_task():
    tasks = [asyncio.ensure_future(init_page_number())]
    return await asyncio.wait(tasks)


def parser_device(web_content):
    """
    Parser device details for a specified web content
    :param web_content:
    :return:
    """
    soup = BeautifulSoup(web_content, 'lxml')
    model = soup.find_all('span', class_=["db model-name", "il-m model-type"])
    devices = {}
    for i in range(0, len(model), 2):
        name = model[i].get_text().strip()
        tmp1 = re.findall('<span class="il-m model-type">(.*?)<em class.*?</span>',
                          str(model[i + 1]),
                          re.S)
        tmp2 = re.findall('<span class="il-m model-type">(.*?)</span>',
                          str(model[i + 1]),
                          re.S)
        aliases = tmp1 or tmp2
        aliases = aliases[0].strip()
        if name not in devices.keys():
            devices[name] = []
        devices[name].append(aliases)
    return devices


async def init_parser_device_tasks(page_num):
    url = CHIMERA_URL
    headers = CHIMERA_HEADERS
    proxy = CHIMERA_PROXY
    tasks = [
        asyncio.ensure_future(
            get_web_content(
                url.format(page),
                headers,
                proxy)) for page in range(page_num)]
    return await asyncio.wait(tasks)


async def localization(dev_dict):
    """
    Localize to txt file with async aiofiles
    :param dev_dict:
    :return:
    """
    device_set = set()
    device_set = device_set.union(dev_dict.keys())
    device_set = device_set.union(list(chain(*dev_dict.values())))
    async with aiofiles.open('../output_chimera/device_chimera.txt', 'w', encoding='utf-8') as f:
        for device in device_set:
            await f.write(device + '\n')
    return len(device_set)


async def init_localization_tasks(dev_dict):
    tasks = [asyncio.ensure_future(localization(dev_dict))]
    return await asyncio.wait(tasks)


def get_page_number_async(loop):
    dones, _ = loop.run_until_complete(init_page_number_task())
    device_number = int([item.result() for item in dones][0].replace(',', ''))
    quotient, remainder = divmod(device_number, NUMBER_PER_PAGE)
    page_number = quotient + 1 if remainder else quotient
    return page_number


def get_total_devices_async(loop, page_num):
    devices = {}
    dones, _ = loop.run_until_complete(init_parser_device_tasks(page_num))
    for done in dones:
        devices.update(parser_device(done.result()[0]))
    return devices


def localization_async(dev_dict):
    dones, _ = loop.run_until_complete(init_localization_tasks(dev_dict))
    if len(dones) == 1:
        for done in dones:
            numbers = done.result()
    else:
        numbers = -1
        raise ValueError('invalid return value')
    return numbers


def start():
    """
    Entry of main function
    :return:
    """
    t1 = time.time()
    page_number = get_page_number_async(loop)
    print('page number consumed: ', time.time() - t1)
    print()

    t2 = time.time()
    total_devices = get_total_devices_async(loop, page_number)
    print('parse device consumed: ', time.time() - t2)
    print()

    t3 = time.time()
    model_number = localization_async(total_devices)
    print('device set cnt: ', model_number)                 # 11554
    print('localize consumed: ', time.time() - t3)

    loop.close()


if __name__ == '__main__':
    start()
