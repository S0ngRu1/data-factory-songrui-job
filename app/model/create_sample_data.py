# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/11 17:22
# LAST MODIFIED ON:
# AIM:

import json
import os
import  random
from typing import List
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utility.file_opt import read_json, write_json, write_file, check_path


def get_created_data_content(dir_path :str)->List[str]:
    create_data_contents = []
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        datas = read_json(file_path)
        for data in datas:
            create_data_contents.append(data['data']['text'])
    return create_data_contents

def create_sample_data(num_of_sample: int, result_labelstudio_path: str):
    create_data_contents = set(get_created_data_content('../../data/ocr_ner_sample_datas'))
    json_files = read_json(result_labelstudio_path)
    json_data_contents = []
    json_data = []
    num_ = 0
    # 顺序选取数据
    for i in range(len(json_files)):
        data = json_files[i]
        if (data['data']['text'] not in create_data_contents and len(data['data']['text']) > 100 and len(data['predictions'][0]['result']) > 5
                and data['data']['text'] not in json_data_contents):
            json_data.append(data)
            num_ += 1
        if num_ >= num_of_sample:
            break

    return json_data

if __name__ == '__main__':
    result_labelstudio_path = '../../data/result_labelstudio_1111.json'
    time = '2025.1.21'
    output_path = f'../../data/sample_data_{time}.json'
    sample_data = create_sample_data(1000, result_labelstudio_path)
    write_json(sample_data, output_path)
