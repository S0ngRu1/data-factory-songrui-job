# Author: caisongrui
# Created on: 2025/3/11 10:19
# Description:
import collections
import os
import time

from ssl import SSLError
from loguru import logger

import requests
from requests import RequestException
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.utility.file_opt import read_json, write_json


def is_chinese(text):
    # 检查字符串是否包含中文字符
    return any('\u4e00' <= char <= '\u9fff' for char in text)


def translate_keywords(keyword):
    API_KEY = "03a6ad5abd674037895d0f07c655a90c"
    ENDPOINT = "https://hrt-test-gpt.openai.azure.com/openai/deployments/gpt-35-16/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    text = f'''我将传入一个中文词，帮我翻译成英文，要求采用蛇形命名法，返回一个字符串，不要返回其他内容。
    中文词:
    {keyword}
    '''

    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    # Send request
    retries = 0
    while retries < 5:
        try:
            # 发送 POST 请求
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()  # 检查HTTP响应是否成功

            # 解析返回的 JSON 内容
            return response.json()['choices'][0]['message']['content']

        except (SSLError, ConnectionError) as e:
            print(f"Request failed with error: {e}. Retrying {retries + 1}/{5}...")
            retries += 1
            time.sleep(1)  # 延迟一段时间再重试

        except RequestException as e:
            print(f"Request failed with error: {e}.")
            retries += 1
            continue
        except Exception as e:
            print(f"Process failed with error: {e}.")
            retries += 1
            continue

    print("Max retries exceeded, skipping this request.")
    return None  # 如果请求失败或重试次数超限，返回None


if __name__ == '__main__':
    dir_path = "/Users/caisongrui/Workspace/data-factory/cangjie_keywords/"
    file_list = os.listdir(dir_path)
    ## translate json files
    # for file in file_list:
    #     if file.endswith(".raw"):
    #         continue
    #     logger.info(f'processing {file}')
    #     translated_data = {}
    #     file_path = os.path.join(dir_path, file)
    #     items = read_json(file_path)
    #     for item in tqdm(items):
    #         item_keyword = item['keyword']
    #         item_id = str(item['id'])
    #         if item_keyword is None:
    #             translated_data[item_id] = item_keyword
    #             continue
    #         if is_chinese(item_keyword):
    #             # translated_data[item_keyword] = translated_result[item_id]
    #             item_keyword = translate_keywords(item_keyword)
    #         # translated_data[item_id] = item_keyword
    #     output_path = os.path.join("../../cangjie_keywords", file.split(".")[0]+"_translated_processed.json")
    #     write_json(translated_data, output_path)
    #     logger.info(f'write complete: {output_path}')

    ## translate raw files
    translated_data = {}
    for file in file_list:
        if file.endswith(".raw"):
            logger.info(f'processing {file}')
            
            file_path = os.path.join(dir_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                items = f.readlines()

            for item in tqdm(items):
                # 去除item中的换行符和所有的‘-’
                process_item = item.strip().replace('-', '')
                if process_item is None:
                    continue
                if is_chinese(process_item):
                    # translated_data[item_keyword] = translated_result[item_id]
                    translated_item = translate_keywords(process_item)
                else:
                    translated_item = process_item
                translated_data[process_item] = translated_item
    output_path = os.path.join("/Users/caisongrui/Workspace/data-factory/cangjie_keywords", "raw_file_translated.json")
    write_json(translated_data, output_path)
    logger.info(f'write complete: {output_path}')

    ## process
    # for file in file_list:
    #     if file.endswith("_translated_processed.json") or file.endswith("_translated.json"):
    #         continue
    #     translated_result = read_json(os.path.join(dir_path, file.split(".")[0] + "_translated_processed.json"))
    #     logger.info(f'processing {file}')
    #     file_path = os.path.join(dir_path, file)
    #     items = read_json(file_path)
    #     for item in tqdm(items):
    #         item_keyword = item['keyword']
    #         item['en_keyword'] = translated_result.get(item_keyword, item_keyword)
    #     output_path = os.path.join("../../cangjie_keywords", file.split(".")[0] + "_add_en_keyword.json")
    #     write_json(items, output_path)
    #     logger.info(f'write complete: {output_path}')