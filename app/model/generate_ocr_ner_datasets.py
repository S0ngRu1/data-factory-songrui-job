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
    def lbl_std2train_data(self):
        
        pass

    def train_data2lbl_std(self):
        pass

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
        
def main():
    
    # smaple_data_dir_path = 'data/ocr_ner_sample_datas/'
    # process_sample_data_path = 'data/ocr_ner_deduplicated_txts.json'
    predict_result_path = 'data/ocr_ner_deduplicated_txts_predict.json'
    lbl_std_data_path = 'data/ocr_ner_deduplicated_txts_predict_lbl_std.json'
    generate_ocr_ner_datasets = GenerateOcrNerDatasets()
    # # 得到去重后的原文本
    # deduplicated_txts = generate_ocr_ner_datasets.get_deduplicated_txts(smaple_data_dir_path)
    # write_json(deduplicated_txts, process_sample_data_path)
    # ocr_ner数据预测

    # ocr_ner 数据预测转换为label studio数据 
    lbl_std_datas = generate_ocr_ner_datasets.predict_data2lbl_std(predict_result_path)
    write_json(lbl_std_datas, lbl_std_data_path)


if __name__ == '__main__':

    main()