import json
import unittest

mapping_relations = {
    'R': 'RANGE',
    'V': 'VALUE',
    'M': 'METHOD',
    'ABB': 'ABB',
    'U': 'UNIT'
}

def convert_to_spo(data):
    entities = data['entities']
    spo_list = []
    current_ci = None
    current_ci_offset = None
    current_ci_idx = -1
    for i, entity in enumerate(entities):
        if entity['category'] == 'CI':
            current_ci = entity['entity']
            current_ci_offset = (entity['start_idx'],entity['end_idx'])
            current_ci_idx = i
            continue
        if current_ci is None:
            continue
        if entity['category'] not in ['CI_R', 'CI_V', 'CI_M', 'CI_ABB', 'CI_U']:
            continue
        is_between = True
        for j in range(i, len(entities)):
            if entities[j]['category'] == 'CI' and j > current_ci_idx and j < i:
                is_between = False
                break
        if is_between:
            relation = mapping_relations[entity['category'].split('_')[1]]
            spo = {
                'subject': current_ci,
                'subject_offset': current_ci_offset,
                'predicate': relation,
                'object': entity['entity'],
                'object_offset': (entity['start_idx'], entity['end_idx'])
            }
            spo_list.append(spo)

    return spo_list


class TestFormatSpo(unittest.TestCase):
    def test_format_spo(self):
        # 测试数据
        data =  {'text': ' 洪泽区人民医院检验报告单\n 110003452773\n姓名：王步明 性别：男 年龄：74岁 标本号：2 仪器：（区）AU5800\n门诊号：2022370195科室：急诊科门诊 病区： 床号： 临床诊断：冠心病\n标本种类：血清 标本说明： 采样日期：2022.12.0507：49 备注：自带血\n序代号 项目 结果 参考值 单位 序 代号 项目 结果 参考值 单位\n\n1TBIL 总胆红素 9.8 1.0~22.0 μmol/L 18ADA 腺苷脱氨酶 8.4 0~15.0U/L\n\n2DBIL 直接胆红素 3.9 0~6.8Hmol/l\n3IDBIL 间接胆红素 5.9 0~13.7mo1/L\n4TP 总蛋白 61.1 60.0~85.0g/L\n5ALB 白蛋白 37.8 35.0~55.0g/L\n6GLO 球蛋白 23.3 20.0~40.0g/L\n7A/G 白球比例 1.62 1.00~2.40\n8ALT 谷丙转氨酶 17.7 0~50.0U/L\n9ALP 碱性确酸酶 43.0 35.0~135.0U/L\n10AST 谷草转氨 23.0 0~40.0U/L\n11GGT 谷氨酰基转移酶 31.0 7.0~60.0U/L\n12TBA 总胆汁酸 4.4 0~11.9Pmo1/L\n13CHE 胆碱酯酶 5704 5000~12000U/L\n14UREA 尿素 7.20 1.70~8.30mmo1/L\n15CREA 肌酐 98.0 44.0~124.0mo1/L\n16UA 尿酸 348 89~416mo1/\n17LDH 乳酸脱氢酶 132.0 100.0~240.0U/\n肾小球滤过率 32.0 100.0~240.0U/\n送检医生：孙涛 检验者： 审核者：接收日期：2022.12.0508:08注：偏高偏低\n\n说明：本检验报告只对本次标本负责如有疑问，请于5日内联系报告日期：2022.12.0508：42', 'entities': [{'start_idx': 1, 'end_idx': 8, 'category': 'HN', 'entity': '洪泽区人民医院'}, {'start_idx': 8, 'end_idx': 13, 'category': 'HD', 'entity': '检验报告单'}, {'start_idx': 28, 'end_idx': 30, 'category': 'PI', 'entity': '姓名'}, {'start_idx': 35, 'end_idx': 37, 'category': 'PI', 'entity': '性别'}, {'start_idx': 40, 'end_idx': 42, 'category': 'PI', 'entity': '年龄'}, {'start_idx': 47, 'end_idx': 50, 'category': 'TI', 'entity': '标本号'}, {'start_idx': 53, 'end_idx': 55, 'category': 'TI', 'entity': '仪器'}, {'start_idx': 66, 'end_idx': 69, 'category': 'TI', 'entity': '门诊号'}, {'start_idx': 80, 'end_idx': 82, 'category': 'TI', 'entity': '科室'}, {'start_idx': 89, 'end_idx': 91, 'category': 'PI', 'entity': '病区'}, {'start_idx': 93, 'end_idx': 95, 'category': 'PI', 'entity': '床号'}, {'start_idx': 97, 'end_idx': 101, 'category': 'TI', 'entity': '临床诊断'}, {'start_idx': 106, 'end_idx': 110, 'category': 'TI', 'entity': '标本种类'}, {'start_idx': 114, 'end_idx': 118, 'category': 'TI', 'entity': '标本说明'}, {'start_idx': 120, 'end_idx': 124, 'category': 'TI', 'entity': '采样日期'}, {'start_idx': 141, 'end_idx': 143, 'category': 'TI', 'entity': '备注'}, {'start_idx': 185, 'end_idx': 189, 'category': 'CI_ABB', 'entity': 'TBIL'}, {'start_idx': 190, 'end_idx': 194, 'category': 'CI', 'entity': '总胆红素'}, {'start_idx': 195, 'end_idx': 198, 'category': 'CI_V', 'entity': '9.8'}, {'start_idx': 199, 'end_idx': 207, 'category': 'CI_R', 'entity': '1.0~22.0'}, {'start_idx': 208, 'end_idx': 214, 'category': 'CI_U', 'entity': 'μmol/L'}, {'start_idx': 217, 'end_idx': 220, 'category': 'CI_ABB', 'entity': 'ADA'}, {'start_idx': 221, 'end_idx': 226, 'category': 'CI', 'entity': '腺苷脱氨酶'}, {'start_idx': 227, 'end_idx': 230, 'category': 'CI_V', 'entity': '8.4'}, {'start_idx': 231, 'end_idx': 235, 'category': 'CI_R', 'entity': '0~15'}, {'start_idx': 237, 'end_idx': 240, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 243, 'end_idx': 247, 'category': 'CI_ABB', 'entity': 'DBIL'}, {'start_idx': 248, 'end_idx': 253, 'category': 'CI', 'entity': '直接胆红素'}, {'start_idx': 254, 'end_idx': 257, 'category': 'CI_V', 'entity': '3.9'}, {'start_idx': 258, 'end_idx': 263, 'category': 'CI_R', 'entity': '0~6.8'}, {'start_idx': 271, 'end_idx': 276, 'category': 'CI_ABB', 'entity': 'IDBIL'}, {'start_idx': 277, 'end_idx': 282, 'category': 'CI', 'entity': '间接胆红素'}, {'start_idx': 283, 'end_idx': 286, 'category': 'CI_V', 'entity': '5.9'}, {'start_idx': 287, 'end_idx': 293, 'category': 'CI_R', 'entity': '0~13.7'}, {'start_idx': 293, 'end_idx': 298, 'category': 'CI_U', 'entity': 'mo1/L'}, {'start_idx': 300, 'end_idx': 302, 'category': 'CI_ABB', 'entity': 'TP'}, {'start_idx': 303, 'end_idx': 306, 'category': 'CI', 'entity': '总蛋白'}, {'start_idx': 307, 'end_idx': 311, 'category': 'CI_V', 'entity': '61.1'}, {'start_idx': 312, 'end_idx': 321, 'category': 'CI_R', 'entity': '60.0~85.0'}, {'start_idx': 321, 'end_idx': 324, 'category': 'CI_U', 'entity': 'g/L'}, {'start_idx': 326, 'end_idx': 329, 'category': 'CI_ABB', 'entity': 'ALB'}, {'start_idx': 330, 'end_idx': 333, 'category': 'CI', 'entity': '白蛋白'}, {'start_idx': 334, 'end_idx': 338, 'category': 'CI_V', 'entity': '37.8'}, {'start_idx': 339, 'end_idx': 348, 'category': 'CI_R', 'entity': '35.0~55.0'}, {'start_idx': 348, 'end_idx': 351, 'category': 'CI_U', 'entity': 'g/L'}, {'start_idx': 353, 'end_idx': 356, 'category': 'CI_ABB', 'entity': 'GLO'}, {'start_idx': 357, 'end_idx': 360, 'category': 'CI', 'entity': '球蛋白'}, {'start_idx': 361, 'end_idx': 365, 'category': 'CI_V', 'entity': '23.3'}, {'start_idx': 366, 'end_idx': 375, 'category': 'CI_R', 'entity': '20.0~40.0'}, {'start_idx': 375, 'end_idx': 378, 'category': 'CI_U', 'entity': 'g/L'}, {'start_idx': 380, 'end_idx': 383, 'category': 'CI_ABB', 'entity': 'A/G'}, {'start_idx': 384, 'end_idx': 388, 'category': 'CI', 'entity': '白球比例'}, {'start_idx': 389, 'end_idx': 393, 'category': 'CI_V', 'entity': '1.62'}, {'start_idx': 394, 'end_idx': 403, 'category': 'CI_R', 'entity': '1.00~2.40'}, {'start_idx': 405, 'end_idx': 408, 'category': 'CI_ABB', 'entity': 'ALT'}, {'start_idx': 409, 'end_idx': 414, 'category': 'CI', 'entity': '谷丙转氨酶'}, {'start_idx': 415, 'end_idx': 419, 'category': 'CI_V', 'entity': '17.7'}, {'start_idx': 420, 'end_idx': 426, 'category': 'CI_R', 'entity': '0~50.0'}, {'start_idx': 426, 'end_idx': 429, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 431, 'end_idx': 434, 'category': 'CI_ABB', 'entity': 'ALP'}, {'start_idx': 435, 'end_idx': 440, 'category': 'CI', 'entity': '碱性确酸酶'}, {'start_idx': 441, 'end_idx': 445, 'category': 'CI_V', 'entity': '43.0'}, {'start_idx': 446, 'end_idx': 456, 'category': 'CI_R', 'entity': '35.0~135.0'}, {'start_idx': 456, 'end_idx': 459, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 462, 'end_idx': 465, 'category': 'CI_ABB', 'entity': 'AST'}, {'start_idx': 466, 'end_idx': 470, 'category': 'CI', 'entity': '谷草转氨'}, {'start_idx': 471, 'end_idx': 475, 'category': 'CI_V', 'entity': '23.0'}, {'start_idx': 476, 'end_idx': 482, 'category': 'CI_R', 'entity': '0~40.0'}, {'start_idx': 482, 'end_idx': 485, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 488, 'end_idx': 491, 'category': 'CI_ABB', 'entity': 'GGT'}, {'start_idx': 492, 'end_idx': 499, 'category': 'CI', 'entity': '谷氨酰基转移酶'}, {'start_idx': 500, 'end_idx': 504, 'category': 'CI_V', 'entity': '31.0'}, {'start_idx': 505, 'end_idx': 513, 'category': 'CI_R', 'entity': '7.0~60.0'}, {'start_idx': 513, 'end_idx': 516, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 519, 'end_idx': 522, 'category': 'CI_ABB', 'entity': 'TBA'}, {'start_idx': 523, 'end_idx': 527, 'category': 'CI', 'entity': '总胆汁酸'}, {'start_idx': 528, 'end_idx': 531, 'category': 'CI_V', 'entity': '4.4'}, {'start_idx': 532, 'end_idx': 538, 'category': 'CI_R', 'entity': '0~11.9'}, {'start_idx': 538, 'end_idx': 544, 'category': 'CI_U', 'entity': 'Pmo1/L'}, {'start_idx': 547, 'end_idx': 550, 'category': 'CI_ABB', 'entity': 'CHE'}, {'start_idx': 551, 'end_idx': 555, 'category': 'CI', 'entity': '胆碱酯酶'}, {'start_idx': 556, 'end_idx': 560, 'category': 'CI_V', 'entity': '5704'}, {'start_idx': 561, 'end_idx': 571, 'category': 'CI_R', 'entity': '5000~12000'}, {'start_idx': 571, 'end_idx': 574, 'category': 'CI_U', 'entity': 'U/L'}, {'start_idx': 577, 'end_idx': 581, 'category': 'CI_ABB', 'entity': 'UREA'}, {'start_idx': 582, 'end_idx': 584, 'category': 'CI', 'entity': '尿素'}, {'start_idx': 585, 'end_idx': 589, 'category': 'CI_V', 'entity': '7.20'}, {'start_idx': 590, 'end_idx': 599, 'category': 'CI_R', 'entity': '1.70~8.30'}, {'start_idx': 599, 'end_idx': 605, 'category': 'CI_U', 'entity': 'mmo1/L'}, {'start_idx': 608, 'end_idx': 612, 'category': 'CI_ABB', 'entity': 'CREA'}, {'start_idx': 613, 'end_idx': 615, 'category': 'CI', 'entity': '肌酐'}, {'start_idx': 616, 'end_idx': 617, 'category': 'CI_V', 'entity': '9'}, {'start_idx': 617, 'end_idx': 620, 'category': 'CI_V', 'entity': '8.0'}, {'start_idx': 621, 'end_idx': 631, 'category': 'CI_R', 'entity': '44.0~124.0'}, {'start_idx': 631, 'end_idx': 636, 'category': 'CI_U', 'entity': 'mo1/L'}, {'start_idx': 639, 'end_idx': 641, 'category': 'CI_ABB', 'entity': 'UA'}, {'start_idx': 642, 'end_idx': 644, 'category': 'CI', 'entity': '尿酸'}, {'start_idx': 645, 'end_idx': 648, 'category': 'CI_V', 'entity': '348'}, {'start_idx': 649, 'end_idx': 655, 'category': 'CI_R', 'entity': '89~416'}, {'start_idx': 655, 'end_idx': 659, 'category': 'CI_U', 'entity': 'mo1/'}, {'start_idx': 662, 'end_idx': 665, 'category': 'CI_ABB', 'entity': 'LDH'}, {'start_idx': 666, 'end_idx': 671, 'category': 'CI', 'entity': '乳酸脱氢酶'}, {'start_idx': 672, 'end_idx': 677, 'category': 'CI_V', 'entity': '132.0'}, {'start_idx': 678, 'end_idx': 689, 'category': 'CI_R', 'entity': '100.0~240.0'}, {'start_idx': 689, 'end_idx': 691, 'category': 'CI_U', 'entity': 'U/'}, {'start_idx': 692, 'end_idx': 699, 'category': 'CI', 'entity': '肾小球滤过率 '}, {'start_idx': 699, 'end_idx': 700, 'category': 'CI_V', 'entity': '3'}, {'start_idx': 700, 'end_idx': 703, 'category': 'CI_V', 'entity': '2.0'}, {'start_idx': 704, 'end_idx': 715, 'category': 'CI_R', 'entity': '100.0~240.0'}, {'start_idx': 715, 'end_idx': 718, 'category': 'CI_U', 'entity': 'U/\n'}, {'start_idx': 718, 'end_idx': 722, 'category': 'TI', 'entity': '送检医生'}, {'start_idx': 726, 'end_idx': 729, 'category': 'TI', 'entity': '检验者'}, {'start_idx': 731, 'end_idx': 734, 'category': 'TI', 'entity': '审核者'}, {'start_idx': 735, 'end_idx': 739, 'category': 'TI', 'entity': '接收日期'}, {'start_idx': 763, 'end_idx': 765, 'category': 'TI', 'entity': '说明'}]}

        spo_result = convert_to_spo(data)
        print(spo_result)
        result = {'text': data['text'], 'spo_list': spo_result}
        with open("./test_result_spo.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)



