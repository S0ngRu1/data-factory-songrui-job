# Author: caisongrui
# Created on: 2024/11/20 10:45
# Description:
import os

def statistic_word_nums(dir_path: str) -> int:
    total_lines = 0  # 初始化总行数计数器

    for filename in os.listdir(dir_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(dir_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                for _ in f:
                    total_lines += 1

    return total_lines

def statistic_file_nums(dir_path: str) -> int:
    total_files = 0

    for filename in os.listdir(dir_path):
        if filename.endswith(".txt"):
            total_files += 1
    return total_files

if __name__ == '__main__':
    dataset_path = '../../data/BIO_ocr_ner_1127_split'
    print(f'总字数:{statistic_word_nums(dataset_path)}')
    print(f'文件数：{statistic_file_nums(dataset_path)}')