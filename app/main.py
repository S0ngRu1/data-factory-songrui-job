# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON:  4:25 PM
# LAST MODIFIED ON:
# AIM:
import time
#
from fastapi import FastAPI
#
from app.errors.hanlder import register_exception_handler
from app.utility.cors import init_cors


def register_echo(app):
    '''
    注册心跳和根目录
    '''

    @app.get('/health')
    def healty():
        return 'ok'

    @app.get('/api/info')
    def info():
        return 'success'

    @app.get('/')
    def healty():
        return f'Hello fellows {time.ctime()}'

    return app


def init_app(app):
    @app.on_event("startup")
    async def init_service():

        pass
        # 用于初始化一些特殊服务
        # -- demo --
        # await mysql_handler.init_app()
        # await request_handler.init_app()
        # redis_handler.init_app()


def register_routers(app):
    '''
    注册各个任务模块
    '''
    # TODO:定义域名
    # demo:
    # app.include_router(chem_router, prefix='/api/chem')
    # return app
    pass


def create_app():
    app = FastAPI()
    init_cors(app)
    #init_app(app) # 如果有东西需要init就uncommnet这个
    register_echo(app)
    register_exception_handler(app)
    register_routers(app)
    return app


app = create_app()
