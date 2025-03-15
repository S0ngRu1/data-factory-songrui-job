# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON:  4:27 PM
# LAST MODIFIED ON:
# AIM:

from fastapi.middleware.cors import CORSMiddleware

def init_cors(app):
    # 处理跨域
    origins = [
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
