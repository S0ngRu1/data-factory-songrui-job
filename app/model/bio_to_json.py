# Author: caisongrui
# Created on: 2024/12/25 15:09
# Description:
import json
import os
from typing import List, Set, Tuple


# 处理BIO格式数据的函数
def bio_to_entities(lines):
    sentence = []
    entities = []
    current_entity = None

    for line in lines:
        if len(line.split())<=1:
            continue
        word, label = line.split()
        # 记录句子中的每个单词
        sentence.append(word)
        if label.startswith('B-'):  # 如果是实体的开始
            if current_entity:
                # 之前的实体也应该加到结果中
                entities.append(current_entity)
            current_entity = {"entity": word, "category": label[2:]}  # 初始化新的实体
        elif label.startswith('I-'):  # 如果是实体的内部
            if current_entity:
                current_entity["entity"] += word  # 继续添加到当前实体
        elif label == 'O' and current_entity:  # 实体结束
            if current_entity:
                entities.append(current_entity)
                current_entity = None

    # 最后一组实体如果存在，需要加到结果中
    if current_entity:
        entities.append(current_entity)

    # 拼接句子
    text = ''.join(sentence)

    return {"text": text, "entities": entities}
def _get_all_files(bio_dir_path):
    files = []
    seen_files = set()
    for root, dirs, filenames in os.walk(bio_dir_path):
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(root, filename)
                if filename not in seen_files:
                    files.append(file_path)
                    seen_files.add(filename)
    return files
if __name__ == '__main__':
    results = []
    bio_dir_path = "../../data/BIO_NER_1220/val"
    bio_files = _get_all_files(bio_dir_path)
    for bio_path in bio_files:

        with open(bio_path, "r", encoding="utf-8") as f:
            bio_data = f.readlines()
        extracted_data = bio_to_entities(bio_data)
        results.append(extracted_data)
    with open("../../data/BIO_NER_1220/BIO_NER_1220_val.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)