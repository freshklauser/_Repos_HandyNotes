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
asyncio.as_completed(tasks)
"""
async def main():
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


start = time.time()
# 创建事件循环对象
loop = asyncio.get_event_loop()

# ---> 将 main() 协程创建成task
task = asyncio.ensure_future(main())

# 将 main()的task 加入到事件循环中
try:
    results = loop.run_until_complete(task)
except KeyboardInterrupt as err:
    all_tasks = asyncio.Task.all_tasks()
    print(len(all_tasks), all_tasks)
    status = asyncio.gather(*asyncio.Task.all_tasks()).cancel()
    print(status)
    loop.stop()
    loop.run_forever()
finally:
    loop.close()
#
# print('results:', results)
# for result in results:
#     print("Task 返回结果：", result)
# print()

print('TIME:', time.time()-start)