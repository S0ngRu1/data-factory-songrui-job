# -*- coding: utf-8 -*-
# Author: caisongrui
# Date: 2025-03-14
# Description: Description of the file


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


def main():
    pass

if __name__ == '__main__':
    main()