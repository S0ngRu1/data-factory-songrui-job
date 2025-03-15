# Author: caisongrui
# Created on: 2025/3/3 16:16
# Description:
import os
import re

import pandas as pd
from pyparsing import empty
from tqdm import tqdm

from app.utility.file_opt import read_json


def process_extracted_user_hn(dir_path:str):
    user_datas = {}
    user_ids = os.listdir(dir_path)
    for user_id_path in tqdm(user_ids):
        user_data_path = os.path.join(dir_path, user_id_path)
        user_data = read_json(user_data_path)
        user_datas.setdefault(user_data['user_id'],{}).update({'check_up_info': user_data['check_up_info'],'empty_txts': user_data['empty_txts']})
    return user_datas

def save_user_hn_data_to_excel(user_datas: dict, out_path: str):
    data_list = []
    empty_txts_list = []
    for user_id, user_info in user_datas.items():
        row = {
            '患者id': user_id,
            '复查情况': user_info.get('check_up_info', '')
        }
        data_list.append(row)
        if user_info.get('empty_txts', []):
            empty_txts_list.append({
                '患者id': user_id,
                'user_url': user_info.get('empty_txts', [])
            })

    df = pd.DataFrame(data_list)
    df.to_excel(out_path, index=False)
    df = pd.DataFrame(empty_txts_list)
    df.to_excel(out_path.replace('.xlsx', '_empty_txts.xlsx'), index=False)
    print('Save user check_up_info data to Excel success.')

def process_review(review_str):
    """处理单个复查记录，合并相似医院名称"""
    # 匹配日期和后续内容
    date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})\s*(.*)')
    match = date_pattern.match(review_str.strip())
    if not match:
        return review_str.strip()  # 无法解析时返回原字符串

    date, hospitals_part = match.groups()
    hospitals = hospitals_part.split()

    if not hospitals:
        return date  # 无医院名称时仅返回日期

    # 选择最长的医院名称
    merged_hospital = max(hospitals, key=lambda x: len(x))
    return f"{date} {merged_hospital}"


def process_review_cell(cell_content):
    """处理整个单元格的复查情况"""
    if pd.isna(cell_content) or not cell_content.strip():
        return cell_content

    reviews = cell_content.split('&')
    processed_reviews = []

    for review in reviews:
        processed = process_review(review)
        processed_reviews.append(processed)

    return ' & '.join(processed_reviews)



if __name__ == '__main__':
    # dir_path = '../../data/users_hn_output'
    # out_path = '../data/复查医院名称.xlsx'
    # user_datas = process_extracted_user_hn(dir_path)
    # save_user_hn_data_to_excel(user_datas, out_path)
    df = pd.read_excel('../data/复查医院名称.xlsx')
    df['复查情况'] = df['复查情况'].apply(process_review_cell)
    df.to_excel('../data/复查医院名称_处理后.xlsx', index=False)
