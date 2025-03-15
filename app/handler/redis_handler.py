# -*- coding: utf-8 -*- #
# CREATED BY: yohoo
# CREATED ON: 2023/12/6 上午10:25
# LAST MODIFIED ON:
# AIM:
import redis
from loguru import logger


class RedisHandler:
    def __init__(self, host: str, port: str, password: str = None):
        self.redis_client = redis.Redis(host, port, password=password)

    def get(self, key):
        logger.info(f'redis get key:{key}')
        return self.redis_client.get(key)

    def set(self, key: str, value: str, ex: int = 3600):
        logger.info(f'write to redis  key: {key}')
        return self.redis_client.set(key, value, ex=ex)

    def delete(self, key):
        logger.info(f'redis delete key:{key}')
        return self.redis_client.delete(key)

    def update(self, key, value):
        logger.info(f'reids update key:{key}')
        if self.redis_client.exists(key):
            return self.redis_client.set(key, value)
        else:
            return None
