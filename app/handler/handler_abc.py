# -*- coding: utf-8 -*- #
# CREATED BY: yohoo
# CREATED ON: 2023/12/7 上午9:53
# LAST MODIFIED ON:
# AIM:

class HandlerABC:
    pass


class AsyncHandlerABC(HandlerABC):
    async def init_app(self):
        raise NotImplementedError
