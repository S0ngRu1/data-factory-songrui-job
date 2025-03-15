# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON:  4:24 PM
# LAST MODIFIED ON:
# AIM:
def on_success(code=0, data={}, message='success'):
    return {'code': code, 'data': data, 'message': message}


def on_failed(code=-1, data={}, message='failed'):
    return {'code': code, 'data': data, 'message': message}
