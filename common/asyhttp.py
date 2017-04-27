import asyncio

def asyn(fun):
    loop = asyncio.get_event_loop()
    tasks = asyncio.ensure_future(fun)
    loop.run_until_complete(tasks)
    # loop.close()
    print('Task ret: {}'.format(tasks.result()))
    return tasks.result()