# -*- coding: utf-8 -*-
# Author: caisongrui
# Date: 2025-03-14
# Description: Description of the file
import os
from typing import List, Dict
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utility.file_opt import read_json, write_json
from generater_abc import TrainDataGeneraterABC

class GenerateOcrNerDatasets(TrainDataGeneraterABC):

    def lbl_std2train_data(self,lbl_std_data_path:str, output_dir:str):
        labelstudio_datas = read_json(lbl_std_data_path)   
        for lbl_std_data in labelstudio_datas:
            if self.isnot_have_label(lbl_std_data):
                continue
            full_text = lbl_std_data['data']['text']
            bio_annotations = ["O"] * len(full_text)
            annotations = lbl_std_data['annotations'][0]['result']
            # annotations.extend(result['annotations'][0]['prediction']["result"])
            # 检查并处理重叠标注
            annotations = self.merge_overlapping_annotations(annotations)
            for annotation in annotations:
                text = annotation["value"]["text"]
                if not text:
                    continue
                label = annotation["value"]["labels"][0]
                if label in ['HD','HN','PI','TI','CI_M'] and len(text) < 2:
                    continue
                if label == "OTHER":
                    continue
                start_idx = annotation['value']["start"]
                end_idx = annotation['value']["end"]
                if any(bio_annotations[idx] != "O" for idx in range(start_idx, end_idx)):
                    continue
                for idx in range(start_idx, end_idx):
                    if idx == start_idx:
                        bio_annotations[idx] = f"B-{label}"
                    else:
                        bio_annotations[idx] = f"I-{label}"
            final_annotations = []
            for idx, char in enumerate(full_text):
                if char == '\n':
                    char ="[ENTER]"
                if char == ' ':
                    char ="[SPACE]"
                if char == '\t':
                    char ="[TAB]"
                final_annotations.append(f"{char}\t{bio_annotations[idx]}")
            
            if len(final_annotations)>0:
                filepath = os.path.join(output_dir, str(lbl_std_data['id']) + '.txt')
                with open(filepath, 'w', encoding='utf-8') as file:
                    for item in final_annotations:
                        file.write(item+ '\n')
    
    @staticmethod
    def isnot_have_label(result)->bool:
        annotations = result['annotations'][0]["result"]
        if len(annotations) == 0:
            return True

    def lbl_std2predict_format(self,data_path:str, bio_data_dir_path)->List[Dict]:
        """
        label studio 标注数据转换为ocr_ner预测数据格式
        param data_path: label studio 标注数据路径
        param bio_data_dir_path: BIO数据路径  '/home/zhangyuting/workspace/data-factory/data/BIO_ocr_ner_1226/'
        return: json_data
        """
        json_data = []
        datas = read_json(data_path)

        for data in datas:
            text = data['data']['text']
            ocr_ner_results = data['annotations'][0]['result']
            entities = []
            bio_data_path = bio_data_dir_path + str(data['id']) + '.txt'
            bio_list = self.get_bio_list(bio_data_path)
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
    
    @staticmethod
    def get_bio_list(data_path:str)->List:
        bio_list = []
        with open(data_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if len(line.strip().split('\t')) > 1:
                    _, value = line.strip().split('\t')
                    bio_list.append(value)

        return bio_list

    def predict_data2lbl_std(self,data_path:str):
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
    
    def split_train_val_datasets(self):
        pass

    def get_deduplicated_txts(self,sample_data_dir_path):
        sample_datas = {}
        for file_path in os.listdir(sample_data_dir_path):
            file_path = os.path.join(sample_data_dir_path,file_path)
            sample_data = read_json(file_path)
            for data in sample_data:
                txt = data['data']['text']
                url = data['data']['url']
                annotations = data['predictions'][0]['result']
                if self.ci_num_in_data(annotations) > 2 and txt not in sample_datas:
                    sample_datas[txt] = {'txt': txt, 'url': url}
        sample_datas = list(sample_datas.values())
        return sample_datas
    
    @staticmethod
    def ci_num_in_data(annotations:List):
        num = 0
        for annotation in annotations:
            if 'CI' in annotation['value']['labels']:
                num += 1
        return num
    @staticmethod
    def get_created_data_content(dir_path :str)->List[str]:
        create_data_contents = []
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            datas = read_json(file_path)
            for data in datas:
                create_data_contents.append(data['data']['text'])
        return create_data_contents

    def create_sample_data(self,num_of_sample: int, result_labelstudio_path: str):
        create_data_contents = set(self.get_created_data_content('data/ocr_ner_sample_datas'))
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
        
def main():

    # smaple_data_dir_path = 'data/ocr_ner_sample_datas/'
    # process_sample_data_path = 'data/ocr_ner_deduplicated_txts.json'
    predict_result_path = 'data/ocr_ner_deduplicated_txts_predict.json'
    lbl_std_data_path = 'data/ocr_ner_deduplicated_txts_predict_lbl_std.json'
    generate_ocr_ner_datasets = GenerateOcrNerDatasets()

    # Step 1 :生成样本数据
    # result_labelstudio_path = '../../data/result_labelstudio_1111.json'
    # time = '2025.1.21'
    # sample_data_output_path = f'data/ocr_ner_sample_datas/sample_data_{time}.json'
    # sample_data = generate_ocr_ner_datasets.create_sample_data(1000, result_labelstudio_path)
    # write_json(sample_data, sample_data_output_path)


    # Step 2 :得到去重后的原文本
    # deduplicated_txts = generate_ocr_ner_datasets.get_deduplicated_txts(smaple_data_dir_path)
    # write_json(deduplicated_txts, process_sample_data_path)
    # Step 3 :ocr_ner数据预测

    # Step 4 :ocr_ner 数据预测转换为label studio数据 
    lbl_std_datas = generate_ocr_ner_datasets.predict_data2lbl_std(predict_result_path)
    write_json(lbl_std_datas, lbl_std_data_path)


if __name__ == '__main__':

    main()