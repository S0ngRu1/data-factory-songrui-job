#!/usr/bin/python3
import json
import traceback
from loguru import logger
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.errors.service_exception import ServiceException


def safe_run(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            info = f'{err}:{err.__class__.__name__}, args:{args}, kwargs:{kwargs}\n{traceback.format_exc()}'
            raise ServiceException(info)
    return func_wrapper


def register_exception_handler(app):
    @app.exception_handler(ServiceException)
    def service_exception_handler(request: Request, err: ServiceException):
        return JSONResponse(
            status_code=200,
            content=err.dict()
        )

    @app.exception_handler(Exception)
    def exception_handler(request: Request, err: Exception):
        return JSONResponse(
            status_code=200,
            content={'code': 500, 'message': str(err)}
        )

    @app.exception_handler(RequestValidationError)
    def pydantic_exception_handler(request: Request, err: Exception):
        return JSONResponse(
            status_code=200,
            content={'code': 422, 'message': str(err)}
        )

    return app

'''
装饰一个类的所有方法
1. 装饰类的装饰器
def decorate_all_methods(decorator):

用法：
@decorate_all_methods(mydecorator)
class C(object):
    def m1(self): pass
    def m2(self, x): pass

2. 使用元类
class ServiceMetaClass(type):

用法：
class myClass(object):
    __metaclass__ = ServiceMetaClass
    def baz(self):
        print self.baz.foo
'''


def decorate_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


class ServiceMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value):
                local[attr] = safe_run(value)
        return type.__new__(cls, name, bases, local)
