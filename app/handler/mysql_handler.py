# -*- coding: utf-8 -*- #
# CREATED BY: yohoo
# CREATED ON: 2023/11/28 下午1:59
# LAST MODIFIED ON:
# AIM:
from typing import Tuple, List

import aiomysql
from loguru import logger

from app.handler.handler_abc import AsyncHandlerABC
from app.utility.wrapper import time_cost
from pymysql.err import OperationalError

'''
pymysql.err.OperationalError: 
'''


class MysqlHandler(AsyncHandlerABC):

    def __init__(self,
                 host: str,
                 user: str,
                 password: str,
                 database: str,
                 port: str = '3306',
                 minsize: str = '10',
                 maxsize: str = '20'):
        env = {
            "host": host,
            "user": user,
            "port": int(port),
            "password": password,
            "db": database,
            "minsize": int(minsize),
            "maxsize": int(maxsize)
        }
        self.env = env
        self.pool = None
        self.__connected = False

    async def connect(self):
        logger.info("mysql build connection ..")
        if 'charset' not in self.env:
            self.env['charset'] = 'utf8'
            self.env['autocommit'] = True

        self.pool = await aiomysql.create_pool(**self.env)
        logger.info("mysql connection established")
        self.__connected = True

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def init_app(self):
        await self.connect()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    def reconnect(self, func):
        async def wrapper(*args):
            try:
                out = await func(*args)
            except OperationalError:
                await self.connect()
                logger.warning('reconnect')
                out = await func(*args)
            return out

        return wrapper

    @time_cost
    async def __select(self, sql_query: str) -> List[dict]:
        assert 'select' in sql_query.lower(), f"select function must be select query!, expect 'SELECT xxx FROM XXX' but '{sql_query}'"
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                logger.info(f'execute sql {sql_query}')
                await cur.execute(sql_query)
                result = await cur.fetchall()
                logger.info(f'sql complete')
                return result

    async def select(self, sql_query: str) -> List[dict]:
        out = await self.reconnect(self.__select)(sql_query)
        return out

    @time_cost
    async def __update(self, sql_query: str, value: Tuple) -> bool:
        assert 'update' in sql_query.lower(), f"update function must be select query!, expect 'UPDATE xxx SET xxx=xx WHERE ..' but {sql_query}"
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    logger.info(f'UPDATE sql {sql_query}, {value}')
                    await cur.execute(sql_query, value)
                    await conn.commit()
                    logger.info(f'sql complete')
                    return True
        except Exception as e:
            if not isinstance(e, OperationalError):
                await conn.rollback()
                logger.error(e)
                return False
            raise e

    async def update(self, sql_query: str, value: Tuple) -> bool:
        out = await self.reconnect(self.__update)(sql_query, value)
        return out

    @time_cost
    async def __insert(self, sql_query: str, value: Tuple) -> bool:
        assert 'insert' in sql_query.lower(), f"insert function must be insert query!, expect 'INSERT INTO xxx (xxxx) VALUES ()' but {sql_query}"
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    logger.info(f'execute sql {sql_query}, {value}')
                    await cur.execute(sql_query, value)
                    await conn.commit()
                    logger.info(f'sql complete')
                    return True
        except Exception as e:
            if not isinstance(e, OperationalError):
                await conn.rollback()
                logger.error(e)
                return False
            raise e

    async def insert(self, sql_query: str, value: Tuple) -> bool:
        out = await self.reconnect(self.__insert)(sql_query, value)
        return out
