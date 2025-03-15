'''
用户自定义 service 错误类型和错误处理 wrapper
'''
from loguru import logger


class ServiceException(Exception):
    def __init__(self, code: int = -1, message: str = 'failed', data=None):
        self.code = code
        self.message = message
        self.data = data

    def dict(self):
        result = {'code': self.code, 'message': self.message}
        if self.data:
            result['data'] = self.data
            if 'create_at' in result['data']:
                del result['data']['create_at']

            if 'update_at' in result['data']:
                del result['data']['update_at']
        return result

    @classmethod
    def parse_obj(cls, obj: dict):
        return ServiceException(code=obj['code'], message=obj['message'])
