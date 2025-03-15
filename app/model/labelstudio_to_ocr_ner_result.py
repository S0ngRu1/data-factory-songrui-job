# Author: caisongrui
# Created on: 2025/2/10 09:15
# Description:

from typing import List

from app.utility.file_opt import read_json, write_json

def get_bio_list(data_path:str)->List:
    bio_list = []
    with open(data_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if len(line.strip().split('\t')) > 1:
                _, value = line.strip().split('\t')
                bio_list.append(value)

    return bio_list



def label_studio_to_ocr_ner_result(data_path:str)->List:
    json_data = []
    datas = read_json(data_path)

    for data in datas:
        text = data['data']['text']
        ocr_ner_results = data['annotations'][0]['result']
        entities = []
        bio_data_path = '/home/zhangyuting/workspace/data-factory/data/BIO_ocr_ner_1226/' + str(data['id']) + '.txt'
        bio_list = get_bio_list(bio_data_path)
        for ocr_ner_result in ocr_ner_results:
            single_entity = {
                "category":ocr_ner_result['value']['labels'][0],
                "entity":ocr_ner_result['value']['text'],
                "start_idx":ocr_ner_result['value']['start'],
                "end_idx":ocr_ner_result['value']['end']
            }
            entities.append(single_entity)

        task_data = {
            "text": text,
            "entities": entities,
            "bio_list": bio_list
        }
        json_data.append(task_data)
    return json_data




if __name__ == '__main__':
    data_path = '/home/zhangyuting/workspace/data-factory/data/project-139-at-2024-12-26-05-43-70944606.json'
    out_path = '../../data/results_ocr_ner_1226.json'
    json_data = label_studio_to_ocr_ner_result(data_path)
    # processed_json_data = merge_json_data(json_data)
    write_json(json_data, out_path)