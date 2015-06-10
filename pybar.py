#! /usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio.subprocess
from functools import partial

bardata = {}


def init_bar():
    print("{\"version\": 1}")
    print('[')
    print('[]')


def save_data(future):
    (key, value), _ = future.result()
    bardata[key] = value
    print_bar()


def print_bar():
    print([bardata])


@asyncio.coroutine
def get_dns(*args, **kwargs):
    yield from asyncio.sleep(1)
    return ('dns', 'whatever'), (get_dns, None, None)


def schedule_task(future):
    _, (func, args, kwargs) = future.result()

    reduced_function = partial(func, args or [], kwargs or {})

    if not asyncio.iscoroutine(reduced_function):
        reduced_function = asyncio.coroutine(reduced_function)

    new_task = loop.create_task(reduced_function())
    new_task.add_done_callback(save_data)
    new_task.add_done_callback(schedule_task)


loop = asyncio.get_event_loop()

loop.call_soon(init_bar)

my_task = loop.create_task(get_dns())
my_task.add_done_callback(save_data)
my_task.add_done_callback(schedule_task)

try:
    loop.run_until_complete(my_task)
    loop.run_forever()
finally:
    loop.close()
