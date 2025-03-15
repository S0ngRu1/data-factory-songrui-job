# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/10 15:03
# LAST MODIFIED ON:
# AIM:
import re
import signal
import sys
import logging
import requests
import json
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from app.utility.file_opt import check_path, read_json

DATA_SERVER_URL = "http://192.168.110.37:8000/20241111/"
NER_SERVER_URL = "http://192.168.110.196:10082/api/doc-ner"
HEADERS = {"Content-Type": "application/json"}

PROGRESS_FILE = "progress_1120_new.txt"
SAVE_FILE = "../../data/results_labelstudio_1120_new"
lock = threading.Lock()

logging.basicConfig(
    filename='process_error_1120_new.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_file_list(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    file_list = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.json')]
    # missing_files = []
    # result_dir = '../../data/results_labelstudio_1106'
    # for file_name in file_list:
    #     file_path = os.path.join(result_dir, file_name)
    #     if not os.path.exists(file_path) and not os.path.exists(os.path.join(result_dir, file_name.replace('.jpg', ''))):
    #         missing_files.append(file_name)
    return file_list


def read_error_log():
    files_index = []
    with open('process_error_1111_new.log', "r") as f:
        lines = f.readlines()
        for line in lines:
            if "Error occurred while processing file" in line:
                match = re.search(r"file (\d+):", line)
                if match:
                    file_index = match.group(1)
                    files_index.append(file_index)
    return files_index


class DataProcessor:
    def __init__(self, data_server_url, ner_server_url, progress_file, save_file, headers):
        self.data_server_url = data_server_url
        self.ner_server_url = ner_server_url
        self.progress_file = progress_file
        self.save_file = save_file
        self.headers = headers
        self.final_index = 0
        self.exit_flag = False

    @staticmethod
    def dict_to_labelstudio(input_dict,filename):
        format_dict = {
            "data": {
                "text": input_dict['content'],
                "url": os.path.splitext(filename)[0]
            },
            "annotations": []
        }
        format_annot_dict = {
            "result": []
        }
        # 确保 `labels` 和 `offsets` 是有效的
        if 'labels' not in input_dict or 'offsets' not in input_dict:
            return format_dict

        for labels, offsets in zip(input_dict['labels'], input_dict['offsets']):
            annotation = {
                "value": {
                    "start": offsets[0],
                    "end": offsets[1],
                    "text": input_dict['content'][offsets[0]:offsets[1]],
                    "labels": [labels]
                },
                "from_name": "label",
                "to_name": "text",
                "type": "labels"
            }
            format_annot_dict["result"].append(annotation)
        format_dict["annotations"].append(format_annot_dict)
        return format_dict

    def get_current_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r") as f:
                return int(f.read().strip())
        return 0

    def save_progress(self, progress):
        with open(self.progress_file, "w") as f:
            f.write(str(progress))

    def read_file_content(self, file_name):
        url = f"{self.data_server_url}{file_name}"
        response = requests.get(url)
        response.raise_for_status()
        json_dict = json.loads(response.content.decode('utf-8'))  # 先解码为字符串，再转为 JSON
        return json_dict

    def process_data(self, data,file_name):
        payload = json.dumps(data, ensure_ascii=False)
        response = requests.request("POST", self.ner_server_url, headers=self.headers, data=payload)
        result_labelstudio = self.dict_to_labelstudio(ast.literal_eval(response.text)['data'],file_name)
        return result_labelstudio

    def read_files_stream(self, file_list, start_index=0):
        file_name = file_list[start_index]
        file_content = self.read_file_content(file_name)
        return  {"content":file_content['data']}, file_name

    def save_result(self,result, file_name):
        check_path(self.save_file)
        file_path = os.path.join(self.save_file, f'{file_name}')

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)

    def run_single(self, file_list, index):
        if self.exit_flag:
            return self.final_index
        try:
            file_content, file_name = self.read_files_stream(file_list, start_index=index)
            result = self.process_data(file_content,file_name)
            self.save_result(result, file_name)
            with lock:
                self.final_index = index + 1
        except Exception as e:
            logging.error(f"Error occurred while processing file {index}: {e}")
        return self.final_index

    def run(self):
        self.final_index = self.get_current_progress()
        file_list = get_file_list(self.data_server_url)
        error_files_index = read_error_log()
        for file_index in error_files_index:
            file_name = file_list[int(file_index)]
            file_content = self.read_file_content(file_name)
            file_content = {"content": file_content['data']}
        # for file_content, file_name in tqdm(self.read_files_stream(file_list, start_index=self.final_index),
        #                                     initial=self.final_index, total=len(file_list)):
            result = self.process_data(file_content,file_name)
            self.final_index += 1
            self.save_progress(self.final_index)
            # self.save_result(result, file_index)
            self.save_result(result, file_name)

    def run_v2(self):
        self.final_index = self.get_current_progress()
        file_list = get_file_list(self.data_server_url)
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(self.run_single, file_list, index): index for index in
                       range(self.final_index, len(file_list))}

            for future in tqdm(as_completed(futures), total=len(futures)):
                if self.exit_flag:  # 检查退出标志
                    print("检测到退出标志，停止处理")
                    break
                index = futures[future]
                try:
                    future.result()  # Get the result from the future
                except Exception as e:
                    logging.error(f"Error occurred while processing file {index}: {e}")
        self.save_progress(self.final_index)

    def save_on_exit(self, signum, frame):
        """在程序终止时保存进度和结果"""
        self.exit_flag = True
        self.save_progress(self.final_index)
        print(f"程序被终止，最后处理的索引是 {self.final_index}")
        sys.exit(0)


if __name__ == "__main__":

    processor = DataProcessor(DATA_SERVER_URL, NER_SERVER_URL, PROGRESS_FILE, SAVE_FILE,HEADERS)

    signal.signal(signal.SIGINT, processor.save_on_exit)
    signal.signal(signal.SIGTERM, processor.save_on_exit)

    processor.run_v2()
    #用于处理异常
    # processor.run()