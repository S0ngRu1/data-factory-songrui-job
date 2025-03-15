# -*- coding: utf-8 -*- #
# CREATED BY: yohoo
# CREATED ON: 2023/12/6 上午11:54
# LAST MODIFIED ON:
# AIM:
# reference :https://www.reddit.com/r/learnpython/comments/12ershy/how_to_maintain_a_single_aiohttp_session_for_all/
import io
import json

import aiohttp

from app.handler.handler_abc import AsyncHandlerABC
from app.errors.service_exception import DownloadsFailErr, PostRequestErr


class RequestHandler(AsyncHandlerABC):

    def __init__(self):
        self._session = None

    async def build_session(self):
        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    async def init_app(self):
        await self.build_session()

    async def __aenter__(self):
        await self.build_session()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def download(self, url: str, timeout: int = 15):
        async with self._session.get(url, timeout=timeout) as r:
            if r.status == 200:
                return await r.read()
            else:
                raise DownloadsFailErr(f"Error downloading URL: {r.status} {r.reason}")

    async def post(self, url: str, data: dict, timeout: int = 15):
        header = {'Content-Type': 'application/json'}
        data = json.dumps(data, ensure_ascii=False)
        bytes_data = io.BytesIO(data.encode())
        async with self._session.post(url, data=bytes_data, headers=header,timeout=timeout) as r:
            if r.status == 200:
                try:
                    return await r.json()
                except:
                    out = await r.text()
                    return json.loads(out)
            else:
                respones = await r.text()
                raise PostRequestErr(f"post server error: {r.status} {r.reason}, \n{respones}")


