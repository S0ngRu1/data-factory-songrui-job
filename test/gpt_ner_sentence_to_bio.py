# Author: caisongrui
# Created on: 2025/1/2 15:31
# Description:
import os
from typing import List, Dict

from app.utility.file_opt import read_json, check_path


def get_entity_from_kg(kg_nodes:Dict,sentence:str):
    result = {}
    for node,cate in kg_nodes.items():
        if node in sentence:
            result[node] = cate
    return result

def gpt_ner_sentence_to_bio(sentence:str, kg_nodes:Dict)->List:
    """
    Convert a sentence into BIO format based on the knowledge graph nodes.
    """
    bio_annotations = ["O"] * len(sentence)
    annotations = get_entity_from_kg(kg_nodes,sentence)

    for text, label in annotations.items():
        if not text:
            continue
        if label:
            start_idx = 0
            while start_idx < len(sentence):
                start_idx = sentence.find(text, start_idx)
                if start_idx == -1:
                    break
                for idx in range(len(text)):
                    if bio_annotations[start_idx + idx] == "O":
                        if idx == 0:
                            bio_annotations[start_idx + idx] = f"B-{label}"
                        else:
                            bio_annotations[start_idx + idx] = f"I-{label}"
                start_idx += len(text)

    final_annotations = []
    for idx, char in enumerate(sentence):
        final_annotations.append(f"{char}\t{bio_annotations[idx]}")
    return final_annotations


if __name__ == '__main__':
    gpt_ner_path = 'patient_doctor_conversations.json'
    gpt_sentence = read_json(gpt_ner_path)
    out_put_dir = '../data/gpt_ner_sentence_to_bio'
    check_path(out_put_dir)
    kg_nodes = read_json('/home/zhangyuting/workspace/ner/kg_keywords.json')
    for i in range(len(gpt_sentence)):
        bio_form = gpt_ner_sentence_to_bio(gpt_sentence[i],kg_nodes)
        with open(f'{out_put_dir}/{i}.txt','w',encoding='utf-8') as file:
            for item in bio_form:
                file.write(item+ '\n')
