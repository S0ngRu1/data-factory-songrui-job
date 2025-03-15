# Author: caisongrui
# Created on: 2024/11/25 16:13
# Description:
# -*- coding: utf-8 -*-
# @Time : 11/9/24 1:58 PM
# @Author : CSR
# @File : process_dataset.py

import json
import os

# 读取 JSON 数据集文件
input_file = '../data/CMeEE-V2/CMeEE-V2_dev.json'  # 将文件路径替换为你的 JSON 文件路径
output_dir = '../data/CMeEE-V2/val'
os.makedirs(output_dir, exist_ok=True)


def convert_to_bio(text, entities):
    bio_format = []
    text_chars = list(text)  # 将文本逐字符拆分

    # 初始化每个字符的标签为 'O'
    labels = ['O'] * len(text_chars)

    # 处理每个实体并标注 BIO 格式
    for entity in entities:
        start_idx = entity['start_idx']
        end_idx = entity['end_idx']
        entity_type = entity['type']

        # 标注首字为 'B-type'，其余字为 'I-type'
        labels[start_idx] = f'B-{entity_type}'
        for i in range(start_idx + 1, end_idx):
            labels[i] = f'I-{entity_type}'

    # 将字符和标签拼接为 BIO 格式
    for char, label in zip(text_chars, labels):
        bio_format.append(f"{char} {label}")

    return '\n'.join(bio_format)


# 读取 JSON 并转换为 BIO 格式
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 将每条数据转换并保存为单独的 TXT 文件
for i, item in enumerate(data):
    text = item['text']
    entities = item['entities']
    bio_content = convert_to_bio(text, entities)

    output_file = os.path.join(output_dir, f'sample_{i + 1}.txt')
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(bio_content)

print("转换完成，每条数据已单独存为 TXT 文件。")