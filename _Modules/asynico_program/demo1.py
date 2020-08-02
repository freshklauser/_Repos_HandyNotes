# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/8/2 21:55
# @FileName : demo2.py
# @SoftWare : PyCharm


import time, asyncio


async def do_work(x):
    print('waitting:', x)
    await asyncio.sleep(x)
    return 'Don after {}s'.format(x)

"""
三种不同的输出协程结果的方式：
await asyncio.gather(*tasks)
await asyncio.wait(tasks)
"""
async def main1():
    """
    返回的是协程的结果列表
    """
    # 创建多个协程对象： 3个task在4s内执行完（同步的话需要7s）
    coroutine1 = do_work(1)
    coroutine2 = do_work(4)
    coroutine3 = do_work(2)
    # 创建任务列表(以下两种方式都可以)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    return await asyncio.gather(*tasks)


async def main2():
    """
    返回的是协程的 Task 列表，取结果需要遍历, task.result()
    """
    # 创建多个协程对象： 3个task在4s内执行完（同步的话需要7s）
    coroutine1 = do_work(1)
    coroutine2 = do_work(4)
    coroutine3 = do_work(2)
    # 创建任务列表(以下两种方式都可以)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    return await asyncio.wait(tasks)


async def main3():
    """
    返回的是协程的结果列表
    """
    # 创建多个协程对象： 3个task在4s内执行完（同步的话需要7s）
    coroutine1 = do_work(1)
    coroutine2 = do_work(4)
    coroutine3 = do_work(2)
    # 创建任务列表(以下两种方式都可以)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)
    return results


start = time.time()
# 创建事件循环对象
loop = asyncio.get_event_loop()
# 将 main 协程对象加入到事件循环中
# ------- 返回方式1 -------
results1 = loop.run_until_complete(main1())
print(results1)
for result in results1:
    print("Task 返回结果：", result)
print()

# ------- 返回方式2 -------
dones, apendings = loop.run_until_complete(main2())
print(dones, apendings)
for task in dones:
    print("Task 返回结果：", task.result())
print()

# ------- 返回方式3 -------
results3 = loop.run_until_complete(main3())
print(results3)
for result in results1:
    print("Task 返回结果：", result)
print()

print('TIME:', time.time()-start)