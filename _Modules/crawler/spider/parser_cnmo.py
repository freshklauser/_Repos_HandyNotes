# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/9 14:34
# @FileName : parser_cnmo.py
# @SoftWare : PyCharm

"""
TODO:
    (1) 增加回调函数，fetch和parser_web_content之间的回调
"""

import asyncio
import json
import re
from pprint import pprint

import aiohttp
import aiofiles
from async_retrying import retry
from bs4 import BeautifulSoup

from config.logger import helper, crawler
from config.params import ATTEMPTS, TIME_OUT, BASE_URL, headers, COLLECTIONS, SEMA_AMOUNT
from db.motor_handler import MotorBase
from utils.general import generate_uuid, generate_document


sema = asyncio.Semaphore(SEMA_AMOUNT)


@retry(attempts=ATTEMPTS)
async def get_web_content():
    time_out = aiohttp.ClientTimeout(total=TIME_OUT)
    async with aiohttp.connector.TCPConnector(limit=300, force_close=True, enable_cleanup_closed=True, verify_ssl=False) as tc:
        async with aiohttp.ClientSession(connector=tc, timeout=time_out) as session:
            async with session.get(url=BASE_URL, headers=headers, proxy=None) as resp:
                helper.info('response attr or func of aiohttp.ClientSession.get: \n{}'.format([item for item in dir(resp) if not item.startswith("_")]))
                status = resp.status
                if status == 200:
                    web_content = await resp.text()
    return web_content


async def parser_web_content(content):
    """
    brand_uuid: 品牌的uuid， name=brand生成
    model_uuid: 款型的uuid, name=brand+model生成
    :param content:
    :return:
    """
    phones = []
    soup = BeautifulSoup(content, features="lxml")
    helper.info("dir(soup): \n{}".format([item for item in dir(soup) if not item.startswith("_")]))
    tags_a = soup.find_all('a', class_='manu-tab-logo')
    tags_a_div = soup.find_all('div', class_='manu-tab-link')
    for tag_a, tag_a_div in zip(tags_a, tags_a_div):
        # TODO: 中英文名的映射，替换为英文名，且款型也要都换成英文名
        brand = tag_a.get_text().strip().replace("手机", '')
        tag_a_div_a = tag_a_div.find_all('a')
        phones.extend([generate_document(brand, item.get_text().strip()) for item in tag_a_div_a])
    return phones


async def write_to_mongodb(documents):
    # 异步写入mongo
    result = await MotorBase().do_insert_many(COLLECTIONS[0], documents)
    if result.acknowledged:
        crawler.info('页面解析成功，且写入mongodb数据库成功')
    else:
        crawler.error('页面解析失败或写入mongodb数据库失败', exc_info=True, stack_info=True)


async def localize(documents):
    pass


async def process_total():
    content = await get_web_content()
    documents = await parser_web_content(content)
    async with sema:
        await write_to_mongodb(documents)
        await localize(documents)


def entry():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(process_total())
    except (NotImplementedError, KeyboardInterrupt):
        status = asyncio.wait(*asyncio.Task.all_tasks()).cancel()
        pprint('status: ', status)
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    entry()
