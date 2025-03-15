# Author: caisongrui
# Created on: 2024/11/28 17:10
# Description:

import os.path
from typing import List,Dict
from tqdm import tqdm
from app.utility.file_opt import read_json, write_json


def trans_label_studio(data_path:str)->List:
    json_data = []
    datas = read_json(data_path)

    for data in datas:
        try:
            if data['entities']:
                text = data['text']
                url = data['url'] if data.get('url') else ''
                task_data = {
                    "data": {
                        "text": text,
                        "url": url,
                    },
                    "annotations": [],
                    "predictions": [
                        {
                            "model_version": "INITIAL",
                            "result":[
                                {"value":{
                                    "start": value['start_idx'],
                                    "end": value['end_idx'],
                                    "text": value['entity'],
                                    "labels":[value['category']]
                                    },
                                    "from_name": "label",
                                    "to_name": "text",
                                    "type": "labels"
                                } for value in data['entities']
                            ],
                        }
                    ]
                }
                json_data.append(task_data)
        except Exception as e:
            # 输出当前文件名以及错误信息
            print(f"Error processing file: {data.get('data', {}).get('file_name', 'Unknown')} - {str(e)}")
            continue  # 继续处理下一个 item

    return json_data


if __name__ == '__main__':
    data_path = '/home/zhangyuting/workspace/data-factory/data/erner-data/1.json'
    out_path = '/home/zhangyuting/workspace/data-factory/data/erner-data/1.json'
    json_data = trans_label_studio(data_path)
    # processed_json_data = merge_json_data(json_data)
    write_json(json_data, out_path)