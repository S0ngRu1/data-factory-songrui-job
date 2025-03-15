# -*- coding: utf-8 -*-
# @Time : 11/10/24 9:14 PM
# @Author : CSR
# @File : test_overlop_labels.py

import unittest


def merge_overlapping_annotations(annotations):
    # 过滤掉不包含 'value' 或其中没有 'start' 或 'end' 字段的注释
    annotations = [ann for ann in annotations if 'value' in ann and 'start' in ann['value'] and 'end' in ann['value']]
    # 按照 value['start'] 字段对 annotations 进行排序
    annotations.sort(key=lambda x: x['value']['start'])
    merged_annotations = []
    if not annotations:
        return merged_annotations  # 如果过滤后为空，直接返回
    current = annotations[0]['value']
    for i in range(1, len(annotations)):
        next_annotation = annotations[i]['value']
        # 判断当前注释和下一个注释是否有重叠或包含关系
        if next_annotation['start'] < current['end']:
            # 计算重叠并集
            current = {
                'start': min(current['start'], next_annotation['start']),
                'end': max(current['end'], next_annotation['end']),
                'text': current['text'] + next_annotation['text'][current['end'] - next_annotation['start']:],
                'labels': current['labels'] if len(current['text']) >= len(next_annotation['text']) else next_annotation['labels']
            }
        else:
            # 如果没有重叠，将当前注释添加到结果中，并更新当前注释为下一个注释
            merged_annotations.append({
                'from_name': annotations[i - 1]['from_name'],
                'to_name': annotations[i - 1]['to_name'],
                'type': annotations[i - 1]['type'],
                'value': current
            })
            current = next_annotation

    # 将最后一个注释添加到结果中
    merged_annotations.append({
        'from_name': annotations[-1]['from_name'],
        'to_name': annotations[-1]['to_name'],
        'type': annotations[-1]['type'],
        'value': current
    })

    return merged_annotations


class TestProcessOverlopLabel(unittest.TestCase):

    def test_process_overlop_label(self):
        # 左端冲突
        # 腿上有一些淤青  腿上有一些淤青， 淤青
        annotations = [{'from_name': 'label', 'id': 'vgFv40YNmD', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 10, 'labels': ['symptom'], 'start': 3, 'text': '腿上有一些淤青'}}, {'from_name': 'label', 'id': 'YBRpfVxkbL', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 10, 'labels': ['symptom'], 'start': 8, 'text': '淤青'}}, {'from_name': 'label', 'id': '1VTh1zuTra', 'origin': 'prediction', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 17, 'text': '提不起气十几秒'}}]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label2(self):
        # 左端冲突
        # 脚上溃烂   脚上溃烂，溃烂
        annotations = [{'from_name': 'label', 'id': '6F7CIEMpA_', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 5, 'labels': ['symptom'], 'start': 1, 'text': '脚上溃烂'}}, {'from_name': 'label', 'id': 'gHD6IXsgEJ', 'origin': 'prediction', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 5, 'labels': ['symptom'], 'start': 3, 'text': '溃烂'}}]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label3(self):
        # 无重叠
        annotations = [{'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}}, {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 15, 'labels': ['symptom'], 'start': 13, 'text': '心累'}}, {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}}]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label4(self):
        # 右端冲突
        # 水肿一块   水肿， 水肿一块
        annotations = [{'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}}, {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 15, 'labels': ['symptom'], 'start': 11, 'text': '水肿一块'}}, {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text', 'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}}]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label5(self):
        # 包含
        # 脾气毛躁火大   脾气毛躁火大， 毛躁
        annotations = [
            {'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}},
            {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 26, 'labels': ['symptom'], 'start': 20, 'text': '脾气毛躁火大'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}}]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label6(self):
        # 包含
        # 脾气毛躁火大   脾气毛躁火大， 毛躁, 火大
        annotations = [
            {'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}},
            {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 26, 'labels': ['symptom'], 'start': 20, 'text': '脾气毛躁火大'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 26, 'labels': ['symptom'], 'start': 24, 'text': '火大'}}
        ]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label9(self):
        # 包含
        # 脾气毛躁火大   脾气毛躁火大，气毛， 毛躁, 火大
        annotations = [
            {'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}},
            {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 26, 'labels': ['symptom'], 'start': 20, 'text': '脾气毛躁火大'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 22, 'labels': ['symptom'], 'start': 21, 'text': '气毛'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 23, 'text': '毛躁'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 26, 'labels': ['symptom'], 'start': 25, 'text': '火大'}}
        ]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label7(self):
        # 包含
        # 脾气毛躁火大得出血  脾气毛躁火大， 毛躁, 火大得出血
        annotations = [
            {'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}},
            {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 26, 'labels': ['symptom'], 'start': 20, 'text': '脾气毛躁火大'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 29, 'labels': ['symptom'], 'start': 24, 'text': '火大得出血'}}
        ]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)

    def test_process_overlop_label8(self):
        # 包含 labels冲突
        # 脾气毛躁火大得出血  脾气毛躁火大， 毛躁, 火大得出血
        annotations = [
            {'from_name': 'label', 'id': '7Qoa7-IE6J', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 13, 'labels': ['symptom'], 'start': 11, 'text': '水肿'}},
            {'from_name': 'label', 'id': '4thk2hUkmU', 'origin': 'manual', 'to_name': 'record_text', 'type': 'labels',
             'value': {'end': 26, 'labels': ['disease'], 'start': 20, 'text': '脾气毛躁火大'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 24, 'labels': ['symptom'], 'start': 22, 'text': '毛躁'}},
            {'from_name': 'label', 'id': 'D7LCwQBAEU', 'origin': 'prediction', 'to_name': 'record_text',
             'type': 'labels', 'value': {'end': 29, 'labels': ['symptom'], 'start': 24, 'text': '火大得出血了了了了了'}}
        ]
        old_annotations = [item['value'] for item in annotations]
        print(old_annotations)
        annotations = merge_overlapping_annotations(annotations)
        new_annotations = [item['value'] for item in annotations]
        print(new_annotations)