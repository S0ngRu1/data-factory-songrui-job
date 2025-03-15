# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/14 10:19
# LAST MODIFIED ON:
# AIM:
import unittest
from app.model.process_predict_label import process_predict_label
from app.utility.file_opt import read_json

class TestProcessPredictLabel(unittest.TestCase):
    def testcase1(self):
        data = read_json('../data/sample_data_11:15:04.970222/2023-04-14T02:44:20.json')
        process_data = process_predict_label(data)
        print(process_data)

    def testcase2(self):
        data = read_json('../data/sample_data_11:15:04.970222/1629155604168.json')
        process_data = process_predict_label(data)
        print(process_data)

    def testcase3(self):
        data = {
  "data": {
    "text": "\n\n\t2022-10-12（肝功能1（ASTALTTP）常规分析仪器：生化LABOSPECT008\n\n\t南充市中心医院·南充市临床检验中心检验报告单\n\n\tNanchong Central Hospital·Nanchong Center for Clinical Laboratories批次（Bat）：1\n\n\t姓名（Name）：王定义\t科别（Dept）：心血管内科门诊标本类型（Type）：血浆\n\t性别（Sex）：男\t床号（Bed）\t病历号（P.No.）：13608748检验号（S.No.）：45\n\n\t年龄（Age）：79岁\t申请医师（Doc）：陈世蓉\t门诊卡号（Pat）：sO1144344800集信训\n\t测定值\t单位\t参考区间\t实验方法\n\t序号\t项目名称\t速率法\n\t天门冬氨酸氨基转移酶（*AST）\t17.4\tU/L\t15.0-40.0\n\t15.8\tU/L\t9.0-50.0\t速率法\n\t丙氨酸氨基转移酶（+ALT）\t72.9\tg/L\t65.0-85.0\t双缩眼法\n\t总蛋自（*TP）\tB/L\t40.0-55.0\t溴甲酚绿法\n\t白蛋白（*ALB）\t37.9\t计算法\n\t35\tB/L\t20.0-40.0\t计算法\n\t5\t球蛋白（G1b）\t1.1\t1.2-2.4\n\t6\t白蛋白/球蛋白（A/G）\tumol/L\t<=23.0\t钒酸盐氧化法\n\t总胆红素（*TBi1）\tumol/L\t1.7-6.8\t钒酸盐氧化法\n\t直接胆红素（DBi1）\t2.5\t速率法\n\t8\t69.5\tU/L\t10.0-60.0\n\t9\tY-谷氨酰基转移酶（*GGT）\tmg/L\t200-430\t免疫比浊法\n\t前白张白（PA）\t232\t5000-12000\t速率法\n\t10\t8712\tU/L\t过氧化物酶法\n\t11\t胆碱脂菌（ChE）\t6.3\tU/L\t<10.0\t乳胶免疫比浊法\n\t12\t5一核苷酸酶（5-NT）\t0.23\tmg/L\t<2.70\t己糖激酶法\n\t13\t甘胆酸（CG）\t5.57\tmmol/L\t3.90-6.10\n\t14\t萄糖（*GLU）\tumol/L\t208.0-428.0\t尿酸酶法-抗VC\n\t尿酿（UA）\t308.3\t57-111\n\t15\t153\tumol/L\n\t16\t肌（*Crea）\t5.41\tmmol/L\t3.10-9.50\t乳胶免疫比浊法\n\t17\t尿素（*Urea）\t1.99.\tmg/L\t0.59-1.03\tGPO-PAP法\n\t18\t航抑素C（Cys\t1.69\tmmol/L\t0.00-1.70\tCHOD-PAP法\n\t19\t甘油三脂（*TG）\tmmol/L\t0.00-5.18\n\t4.20\t1.16-1.42\t直接法\n\t20\t总胆固醇（*CHO）\t1.12\tmmol/L\t直接法\n\t高密度脂蛋白胆固醇（HDL-C）\t2.72\tmmo1/L\t0.00-3.10\n\t21\t低密度脂蛋自胆固醇（LDL-C）\tmg/1\t<=6.0\t免疫比浊法\n\t22\t10.8\t0.10-0.90\tACS-ACOD法\n\t23\t全程C反应蛋白（CRP）\t0.14\tmmol/L\t离子选择电极法\n\t游高脂助酸（NEFA)\t4.03\tmmol/L\t3.50-5.30\n\t24\tmmol/L\t137.0-147.0\t离子选择电极法\n\t25\t（*K）\t143.2\t99.0-110.0\t离子选择电极法\n\t26\t钠（*Na）\t110.5\tmmol/L\t计算法\n\t（*C1）\tmmol/L\t280-310\n\t27\t305.4\n\t28\t晶体渗透压（PCOP）\n\n\t备注：*项目为四川省医疗机构临床检验结果互认项目本检验正常参考范围针对正常成人，特殊人群请咨询临床医师。\n\n\t页码：第1页\n\t复核者：赵全能\t报告时间：2022-10-1209:29\n\t检验者：李欣\t接收时间：2022-10-1208:40\n\n\t采集时间：2022-10-1208:29\t电话：0817-2243072\n\n\t医院本部地址：四川省南充市顺庆区人民南路97号\t电话：0817-3343299\n\n\t医院江东院区：四川省南充市高坪区星河东路99号\n\n\t声明：此报告只对该送检标本负贵，如有疑义应在报告发出两日内提出。"
  },
  "annotations": [
    {
      "result": [
        {
          "value": {
            "start": 52,
            "end": 59,
            "text": "南充市中心医院",
            "labels": "HN"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 86,
            "end": 94,
            "text": "Central ",
            "labels": "CI_ABB"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 94,
            "end": 102,
            "text": "Hospital",
            "labels": "OTHER"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 119,
            "end": 123,
            "text": "for ",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 123,
            "end": 132,
            "text": "Clinical ",
            "labels": "CI_ABB"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 156,
            "end": 159,
            "text": "姓名（",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 169,
            "end": 172,
            "text": "科别（",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 185,
            "end": 190,
            "text": "标本类型（",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 200,
            "end": 203,
            "text": "性别（",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 210,
            "end": 212,
            "text": "床号",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 218,
            "end": 222,
            "text": "病历号（",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 253,
            "end": 256,
            "text": "年龄（",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 265,
            "end": 270,
            "text": "申请医师（",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 282,
            "end": 284,
            "text": "号（",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 313,
            "end": 317,
            "text": "参考区间",
            "labels": "CI_TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 317,
            "end": 318,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 324,
            "end": 326,
            "text": "序号",
            "labels": "CI_TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 326,
            "end": 327,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 327,
            "end": 331,
            "text": "项目名称",
            "labels": "CI_TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 331,
            "end": 332,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 332,
            "end": 335,
            "text": "速率法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 335,
            "end": 336,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 336,
            "end": 337,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 337,
            "end": 353,
            "text": "天门冬氨酸氨基转移酶（*AST）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 353,
            "end": 354,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 359,
            "end": 362,
            "text": "U/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 362,
            "end": 363,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 379,
            "end": 382,
            "text": "U/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 382,
            "end": 383,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 392,
            "end": 395,
            "text": "速率法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 395,
            "end": 396,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 396,
            "end": 397,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 397,
            "end": 411,
            "text": "丙氨酸氨基转移酶（+ALT）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 411,
            "end": 412,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 417,
            "end": 420,
            "text": "g/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 420,
            "end": 421,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 437,
            "end": 445,
            "text": "总蛋自（*TP）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 445,
            "end": 446,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 460,
            "end": 465,
            "text": "溴甲酚绿法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 465,
            "end": 466,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 466,
            "end": 467,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 467,
            "end": 476,
            "text": "白蛋白（*ALB）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 476,
            "end": 477,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 482,
            "end": 485,
            "text": "计算法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 485,
            "end": 486,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 486,
            "end": 487,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 504,
            "end": 507,
            "text": "计算法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 507,
            "end": 508,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 508,
            "end": 509,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 511,
            "end": 519,
            "text": "球蛋白（G1b）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 519,
            "end": 520,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 535,
            "end": 547,
            "text": "白蛋白/球蛋白（A/G）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 547,
            "end": 548,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 548,
            "end": 554,
            "text": "umol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 554,
            "end": 555,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 562,
            "end": 568,
            "text": "钒酸盐氧化法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 568,
            "end": 569,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 569,
            "end": 570,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 570,
            "end": 581,
            "text": "总胆红素（*TBi1）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 581,
            "end": 582,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 582,
            "end": 588,
            "text": "umol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 588,
            "end": 589,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 597,
            "end": 603,
            "text": "钒酸盐氧化法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 603,
            "end": 604,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 604,
            "end": 605,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 605,
            "end": 616,
            "text": "直接胆红素（DBi1）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 616,
            "end": 617,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 621,
            "end": 624,
            "text": "速率法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 624,
            "end": 625,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 625,
            "end": 626,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 633,
            "end": 636,
            "text": "U/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 636,
            "end": 637,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 650,
            "end": 665,
            "text": "Y-谷氨酰基转移酶（*GGT）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 665,
            "end": 666,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 666,
            "end": 670,
            "text": "mg/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 670,
            "end": 671,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 679,
            "end": 684,
            "text": "免疫比浊法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 684,
            "end": 685,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 685,
            "end": 686,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 710,
            "end": 713,
            "text": "速率法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 713,
            "end": 714,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 714,
            "end": 715,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 723,
            "end": 726,
            "text": "U/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 726,
            "end": 727,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 727,
            "end": 733,
            "text": "过氧化物酶法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 733,
            "end": 734,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 734,
            "end": 735,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 738,
            "end": 747,
            "text": "胆碱脂菌（ChE）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 747,
            "end": 748,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 752,
            "end": 755,
            "text": "U/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 755,
            "end": 756,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 762,
            "end": 769,
            "text": "乳胶免疫比浊法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 769,
            "end": 770,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 770,
            "end": 771,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 774,
            "end": 786,
            "text": "5一核苷酸酶（5-NT）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 786,
            "end": 787,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 792,
            "end": 796,
            "text": "mg/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 796,
            "end": 797,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 803,
            "end": 808,
            "text": "己糖激酶法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 808,
            "end": 809,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 809,
            "end": 810,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 813,
            "end": 820,
            "text": "甘胆酸（CG）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 820,
            "end": 821,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 826,
            "end": 832,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 832,
            "end": 833,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 847,
            "end": 855,
            "text": "萄糖（*GLU）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 855,
            "end": 856,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 856,
            "end": 862,
            "text": "umol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 862,
            "end": 863,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 875,
            "end": 883,
            "text": "尿酸酶法-抗VC",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 883,
            "end": 884,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 884,
            "end": 885,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 885,
            "end": 891,
            "text": "尿酿（UA）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 891,
            "end": 892,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 913,
            "end": 919,
            "text": "umol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 919,
            "end": 920,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 920,
            "end": 921,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 924,
            "end": 932,
            "text": "肌（*Crea）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 932,
            "end": 933,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 938,
            "end": 944,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 944,
            "end": 945,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 955,
            "end": 962,
            "text": "乳胶免疫比浊法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 962,
            "end": 963,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 963,
            "end": 964,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 967,
            "end": 976,
            "text": "尿素（*Urea）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 976,
            "end": 977,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 983,
            "end": 987,
            "text": "mg/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 987,
            "end": 988,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 998,
            "end": 1006,
            "text": "GPO-PAP法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1006,
            "end": 1007,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1007,
            "end": 1008,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1011,
            "end": 1019,
            "text": "航抑素C（Cys",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1019,
            "end": 1020,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1025,
            "end": 1031,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1031,
            "end": 1032,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1042,
            "end": 1051,
            "text": "CHOD-PAP法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1051,
            "end": 1052,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1052,
            "end": 1053,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1056,
            "end": 1065,
            "text": "甘油三脂（*TG）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1065,
            "end": 1066,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1066,
            "end": 1072,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1072,
            "end": 1073,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1099,
            "end": 1102,
            "text": "直接法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1102,
            "end": 1103,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1103,
            "end": 1104,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1107,
            "end": 1117,
            "text": "总胆固醇（*CHO）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1117,
            "end": 1118,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1123,
            "end": 1129,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1129,
            "end": 1130,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1130,
            "end": 1133,
            "text": "直接法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1133,
            "end": 1134,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1134,
            "end": 1135,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1135,
            "end": 1151,
            "text": "高密度脂蛋白胆固醇（HDL-C）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1151,
            "end": 1152,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1157,
            "end": 1163,
            "text": "mmo1/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1163,
            "end": 1164,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1178,
            "end": 1194,
            "text": "低密度脂蛋自胆固醇（LDL-C）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1194,
            "end": 1195,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1195,
            "end": 1199,
            "text": "mg/1",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1199,
            "end": 1200,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1206,
            "end": 1211,
            "text": "免疫比浊法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1211,
            "end": 1212,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1212,
            "end": 1213,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1231,
            "end": 1240,
            "text": "ACS-ACOD法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1240,
            "end": 1241,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1241,
            "end": 1242,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1245,
            "end": 1257,
            "text": "全程C反应蛋白（CRP）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1257,
            "end": 1258,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1263,
            "end": 1269,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1269,
            "end": 1270,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1270,
            "end": 1277,
            "text": "离子选择电极法",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1277,
            "end": 1278,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1278,
            "end": 1279,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1296,
            "end": 1302,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1302,
            "end": 1303,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1317,
            "end": 1323,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1323,
            "end": 1324,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1336,
            "end": 1343,
            "text": "离子选择电极法",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1343,
            "end": 1344,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1344,
            "end": 1345,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1370,
            "end": 1377,
            "text": "离子选择电极法",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1377,
            "end": 1378,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1378,
            "end": 1379,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1382,
            "end": 1388,
            "text": "钠（*Na）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1388,
            "end": 1389,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1395,
            "end": 1401,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1401,
            "end": 1402,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1402,
            "end": 1405,
            "text": "计算法",
            "labels": "CI_M"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1405,
            "end": 1406,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1406,
            "end": 1407,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1413,
            "end": 1419,
            "text": "mmol/L",
            "labels": "CI_U"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1419,
            "end": 1420,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1442,
            "end": 1453,
            "text": "晶体渗透压（PCOP）",
            "labels": "CI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1453,
            "end": 1454,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1454,
            "end": 1455,
            "text": "\n",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1455,
            "end": 1456,
            "text": "\t",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1456,
            "end": 1458,
            "text": "备注",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1458,
            "end": 1459,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1512,
            "end": 1513,
            "text": "码",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1513,
            "end": 1514,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1519,
            "end": 1522,
            "text": "复核者",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1527,
            "end": 1531,
            "text": "报告时间",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1531,
            "end": 1532,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1549,
            "end": 1552,
            "text": "检验者",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1556,
            "end": 1560,
            "text": "接收时间",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1560,
            "end": 1561,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1579,
            "end": 1583,
            "text": "采集时间",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1583,
            "end": 1584,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1600,
            "end": 1602,
            "text": "电话",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1602,
            "end": 1603,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1622,
            "end": 1624,
            "text": "地址",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1624,
            "end": 1625,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1642,
            "end": 1644,
            "text": "电话",
            "labels": "PI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1644,
            "end": 1645,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1664,
            "end": 1666,
            "text": "院区",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1666,
            "end": 1667,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1686,
            "end": 1688,
            "text": "声明",
            "labels": "TI"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1688,
            "end": 1689,
            "text": "：",
            "labels": [
              "OTHER"
            ]
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        },
        {
          "value": {
            "start": 1697,
            "end": 1701,
            "text": "标本负贵",
            "labels": "OTHER"
          },
          "from_name": "label",
          "to_name": "text",
          "type": "labels"
        }
      ]
    }
  ]
}
        processed_data = process_predict_label(data)
        print(processed_data)