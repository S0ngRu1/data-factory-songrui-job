# Author: caisongrui
# Created on: 2024/12/24 09:47
# Description:
import os

import jieba
from tqdm import tqdm


def get_text_from_file(file_path):
    text = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip():
            parts = line.split()
            if len(parts) < 2:
                continue
            x = parts[0].strip()
            text.append(x)
    return ''.join(text)



def generate_bies_datasets(bio_dataset_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for filename in tqdm(os.listdir(bio_dataset_path)):
        if filename.endswith('.txt'):
            file_path = os.path.join(bio_dataset_path, filename)
            text = get_text_from_file(file_path)
            seg_list = jieba.cut(text, cut_all=False)
            seg_result = list(seg_list)
            bies_result = convert_to_bies(seg_result)
            with open(os.path.join(out_dir, filename), 'w', encoding='utf-8') as f:
                for word, label in bies_result:
                    f.write(f"{word}\t{label}\n")


def convert_to_bies(seg_result):
    bies_result = []
    for word in seg_result:
        # 对于单字词，标记为 S
        if len(word) == 1:
            bies_result.append((word, 'S'))
        else:
            # 对于多字词，标记开始为 B，结束为 E，中间为 I
            bies_result.append((word[0], 'B'))
            for i in range(1, len(word) - 1):
                bies_result.append((word[i], 'I'))
            bies_result.append((word[-1], 'E'))
    return bies_result


if __name__ == '__main__':
    bio_dataset_path = '../data/BIO_NER_1220'
    out_dir = '../data/Segment_1220'
    generate_bies_datasets(bio_dataset_path, out_dir)
