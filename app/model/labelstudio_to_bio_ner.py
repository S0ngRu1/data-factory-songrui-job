# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/12 09:06
# LAST MODIFIED ON:
# AIM:
import os
import re
from datetime import datetime
from typing import List

from numpy.random import choice


from app.utility.file_opt import read_json,check_path
from test.test_process_overlop_label import merge_overlapping_annotations

ocr_ner_label = []
chinese_label_mapping = {
    '病症':'Disease',
    '症状':'Symptom',
    '药品':'Medicine',
    '指标':'Index',
    '用法':'Usage',
    '手术':'Operation',
    '运动': 'Sport',
    '生活习惯': 'Lifestyle',
    '饮食': 'Diet'
}

ner_label_mapping = {
    'disease': 'Disease',
    'symptom': 'Symptom',
    'medicine': 'Medicine',
    'index': 'Index',
    'usage': 'Usage',
    'operation': 'Operation',
    'sport': 'Sport',
    'lifestyle': 'Lifestyle',
    'diet': 'Diet',
    'check': 'Index'
}

def title_ner_labelstudio_to_bio(result):
    full_text = result['data']['text']
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]['result']
    # annotations.extend(result['annotations'][0]['prediction0']["result"])

    # 检查并处理重叠标注
    annotations = merge_overlapping_annotations(annotations)

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
    return final_annotations

def chd_handbook_label_to_bio_ner(result):
    full_text = result['data']['text']
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]["result"]
    annotations = merge_overlapping_annotations(annotations)

    for annotation in annotations:
        text = annotation["value"]["text"]
        if not text:
            continue
        if  annotation["value"]["labels"][0] not in chinese_label_mapping:
            continue
        label = chinese_label_mapping[annotation["value"]["labels"][0]]
        if label != "OTHER":
            start_idx = 0
            while start_idx < len(full_text):
                start_idx = full_text.find(text, start_idx)
                if start_idx == -1:
                    break
                for idx in range(len(text)):
                    if idx == 0:
                        bio_annotations[start_idx + idx] = f"B-{label}"
                    else:
                        bio_annotations[start_idx + idx] = f"I-{label}"
                start_idx += len(text)

    final_annotations = []
    for idx, char in enumerate(full_text):
        final_annotations.append(f"{char}\t{bio_annotations[idx]}")
    return final_annotations

def ner_attention_labelstudio_to_bio(result):
    full_text = result['data']['current_text'].split(':')[1]
    final_annotations = []
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]["result"]
    filtered_annotations = [annotation for annotation in annotations if annotation['type'] != 'choices']
    if filtered_annotations:
        annotations = merge_overlapping_annotations(filtered_annotations)
        for annotation in annotations:
            text = annotation["value"]["text"]
            if not text:
                continue
            label = ner_label_mapping[annotation["value"]["labels"][0]]
            if label == 'check':
                label = 'Index'
            if label != "OTHER":
                start_idx = 0
                while start_idx < len(full_text):
                    start_idx = full_text.find(text, start_idx)
                    if start_idx == -1:
                        break
                    for idx in range(len(text)):
                        if idx == 0:
                            bio_annotations[start_idx + idx] = f"B-{label}"
                        else:
                            bio_annotations[start_idx + idx] = f"I-{label}"
                    start_idx += len(text)

        for idx, char in enumerate(full_text):
            final_annotations.append(f"{char}\t{bio_annotations[idx]}")
    return final_annotations

def ner_labelstudio_to_bio(result):
    full_text = result['data']['record_text']
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]["result"]
    annotations.extend(result['annotations'][0]['prediction']["result"])
    # 检查并处理重叠标注
    annotations = merge_overlapping_annotations(annotations)

    for annotation in annotations:
        text = annotation["value"]["text"]
        if not text:
            continue
        label = ner_label_mapping[annotation["value"]["labels"][0]]
        if label == 'check':
            label = 'Index'
        if label != "OTHER":
            start_idx = 0
            while start_idx < len(full_text):
                start_idx = full_text.find(text, start_idx)
                if start_idx == -1:
                    break
                for idx in range(len(text)):
                    if idx == 0:
                        bio_annotations[start_idx + idx] = f"B-{label}"
                    else:
                        bio_annotations[start_idx + idx] = f"I-{label}"
                start_idx += len(text)

    final_annotations = []
    for idx, char in enumerate(full_text):
        final_annotations.append(f"{char}\t{bio_annotations[idx]}")
    return final_annotations

