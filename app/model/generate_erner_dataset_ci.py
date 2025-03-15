# Author: caisongrui
# Created on: 2025/2/21 13:48
# Description:
import copy
import random
import string
from typing import List, Dict, Tuple
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utility.file_opt import read_json, write_json
from merge_overlap_annotations import merge_overlapping_annotations
from generater_abc import TrainDataGeneraterABC


relation_type_map = {
    1: "ABB",
    2: "VALUE",
    3: "RANGE",
    4: "METHOD",
    5: "UNIT"
}

class GenerateErNerDatasets(TrainDataGeneraterABC):

    def __init__(self):
         # 用于保存已生成的ID，确保不重复
        self.unique_ids = set()

    def lbl_std2train_data(self):
        pass

    def train_data2lbl_std(self):
        pass

    def predict_data2lbl_std(self,data_path:str):
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
                                    "id": self.get_unique_id(),
                                    "from_name": "label",
                                    "to_name": "text",
                                    "type": "labels"
                                } for value in data['entities']
                            ],
                        }
                    ]
                }
                task_data_result = task_data['predictions'][0]['result']
                relations = self.convert_relations_to_labelstudio_format(data['predicted_er_labels'], task_data_result)
                task_data['predictions'][0]['result'].extend(relations)
                json_data.append(task_data)
            return json_data
        
    def get_unique_id(self, length=10):
        new_id = self.generate_random_id(length)
        while new_id in self.unique_ids:
            new_id = self.generate_random_id(length)
        self.unique_ids.add(new_id)
        return new_id
    
    @staticmethod
    def generate_random_id(length=10):
        """生成由字母和数字组成的随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def convert_relations_to_labelstudio_format(predicted_er_labels, entity_results):
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

    @staticmethod
    def generate_random_id(length=10):
        """生成由字母和数字组成的随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


    def split_train_val_datasets(self):
        pass


    @staticmethod
    def ci_num_in_data(annotations:List):
        num = 0
        for annotation in annotations:
            if 'CI' in annotation['value']['labels']:
                num += 1
        return num

    @staticmethod
    def split_sentence(txt: str, annotations: List) -> List[Dict]:
        allowed_labels = {'CI','CI_ABB'}
        ci_annotations = [ann for ann in annotations
                        if any(lbl in allowed_labels for lbl in ann.get('value', {}).get('labels', []))]
        ci_annotations.sort(key=lambda ann: ann['value']['start'])

        sentences = []
        if len(ci_annotations) < 7:
            sentences.append({
                'text': txt,
                'annotations': annotations
            })
            return sentences

        n = len(ci_annotations)
        for i in range(0, n, 6):
            first_ci = ci_annotations[i]
            # 如果存在完整的下一组，使用下一组第一个元素的开始位置作为结束位置，否则使用文本末尾
            if i + 6 < n:
                last_ci = ci_annotations[i + 6]
                sent_end = last_ci['value']['start']
            else:
                sent_end = len(txt)
            sent_start = first_ci['value']['start']
            sent_text = txt[sent_start:sent_end]
            new_annotations = []
            for ann in annotations:
                ann_start = ann['value']['start']
                ann_end = ann['value']['end']
                if ann_start >= sent_start and ann_end <= sent_end:
                    new_ann = copy.deepcopy(ann)
                    new_ann['value']['start'] = ann_start - sent_start
                    new_ann['value']['end'] = ann_end - sent_start
                    new_annotations.append(new_ann)

            # relations = create_relation(new_annotations)
            # new_annotations.extend(relations)
            sentences.append({
                'text': sent_text,
                'annotations': new_annotations
            })

        return sentences

    @staticmethod
    def get_boundary_type(sorted_anns: List[Dict]) -> str:
        """
        根据排序后第一个标注的类型，确定分组边界。
        如果第一个标注的类型是 "CI_ABB"，则以 "CI_ABB" 作为边界类型，
        否则以 "CI" 作为边界类型。
        """
        first_type = sorted_anns[0]["value"].get("labels")[0]
        return "CI_ABB" if first_type == "CI_ABB" else "CI"
    @staticmethod
    def group_annotations(sorted_anns: List[Dict], boundary_type: str) -> List[List[Dict]]:
        """
        根据边界类型将标注分组：
        - 如果遇到标注类型为 boundary_type，则认为是一个新组的起始点；
        - 否则，归入当前组。
        返回各组的标注列表。
        """
        groups = []
        current_group = []
        for ann in sorted_anns:
            ann_type = ann["value"].get("labels")[0]
            if ann_type == boundary_type:
                if current_group:
                    groups.append(current_group)
                current_group = [ann]
            else:
                if not current_group:
                    current_group = [ann]
                else:
                    current_group.append(ann)
        if current_group:
            groups.append(current_group)
        return groups
    @staticmethod
    def update_annotation(annotation: Dict, new_start: int, new_end: int) -> Dict:
        """
        复制原始标注并更新其在新文本中的起始和结束位置。
        """
        new_ann = copy.deepcopy(annotation)
        new_ann["value"]["start"] = new_start
        new_ann["value"]["end"] = new_end
        return new_ann

    def process_group(self,group: List[Dict],original_text: str,new_text: str,new_pos: int,
            possible_symbols: List[str]) -> Tuple[str, int, List[Dict]]:
        """
        处理单个组内的标注，保留组内实体之间的非实体内容：
        - 先在组开始时插入一次随机特殊符号作为组间分隔；
        - 遍历组内各标注：在当前标注前，复制原文本中从上一个标注结束位置（或组起始）到当前标注起始位置的非实体文本，
            然后拼接当前实体文本，更新 offset。
        返回更新后的 new_text、new_pos 以及该组更新后的标注列表。
        """
        group_annotations_updated = []
        # 在组开始时插入一次随机特殊符号作为组间分隔
        sep = random.choice(possible_symbols)
        new_text += sep
        new_pos += len(sep)
        # 记录当前组在原文本中的起始位置（即组内第一个标注的起始位置）
        group_start = group[0]["value"]["start"]
        # prev_end 用于记录上一个实体在原文本中的结束位置，
        # 对于第一个实体，prev_end 就等于 group_start
        prev_end = group_start
        # 依次处理组内每个标注
        for ann in group:
            # 复制实体前的非实体文本（即 gap 部分）
            gap_text = original_text[prev_end: ann["value"]["start"]]
            new_text += gap_text
            new_pos += len(gap_text)
            # 插入实体前的随机特殊字符
            symbol = random.choice(possible_symbols)
            new_text += symbol
            new_pos += len(symbol)
            # 追加实体文本
            start_new = new_pos  # 新文本中当前实体的起始位置
            entity_text = original_text[ann["value"]["start"]: ann["value"]["end"]]
            new_text += entity_text
            new_pos += len(entity_text)

            # 更新标注 offset（相对于 new_text 的位置）
            new_ann = self.update_annotation(ann, start_new, new_pos)
            group_annotations_updated.append(new_ann)

            # 更新 prev_end 为当前实体在原文本中的结束位置
            prev_end = ann["value"]["end"]

        return new_text, new_pos, group_annotations_updated

    @staticmethod
    def process_sentence(self, sentence: Dict, possible_symbols: List[str]) -> Dict:
        """
        处理单个句子：
        - 从 sentence["text"] 中提取原始文本；
        - 分离出类型为 "labels" 的标注与 "relation" 的标注；
        - 对 labels 按实体起始位置排序，并根据最前面实体的类型确定分组规则，再进行分组；
        - 保留原文本中第一个标注前的部分，然后依次处理各组，
            在组内调用 process_group 保留实体之间的非实体文本，同时更新实体 offset；
        - 最后附加原文本中最后一个标注之后的部分，并将 relation 标注添加进来。
        返回处理后的句子字典，同时保留原始文本作为 "original_text" 字段。
        """
        original_text = sentence["text"]
        annotations = sentence["annotations"]
        if not annotations:
            return {"text": original_text, "annotations": []}
        # 按 labels 中实体在原文本中的起始位置排序
        sorted_anns = sorted(annotations, key=lambda ann: ann["value"]["start"])
        boundary_type = self.get_boundary_type(sorted_anns)
        groups = self.group_annotations(sorted_anns, boundary_type)

        new_text = ""
        new_annotations = []
        new_pos = 0

        # 保留原文本中第一个标注之前的内容
        prefix = original_text[: sorted_anns[0]["value"]["start"]]
        new_text += prefix
        new_pos += len(prefix)

        # 依次处理各个组
        for i, group in enumerate(groups):
            new_text, new_pos, group_updated = self.process_group(group, original_text, new_text, new_pos, possible_symbols)
            new_annotations.extend(group_updated)

            if i < len(groups) - 1:
                current_group_last = group[-1]["value"]["end"]
                next_group_first = groups[i+1][0]["value"]["start"]
                gap_between = original_text[current_group_last: next_group_first]
                new_text += gap_between
                new_pos += len(gap_between)

        # 附加原文本中最后一个标注之后的部分
        last_end = sorted_anns[-1]["value"]["end"]
        suffix = original_text[last_end:]
        new_text += suffix

        return {"text": new_text, "annotations": new_annotations, "original_text": original_text}


    def process_splited_sentence(self,splited_sentences: List[Dict]) -> List[Dict]:
        """
        对切分后的句子进行扰乱排版处理：
        - 随机在实体之间插入回车、制表符、空格等字符；
        - 根据最前面实体的类型进行分组：
            如果最前面的实体类型是 "ci_abb"，则将从一个 "ci_abb" 到下一个 "ci_abb" 之间的实体作为一组；
            否则将从一个 "ci" 到下一个 "ci" 之间的实体作为一组；
        - 对组内的实体顺序进行随机打乱；
        - 重构文本时重新拼接各个实体，并更新标注的 offset（"start" 和 "end"）。
        返回处理后的句子列表，每个句子包含更新后的 "text" 与 "annotations"。
        """
        processed = []
        possible_symbols = ["\n", "\t", " ", "   ", "  "]
        for sentence in splited_sentences:
            processed_sentence = self.process_sentence(sentence, possible_symbols)
            processed.append(processed_sentence)

        return processed
    
    @staticmethod
    def create_relation(entities):
        relation_list = []
        current_ci = None
        current_ci_id = None
        current_ci_idx = -1
        for i, entity in enumerate(entities):
            if entity['value']['labels'][0] == 'CI':
                current_ci = entity['value']['text']
                current_ci_id = entity['id']
                current_ci_idx = i
                continue
            if current_ci is None:
                continue
            if entity['value']['labels'][0] not in ['CI_R', 'CI_V', 'CI_M', 'CI_ABB', 'CI_U']:
                continue
            is_between = True
            for j in range(i, len(entities)):
                if entities[j]['value']['labels'][0] == 'CI' and j > current_ci_idx and j < i:
                    is_between = False
                    break
            if is_between:
                relation_dict ={
                    "from_id": current_ci_id,
                    "to_id": entity['id'],
                    "type": "relation",
                    "direction": "right",
                    "labels":[""]
                }
                relation_list.append(relation_dict)
        return relation_list

    def generate_erner_dataset(self,ner_datas: List[Dict]):
        erner_datasets = []
        for ner_data in ner_datas:
            annotations = ner_data['predictions'][0]["result"]
            annotations = merge_overlapping_annotations(annotations)
            text = ner_data['data']['text']
            if self.ci_num_in_data(annotations) > 3:
                splited_sentences = self.split_sentence(text, annotations)
                processed_splited_sentences = self.process_splited_sentence(splited_sentences)
                processed_data = {
                                "data": {
                                    "text": processed_splited_sentences[0]['text'],
                                    "original_text": processed_splited_sentences[0]['original_text'],
                                },
                                "annotations": [],
                                "predictions": [
                                    {
                                        "model_version": "INITIAL",
                                        "result":processed_splited_sentences[0]['annotations'],
                                    }
                                ]
                            }
                erner_datasets.append(processed_data)
        return erner_datasets
    
    def process_ner_lbl_std_data(self,file_path:str):
        """
        对ner原始文本进行排版处理
        :param file_path: str:ner原始文本文件路径
        :return: List[Dict]:处理后的ner数据
        """
        ner_datas_list = read_json(file_path)
        erner_datasets = self.generate_erner_dataset(ner_datas_list)
        return erner_datasets


if __name__ == '__main__':
    ner_label_studio_data_path = 'data/ocr_ner_deduplicated_txts_predict_lbl_std.json'
    ner_datas_list = read_json(ner_label_studio_data_path)
    generate_erner_datasets = GenerateErNerDatasets()
    
    # 对ner原始文本进行排版处理
    erner_datasets = generate_erner_datasets.process_ner_lbl_std_data(ner_datas_list)

    # 保存处理后的数据
    write_json(erner_datasets, 'data/erner_datasets_3_14_processed.json')
