# Author: caisongrui
# Created on: 2024/11/20 11:31
# Description:
import os
from os.path import basename

from app.utility.file_opt import check_path


def split_ocr_ner_dateset(file_path: str,num_of_char:int,out_path:str):
    file_data = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        while len(lines) > num_of_char:
            split_index = -1
            for i in range(num_of_char, len(lines)):  # 从第450行开始往后查找
                if '[ENTER]' in lines[i]:
                    split_index = i
                    break

            if split_index == -1:  # 如果没有找到 [ENTER]，直接取前450行
                split_index = num_of_char

            file_data.append("".join(lines[:split_index + 1]).strip())
            lines = lines[split_index + 1:]
        if lines:
            file_data.append("".join(lines).strip())

    for idx, part in enumerate(file_data):
        new_filename = f"{basename(file_path).replace('.txt', '')}_part{idx + 1}.txt"
        new_filepath = f"{out_path}+{new_filename}"
        with open(new_filepath, "w", encoding="utf-8") as new_f:
            new_f.write(part)

def split_ner_dateset(file_path: str,num_of_char: int,out_path:str):
    file_data = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        while len(lines) > num_of_char:
            split_index = -1
            for i in range(num_of_char, len(lines)):  # 从第450行开始往后查找
                if any(sep in lines[i] for sep in ';；。'):
                    split_index = i
                    break

            if split_index == -1:  # 如果没有找到 [ENTER]，直接取前450行
                split_index = num_of_char

            file_data.append("".join(lines[:split_index + 1]).strip())
            lines = lines[split_index + 1:]
        if lines:
            file_data.append("".join(lines).strip())

    for idx, part in enumerate(file_data):
        new_filename = f"{basename(file_path).replace('.txt', '')}_part{idx + 1}.txt"
        new_filepath = f"{out_path}{new_filename}"
        with open(new_filepath, "w", encoding="utf-8") as new_f:
            new_f.write(part)

if __name__ == '__main__':
    ocr_ner_dateset_path = '../../data/BIO_ner_25115_conv_12_top400/'
    out_path = '../../data/BIO_ner_25115_conv_12_top400_split/'
    check_path(out_path)
    for file in os.listdir(ocr_ner_dateset_path):
        split_ner_dateset(ocr_ner_dateset_path + file,num_of_char = 300,out_path = out_path)