def conv_ner_labelstudio_to_bio(result):
    full_text = result['data']['text']
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]["result"]
    # annotations.extend(result['annotations'][0]['prediction']["result"])
    # 检查并处理重叠标注
    annotations = merge_overlapping_annotations(annotations)

    for annotation in annotations:
        text = annotation["value"]["text"]
        if not text:
            continue
        label = annotation["value"]["labels"][0]
        if label == 'Check':
            label = 'Index'
        if label != "OTHER":
            start_idx = 0
            while start_idx < len(full_text):
                start_idx = full_text.find(text, start_idx)
                if start_idx == -1:
                    break
                for idx in range(len(text)):
                    if idx == 0:
                        bio_annotations[start_idx + idx] = f"B-{label}"
                    else:
                        bio_annotations[start_idx + idx] = f"I-{label}"
                start_idx += len(text)

    final_annotations = []
    for idx, char in enumerate(full_text):
        final_annotations.append(f"{char}\t{bio_annotations[idx]}")
    return final_annotations

def isnot_have_label(result)->bool:
    annotations = result['annotations'][0]["result"]
    if len(annotations) == 0:
        return True

def isnot_have_CI(result)->bool:
    annotations = result['predictions'][0]["result"]
    labels = set()
    for annotation in annotations:
        labels.update(annotation['value']['labels'])
    for label in labels:
        if 'CI' in label:
            return False
    return True


def is_have_usage(result)->bool:
    annotations = result['annotations'][0]["result"]
    labels = set()
    for annotation in annotations:
        if annotation['type'] == 'relation':
            continue
        labels.update(annotation['value']['labels'])
    for label in labels:
        if '用法' in label:
            return True
    return False

def filter_by_time(result)->bool:
    update_time = result["updated_at"]
    matched = re.match(r'(\d{4}-\d{2}-\d{2})', update_time)

    if matched:
        update_time_str = matched.group(1)

        # 将字符串转为 datetime 对象
        update_date = datetime.strptime(update_time_str, '%Y-%m-%d')
        cutoff_date = datetime(2024, 11, 5)
        if update_date > cutoff_date:
            return True
        else:
            return False
    else:
        return False

def process_bio_ocr_ner(results:List):
    first_ci_index,last_ci_index = 0,len(results)-1
    # 过滤掉所有非实体且非特殊字符的标签
    for i,result in enumerate(results):
        parts = result.split("\t")
        if len(parts) < 2:
            continue
        if 'CI' in parts[1] :
            first_ci_index = i
            break
    for i,result in enumerate(results[::-1]):
        parts = result.split("\t")
        if len(parts) < 2:
            continue
        if 'CI' in parts[1] :
            last_ci_index = len(results)-i
            break

    return results[first_ci_index:last_ci_index]


if __name__ == '__main__':
    output_dir = '../../data/BIO_ner_25115_conv_12_top400'
    check_path(output_dir)
    labelstudio_result = read_json("../../data/talk_ner_115_top400.json")

    for annotation in labelstudio_result:
        filepath = os.path.join(output_dir, str(annotation['id']) + '.txt')
        if isnot_have_label(annotation):
            continue
        # if is_have_usage(annotation):
        #     continue
        # if filter_by_time(annotation):
        bio_result = conv_ner_labelstudio_to_bio(annotation)
        # processed_bio_result = process_bio_ocr_ner(bio_result)
        if len(bio_result)>0:
            with open(filepath, 'w', encoding='utf-8') as file:
                for item in bio_result:
                    file.write(item+ '\n')
