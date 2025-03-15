# Author: caisongrui
# Created on: 2025/1/2 15:27
# Description:
import json
import os
import random
import openai
from pandas import Index
from tqdm import tqdm


def get_kg_nodes(kg_node_path):
    kg_nodes = {}
    for filename in os.listdir(kg_node_path):
        file_path = os.path.join(kg_node_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                kg_nodes.setdefault(filename.split('.')[0], []).append(line.strip())
    return kg_nodes

# 创建一个函数，通过GPT生成患者的话
def generate_patient_doctor_conversation(kg_nodes):
    selected_nodes = [
        random.choice(kg_nodes['Disease']),
        random.choice(kg_nodes['Symptom']),
        random.choice(kg_nodes['Medicine']),
        random.choice(kg_nodes['Diet']),
        random.choice(kg_nodes['Sport']),
        random.choice(kg_nodes['Lifestyle'])
        , random.choice(kg_nodes['Operation'])
        , random.choice(kg_nodes['Index'])
    ]

    # 构建prompt，指示GPT生成相关的对话
    prompt = f"""
    假设你是一个患者，你想向医生询问问题或陈述的症状，病情，治疗方案，运动，饮食，生活，用药，现在给你5个实体{selected_nodes}，请根据这些实体生成一句话，应尽量自然，并且对话中的实体不能改变。
    """
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ],
    )
    return completion.choices[0].message.content

def save_conversations_to_file(conversations, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error occurred while saving to file: {e}")

def generate_and_save_conversations(num_conversations, filename):
    conversations = []
    try:
        for i in tqdm(range(num_conversations)):
            conversation = generate_conversation(kg_nodes)
            conversations.append(conversation)
        save_conversations_to_file(conversations, filename)
    except Exception as e:
        print(f"Error occurred during conversation generation: {e}")
        print(f"Saving the generated conversations up to this point...")
        save_conversations_to_file(conversations, filename)


# 随机决定每个节点的数量
def randomize_node_count(node_list):
    num_nodes = random.randint(4, 5)
    return random.sample(node_list, num_nodes)

# 随机选择标点符号
punctuations = ['','','','','','','','','，', '。', '；', '！', '？']

def random_punctuation():
    return random.choice(punctuations)

def generate_conversation(kg_nodes):
    # 随机生成不同节点的数量和内容
    symptom = randomize_node_count(kg_nodes['Symptom'])
    disease = randomize_node_count(kg_nodes['Disease'])
    medication = randomize_node_count(kg_nodes['Medicine'])
    diet = randomize_node_count(kg_nodes['Diet'])
    sport = randomize_node_count(kg_nodes['Sport'])
    lifestyle = randomize_node_count(kg_nodes['Lifestyle'])
    operation = randomize_node_count(kg_nodes['Operation'])
    index = randomize_node_count(kg_nodes['Index'])

    # 随机组合和插入标点符号
    conversation = [
        f"最近我感觉{random.choice(symptom)}{random_punctuation()}{random.choice(symptom)}{random_punctuation()}{random.choice(symptom)}{random_punctuation()}感觉很难受。",
        f"我{random.choice(symptom)}{random_punctuation()}{random.choice(disease)}{random_punctuation()}{random.choice(symptom)}{random_punctuation()}这是什么病。",
        f"我最近在吃{random.choice(medication)}{random_punctuation()}{random.choice(medication)}{random_punctuation()}{random.choice(medication)}{random_punctuation()}对症吗。",
        f"我刚做了{random.choice(index)}{random_punctuation()}{random.choice(index)}{random_punctuation()}{random.choice(index)}{random_punctuation()}结果还没出来。",
        f"我最近在做{random.choice(sport)}{random_punctuation()}{random.choice(sport)}{random_punctuation()}{random.choice(sport)}{random_punctuation()}感觉很不错。",
        f"我最近改变了一些生活方式{random.choice(lifestyle)}{random_punctuation()}{random.choice(lifestyle)}{random_punctuation()}{random.choice(lifestyle)}{random_punctuation()}晚上不再熬夜了。",
        f"医生建议我进行{random.choice(operation)}{random_punctuation()}{random.choice(operation)}{random_punctuation()}{random.choice(operation)}{random_punctuation()}吃{random.choice(medication)}{random_punctuation()}{random.choice(medication)}{random_punctuation()}以便进一步治疗。",
        f"我也开始注意饮食{random.choice(diet)}{random_punctuation()}{random.choice(diet)}{random_punctuation()}{random.choice(diet)}{random_punctuation()}少吃油腻食物。"
    ]
    return random.choice(conversation)



if __name__ == '__main__':
    # openai.api_key = "sk-19hNrjvtIzKyOYlN9443Fd763f5d436992F9Ba7cF4C3702f"
    # openai.base_url = "https://free.v36.cm/v1/"
    # openai.default_headers = {"x-foo": "true"}
    kg_node_path = '/home/zhangyuting/workspace/ner/output_nodes_1125'
    kg_nodes = get_kg_nodes(kg_node_path)
    # conversation = generate_patient_doctor_conversation(kg_nodes)
    num_conversations = 2000
    filename = 'random_sentence.json'
    generate_and_save_conversations(num_conversations, filename)