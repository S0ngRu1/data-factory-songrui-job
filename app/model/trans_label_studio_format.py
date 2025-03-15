# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/29 09:25
# LAST MODIFIED ON:
# AIM:
import os.path
from typing import List,Dict

from tqdm import tqdm

from app.utility.file_opt import read_json, write_json

def get_data(dir_path) -> Dict:
    for data_file in os.listdir(dir_path):
        try:
            yield read_json(os.path.join(dir_path, data_file))
        except Exception as e:
            # 输出读取文件时的异常和文件名
            print(f"Error reading file: {data_file} - {str(e)}")
            continue  # 继续读取下一个文件

def trans_label_studio(dir_path:str)->List:
    json_data = []
    total_files = len(os.listdir(dir_path))
    for item in tqdm(get_data(dir_path), total=total_files):
        try:
            if item['annotations']:
                task_data = {
                    "data": {
                        "text": item['data']['text'],
                        "url": item['data']['url'],
                    },
                    "annotations": [],
                    "predictions": [
                        {
                            "model_version": "INITIAL",
                            "result": item['annotations'][0]['result'],
                        }
                    ]
                }
                json_data.append(task_data)
            else:
                json_data.append(item)
        except Exception as e:
            # 输出当前文件名以及错误信息
            print(f"Error processing file: {item.get('data', {}).get('file_name', 'Unknown')} - {str(e)}")
            continue  # 继续处理下一个 item

    return json_data


if __name__ == '__main__':
    data_dir_path = '../../data/results_labelstudio_1120_new'
    out_path = '../../data/results_labelstudio_1120_new.json'
    json_data = trans_label_studio(data_dir_path)
    write_json(json_data, out_path)
# print(transed_data)