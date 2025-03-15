# Author: caisongrui
# Created on: 2025/2/26 15:16
# Description: 

import os
from typing import List
from app.utility.file_opt import read_json, check_path, write_json
from test.test_process_overlop_label import merge_overlapping_annotations

mapping_relations = {
    'R': 'RANGE',
    'V': 'VALUE',
    'M': 'METHOD',
    'ABB': 'ABB',
    'U': 'UNIT'
}

def extract_relationships(data):
    # 首先构建一个 id 到实体信息的映射
    entities = {}
    relations = []
    for item in data:
        if item.get("type") == "labels":
            entity_id = item.get("id")
            value = item.get("value", {})
            entities[entity_id] = {
                "entity": value.get("text"),
                "start_idx": value.get("start"),
                "end_idx": value.get("end"),
                "category": value.get("labels", [])[0]
            }

        elif item.get("type") == "relation":
            relations.append(item)

    spo_list = []
    # 记录每个 CI 指向的目标实体（非 ABB），格式为 { CI_id: [ {target_id, predicate}, ... ] }
    ci_targets = {}
    # 记录 CI 指向的 ABB 的映射（注意关系方向为 CI -> ABB）
    ci_to_abb = {}

    # 遍历原始关系生成 spo，同时记录上述映射
    for rel in relations:
        subject_id = rel.get("from_id")
        object_id = rel.get("to_id")
        subject_entity = entities.get(subject_id)
        object_entity = entities.get(object_id)
        if not (subject_entity and object_entity):
            continue
        # 计算谓词：若两实体类别相同，直接用 "CONNECT"
        if subject_entity["category"] == object_entity["category"]:
            predicate = "CONNECT"
        else:
            if subject_entity['category'] == 'CI':
                predicate = mapping_relations[object_entity['category'].split('_')[1]]
            else:
                predicate = mapping_relations[subject_entity['category'].split('_')[1]]
        # 记录原始关系
        spo = {
            "subject": subject_entity["entity"],
            "subject_offset": (subject_entity["start_idx"], subject_entity["end_idx"]),
            "predicate": predicate,
            "object": object_entity["entity"],
            "object_offset": (object_entity["start_idx"], object_entity["end_idx"])
        }
        spo_list.append(spo)

        # 当 CI 指向某个实体时，做对应记录
        if subject_entity["category"] == "CI":
            # 如果目标实体类别为 ABB，则记录 CI->ABB 映射
            if object_entity["category"] == "ABB":
                ci_to_abb[subject_id] = object_id
            else:
                # 否则记录 CI 指向的目标（非 ABB）
                if subject_id not in ci_targets:
                    ci_targets[subject_id] = []
                ci_targets[subject_id].append({"target_id": object_id, "predicate": predicate})

    # 根据每个 CI 的指向，若该 CI 指向了 ABB，则让 ABB 也指向该 CI 指向的其他目标实体
    for ci_id, targets in ci_targets.items():
        if ci_id in ci_to_abb:
            abb_id = ci_to_abb[ci_id]
            abb_entity = entities.get(abb_id)
            if not abb_entity:
                continue
            for target_info in targets:
                target_entity = entities.get(target_info["target_id"])
                if not target_entity:
                    continue
                # 新生成一条关系，主体为 ABB，谓词和目标与原关系保持一致
                spo_list.append({
                    "subject": abb_entity["entity"],
                    "subject_offset": (abb_entity["start_idx"], abb_entity["end_idx"]),
                    "predicate": target_info["predicate"],
                    "object": target_entity["entity"],
                    "object_offset": (target_entity["start_idx"], target_entity["end_idx"])
                })

    return spo_list


def title_ner_labelstudio_to_bio(result):
    full_text = result['data']['text']
    bio_annotations = ["O"] * len(full_text)
    annotations = result['annotations'][0]['result']
    # annotations.extend(result['annotations'][0]['prediction0']["result"])
    # 检查并处理重叠标注
    annotations = merge_overlapping_annotations(annotations)
    for annotation in annotations:
        if annotation.get("type") != "labels":
            continue
        text = annotation["value"]["text"]
        if not text:
            continue
        label = annotation["value"]["labels"][0]
        start_idx = annotation['value']["start"]
        end_idx = annotation['value']["end"]
        try:
            if any(bio_annotations[idx] != "O" for idx in range(start_idx, end_idx)):
                continue
            for idx in range(start_idx, end_idx):
                if idx == start_idx:
                    bio_annotations[idx] = f"B-{label}"
                else:
                    bio_annotations[idx] = f"I-{label}"
        except IndexError:
            print(f"Error: Index out of range for text '{text}',full_text:{full_text}")
    final_annotations = []
    for idx, char in enumerate(bio_annotations):
        final_annotations.append(f"{bio_annotations[idx]}")
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
    output_path = '../../data/erner-data/erner_ci_0310_train_plus.json'
    labelstudio_result = read_json("../../data/project-174-at-2025-03-10-01-06-71e25a5c.json")
    erner_results = []
    for annotation in labelstudio_result:
        bio_result = title_ner_labelstudio_to_bio(annotation)
        spo_result = extract_relationships(annotation['annotations'][0]['result'])
        erner_result = {
            "text": annotation['data']['text'],
            "bio_list": bio_result,
            "spo_list": spo_result
        }
        erner_results.append(erner_result)
    write_json(erner_results, output_path)
