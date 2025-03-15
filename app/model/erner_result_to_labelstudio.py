# Author: caisongrui
# Created on: 2025/2/20 10:44
# Description:

from typing import List,Dict
from app.utility.file_opt import read_json, write_json

relation_type_map = {
    1: "ABB",
    2: "VALUE",
    3: "RANGE",
    4: "METHOD",
    5: "UNIT"
}
def convert_relations_to_result_format(predicted_er_labels, entity_results):
    entity_id_map = {}
    for entity in entity_results:
        start = entity['value']['start']
        end = entity['value']['end']
        entity_id_map[(start, end)] = (entity['id'],entity['value']['labels'][0])

    relations = []
    for relation in predicted_er_labels[0]:
        # 获取from实体的位置
        from_start, from_end = relation[0]
        # 获取to实体的位置
        to_start, to_end = relation[2]
        # 获取关系类型
        relation_type = relation[1]
        # 查找对应的entity id
        # if entity_id_map.get((from_start, from_end))[1] in ['CI','CI_ABB'] :
        from_id = entity_id_map.get((from_start, from_end))[0]
        to_id = entity_id_map.get((to_start, to_end))[0]
        if from_id and to_id:
            relation_dict = {
                "from_id": from_id,
                "to_id": to_id,
                "type": "relation",
                "direction": "right" if from_start < to_start else "left",
                "labels": [relation_type_map.get(relation_type, "")]
            }
            relations.append(relation_dict)

    return relations

import random
import string

def generate_random_id(length=10):
    """生成由字母和数字组成的随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 用于保存已生成的ID，确保不重复
unique_ids = set()

def get_unique_id(length=10):
    new_id = generate_random_id(length)
    while new_id in unique_ids:
        new_id = generate_random_id(length)
    unique_ids.add(new_id)
    return new_id
def trans_label_studio(data_path:str)->List:
    json_data = []
    datas = read_json(data_path)

    for i, data in enumerate(datas):
        if data['entities']:
            text = data['text']
            # original_text = data['original_text']
            task_data = {
                "data": {
                    "text": text,
                    # "original_text": original_text,
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
                                "id": get_unique_id(),
                                "from_name": "label",
                                "to_name": "text",
                                "type": "labels"
                            } for value in data['entities']
                        ],
                    }
                ]
            }
            task_data_result = task_data['predictions'][0]['result']
            relations = convert_relations_to_result_format(data['predicted_er_labels'], task_data_result)
            task_data['predictions'][0]['result'].extend(relations)
            json_data.append(task_data)

    return json_data


if __name__ == '__main__':
    data_path = '/home/zhangyuting/workspace/data-factory/data/erner-data/erner_ci_0310_train_processed_erner.json'
    out_path = '/home/zhangyuting/workspace/data-factory/data/erner-data/erner_ci_0310_train_processed_erner_lbl_std.json'
    json_data = trans_label_studio(data_path)
    write_json(json_data, out_path)