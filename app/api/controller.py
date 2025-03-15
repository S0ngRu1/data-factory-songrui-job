# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON:  5:09 PM
# LAST MODIFIED ON:
# AIM:

from fastapi import APIRouter
from loguru import logger

#------------- 代码填入这里 ------------ #
# from fastapi import APIRouter
# import json
#
# from loguru import logger
#
# from app.schema.server import Request, Response
# from app.service.server import TxtExtractorServer
# from _version import __version__
# from app.config.server import load_config
#
# extraction_router = _router = APIRouter()
# extraction_server = TxtExtractorServer(**load_config())
#
#
# @_router.post('/text-extraction')
# async def extract(request: Request) -> Response:
#     logger.info(f'receive request {json.dumps(request.model_dump(), ensure_ascii=False, indent=2)}')
#     logger.info(f'version {__version__}')
#
#     out = extraction_server.extract(request)
#     return out
# ----------------------------------- #