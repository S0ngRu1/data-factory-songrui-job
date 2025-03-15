# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/22 11:14
# LAST MODIFIED ON:
# AIM:
import os
from typing import Dict

from app.utility.file_opt import read_json


def yield_json_file(json_dir: str):
    for file in os.listdir(json_dir):
        file_name, extend = os.path.splitext(file)
        if extend == '.json':
            data = read_json(os.path.join(json_dir, file))
            yield file_name, data
def collect_id_data(dir_path: str) -> Dict:
    id_data = {}
    for _, data in yield_json_file(dir_path):
        for id_key, entries in data.items():  # 遍历每个 ID 和对应的条目
            if id_key not in id_data:
                id_data[id_key] = []  # 初始化列表
            for entry in entries:
                id_data[id_key].append(entry)
    return id_data

if __name__ == '__main__':
    id_data = collect_id_data('/home/zhangyuting/workspace/palword/data/起搏器数据合并/sorted')
    print(id_data)