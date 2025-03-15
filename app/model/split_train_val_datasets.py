# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/15 20:03
# LAST MODIFIED ON:
# AIM:

import os
import shutil
import random
from typing import List


def process_file_labels(file_path, ner_labels):
    """
    处理文件并返回该文件中出现的标签集合。
    """
    labels_in_file = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) > 1:
                label = parts[1].strip()
                if label in ner_labels:
                    labels_in_file.add(label)
    return labels_in_file

def split_dataset(source_dir: str, train_dir: str, val_dir: str, ner_labels: List[str], train_ratio=0.8):
    # 创建训练集和验证集的目录
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # 获取源目录中的所有文件并打乱
    all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    print(f"文件总数:{len(all_files)}")
    random.shuffle(all_files)

    # 划分训练集和验证集
    split_index = int(len(all_files) * train_ratio)
    train_files = all_files[:split_index]
    val_files = all_files[split_index:]

    # 初始化每个标签的目录
    label_counts = {label: {'train': 0, 'val': 0} for label in ner_labels}
    for label in ner_labels:
        os.makedirs(os.path.join(train_dir, label), exist_ok=True)
        os.makedirs(os.path.join(val_dir, label), exist_ok=True)

    # 处理文件分配
    for filename, dataset_type in zip(train_files + val_files, ['train'] * len(train_files) + ['val'] * len(val_files)):
        file_path = os.path.join(source_dir, filename)
        labels_in_file = process_file_labels(file_path, ner_labels)

        # 将文件复制到相应的目录中
        for label in labels_in_file:
            target_dir = train_dir if dataset_type == 'train' else val_dir
            shutil.copy(file_path, os.path.join(target_dir, label, filename))
            label_counts[label][dataset_type] += 1

    for label, counts in label_counts.items():
        print(f"标签 '{label}': 训练集文件数: {counts['train']}, 验证集文件数: {counts['val']}")

def generate_test_dataset(source_dir: str, test_dir: str, ner_labels: List[str]):
    # 创建测试集的目录
    os.makedirs(test_dir, exist_ok=True)
    test_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    # 初始化每个标签的目录
    label_counts = {label: {'test': 0} for label in ner_labels}
    for label in ner_labels:
        os.makedirs(os.path.join(test_dir, label), exist_ok=True)

    for filename, dataset_type in zip(test_files, ['test'] * len(test_files)):
        file_path = os.path.join(source_dir, filename)
        labels_in_file = process_file_labels(file_path, ner_labels)

        for label in labels_in_file:
            shutil.copy(file_path, os.path.join(test_dir, label, filename))
            label_counts[label][dataset_type] += 1

    for label, counts in label_counts.items():
        print(f"标签 '{label}': 测试集文件数: {counts['test']}")


if __name__ == '__main__':
    ner_labels = ['O', 'B-Disease', 'I-Disease', 'B-Symptom', 'I-Symptom',
                  'B-Medicine', 'I-Medicine', 'B-Diet', 'I-Diet',
                  'B-Index', 'I-Index', 'B-Sport', 'I-Sport',
                  'B-Operation', 'I-Operation', 'B-Lifestyle', 'I-Lifestyle', 'B-Usage', 'I-Usage']
    seg_labels = ['B', 'I', 'S', 'E']
    ocr_ner_labels = ['O', 'B-CI', 'B-CI_R', 'B-CI_V', 'B-CI_ABB', 'B-CI_U', 'B-CI_M', 'B-HD', 'B-HN', 'B-PI', 'B-TI',
                      'I-CI', 'I-CI_R', 'I-CI_V', 'I-CI_ABB', 'I-CI_U', 'I-CI_M', 'I-HD', 'I-HN', 'I-PI', 'I-TI']

    split_dataset('../../data/BIO_ner_25115_conv_12_top400_split', '../../data/BIO_ner_25115_conv_12_top400_split/train',
                  '../../data/BIO_ner_25115_conv_12_top400_split/val', ner_labels)
    # generate_test_dataset('../../data/BIO_ner_1107_test', '../../data/BIO_ner_1106/test', ner_labels)