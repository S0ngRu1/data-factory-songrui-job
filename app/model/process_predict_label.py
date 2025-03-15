# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/14 09:20
# LAST MODIFIED ON:
# AIM:
import re
from typing import Dict

from app.utility.file_opt import read_json


def process_predict_label(data: Dict) -> Dict:
    new_results = []
    for annotation in data['annotations'][0]["result"]:
        text = annotation["value"]["text"]
        label = annotation["value"]["labels"][0]
        start = annotation["value"]["start"]

        text_split = [s for s in re.split(r'(：|:|\n|\t| |，|（|）)', text) if s]

        for i, text_part in enumerate(text_split):
            new_results.append({
                "value": {
                    "start": start,
                    "end": start + len(text_part),
                    "text": text_part,
                    "labels": [label] if text_part not in ['：',':','\n','\t','（',' ','）'] else ["OTHER"]
                },
                "from_name": 'label',
                "to_name": 'text',
                "type": 'labels'
            })
            start += len(text_part)

    data['annotations'][0]["result"] = new_results
    return data

if __name__ == '__main__':
    data = read_json('../../data/sample_data_09:15:42.674474/1575343474213.json')
    process_data = process_predict_label(data)
    print(process_data)