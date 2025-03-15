# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON: 2021/9/1 10:33 AM
# LAST MODIFIED ON:
# AIM:
import os
import json

import loguru


def check_path(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)
        loguru.logger.info(f'dir {dir} not exist, create complete ')
    return dir


def read_json(path: str, verbose: bool = False):
    with open(path, 'r') as f:
        data = json.loads(f.read())
        if verbose:
            loguru.logger.info(f'loads success {path}')
    return data


def write_json(data, out_path: str):
    with open(out_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))


def load_file_to_list(path: str):
    with open(path, 'r') as f:
        data = [v.strip() for v in f.read().splitlines()]
    return [v for v in data if v]


def write_file(data: str, file_path: str):
    with open(file_path, 'w') as f:
        f.write(data)


def read_file(path: str):
    with open(path, 'r') as f:
        return f.read()
