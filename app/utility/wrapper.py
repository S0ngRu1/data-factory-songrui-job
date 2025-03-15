# -*- coding: utf-8 -*- #
# CREATED BY: yohoo
# CREATED ON: 2023/10/13 上午11:34
# LAST MODIFIED ON:
# AIM:
import pathlib
import sys
import signal
import asyncio

root = pathlib.Path(__file__).absolute().parents[2]
sys.path.append(str(root))
import os
import json
import functools

import time

from loguru import logger
from dotenv import load_dotenv

from app.utilities.file_opt import check_path

load_dotenv()


def eval_data_saver(file_name: str):
    def decorate(func):
        def wrapper(*args):
            input = args[0]
            output = func(*args)
            save_content = {"input": input, "output": output}
            out_path = os.path.join(root, 'data', 'info_extract')
            check_path(out_path)
            with open(os.path.join(out_path, file_name), 'a') as f:
                f.write("\n" + json.dumps(save_content, ensure_ascii=False))
            logger.info(f'write complete: {save_content}')
            return output

        return wrapper

    return decorate


def singleton(cls):
    _instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")


def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)  # Disable the alarm
            return result

        return wrapper

    return decorator


def time_cost(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            out = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f'{func.__class__.__name__} - {func.__name__} executed in {duration:.4f} s')
            return out
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            out = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f'{func.__class__.__name__} - {func.__name__} executed in {duration:.4f} s')
            return out

    return wrapper


def to_async_func(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    return wrapper


def add_log(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f'run {func.__qualname__}')
            start_time = time.time()
            out = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f'run {func.__qualname__} complete executed in {duration:.4f} s ')
            return out
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f'run {func.__qualname__}')
            start_time = time.time()
            out = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f'run {func.__qualname__} complete executed in {duration:.4f} s ')
            return out
    return wrapper


def phase_wrapper(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            env_phase = os.environ.get("PHASE")
            if env_phase == 'TEST':
                logger.info('phase in test')
                out = None
            else:
                out = await func(*args, **kwargs)
            return out
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            env_phase = os.environ.get("PHASE")
            if env_phase == 'TEST':
                logger.info('phase in test')
                out = None
            else:
                out = func(*args, **kwargs)
            return out
    return wrapper


def cache(maxsize=128):
    cache = {}
    queue = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (func.__name__,  str(args), frozenset([(k, str(v)) for k, v in kwargs.items()]))
            if key in cache:
                # 如果缓存中已经有结果，则将该结果移到队列尾部
                queue.remove(key)
                queue.append(key)
                return cache[key]
            result = func(*args, **kwargs)

            # 在缓存中存储结果
            cache[key] = result

            # 将新的结果加入队列尾部
            queue.append(key)

            # 如果缓存超过了最大容量，则移除队列头部的最早使用的结果
            if len(queue) > maxsize:
                old_key = queue.pop(0)
                del cache[old_key]

            return result

        return wrapper

    return decorator
