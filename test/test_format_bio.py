# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/12 15:00
# LAST MODIFIED ON:
# AIM:

import unittest
from app.model.labelstudio_to_bio_ner import title_ner_labelstudio_to_bio,ner_labelstudio_to_bio
from app.utility.file_opt import read_json


class TestFormatLabelStudio(unittest.TestCase):
    def testcase1(self):
        labelstudio_result = read_json("../data/results/24小时动态血压0-1666265934409.json")
        bio_result = title_ner_labelstudio_to_bio(labelstudio_result)
        predict_result = ['\n O', '\n O', '\t O', '1 O', '9 O', ': O', '3 O', '8 O', '\n O', '\n O', '\t O', '血 O', '压 O', '血 O', '糖 O', '\n O', '\n O', '\t O', '3 O', '\t O', '已 O', '完 O', '成 O', '\n O', '\t O', '/ O', '2 O', '次 O', '\n O', '\n O', '\t O', '您 O', '今 O', '天 O', '已 O', '完 O', '成 O', '两 O', '次 O', '血 O', '压 O', '测 O', '量 O', '， O', '棒 O', '棒 O', '哒 O', '！ O', '\n O', '\n O', '\t O', '当 O', '前 O', '血 O', '压 O', '（ O', '单 O', '位 O', '： O', 'm O', 'm O', 'H O', 'g O', '） O', '2 O', '0 O', '2 O', '2 O', '- O', '1 O', '0 O', '- O', '2 O', '0 O', '1 O', '9 O', ': O', '0 O', '0 O', ': O', '0 O', '0 O', '\n O', '\n O', '\t O', '收 O', '缩 O', '压 O', '\t O', '舒 O', '张 O', '压 O', '\t O', '心 B_CI', '率 I_CI', '  I_CI', '异 O', '常 O', '\n O', '\n O', '\t O', '1 O', '6 O', '5 O', '\t O', '9 O', '0 O', '\t O', '7 O', '6 O', '\n O', '\n O', '\t O', '今 O', '日 O', '血 O', '压 O', '（ O', '单 O', '位 O', '： O', 'm B_CI_U', 'm I_CI_U', 'H I_CI_U', 'g I_CI_U', '） I_CI_U', '\t I_CI_U', '历 O', '史 O', '血 O', '压 O', '\n O', '\n O', '\t O', '时 O', '间 O', '\t O', '收 O', '缩 O', '压 O', '\t O', '舒 O', '张 O', '压 O', '\t O', '心 B_CI', '率 I_CI', '\n I_CI', '\n I_CI', '\t I_CI', '1 O', '9 O', ': O', '0 O', '0 O', ': O', '0 O', '0 O', '\t O', '1 O', '6 O', '5 O', '\t O', '0 O', '6 O', '\t O', '7 O', '6 O', '\n O', '\n O', '\t O', '0 O', '7 O', ': O', '2 O', '9 O', ': O', '0 O', '0 O', '\t O', '1 O', '5 O', '1 O', '\t O', '8 O', '8 O', '\t O', '6 O', '7 O', '\n O', '\n O', '\t O', '0 O', '7 O', ': O', '2 O', '7 O', ': O', '0 O', '0 O', '\t O', '1 O', '5 O', '1 O', '\t O', '8 O', '8 O', '\t O', '7 O', '0 O', '\n O', '\n O', '\t O', '手 O', '动 O', '输 O', '入 O']
        assert bio_result == predict_result
        print(bio_result)

    def testcase2(self):
        labelstudio_result = read_json("test.json")
        bio_result = title_ner_labelstudio_to_bio(labelstudio_result)

        print(bio_result)