# -*- coding: utf-8 -*- #
# CREATED BY: caisongrui
# CREATED ON: 2024/10/10 16:45
# LAST MODIFIED ON:
# AIM:

import requests
import json

import unittest

class TestNERserver(unittest.TestCase):
    def test_case1(self):
      url = "http://192.168.110.196:10082/api/doc-ner"
      payload = json.dumps({
        "content": "\n\n\t重庆黔江民族医院检验报告单重庆医科大学附属第二医院黔江分院\n\n\t性\t别：男\t门诊号：20030000送检医生：游治虎目的：心肌三合一定量\n\t姓名：倪明山\t备注：\n\t科室：心血管内科门诊\t状态\t单位\t参考范围\n\t临床诊断：\t结果\n\t电请号：202000833515\t简称\tng/ml\t<100\n\t序号中文名称\t26.20\tng/ml\t<4.0\n\tMyo\t2.16\t≤0.1\n\t肌红张白\tCK-MB\tng/ml\n\t0.05\n\n\t检验时间：2020-03-0109：52 报告时间：2020-03-0110:13\n\t采样时间：2020-03-0109:05签收时间：2020-03-0109:52\t审核者签名： 王秀\n\t注：此结果仅对本次检测标本负责！\t检验者：冉茂红\n\t如果对结果有疑义，请在收到结果7个工作日内与我们联系，多谢合作！"
      })
      headers = {
        'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      print(response.text)

    def test_case2(self):
      url = "http://192.168.110.196:10082/api/doc-ner"
      payload = json.dumps({
        "content": " RIA3DR01 Date ofVisit:19-Apr-2023 1A.e 集团提\\n imber:PzK695885s 项目、\\n\\n 打造全\\n\\n\\n DateofVisit:29-Nov-2023 14:13:27 页目建\\n27\\n1) Device:AstraS DR MRIX3DR01 SW030SoftwareVersion8.2(8.1)\\n20 SerialNumber:RNL646260S CopyrightMedtronic.Inc.2020 汤馆10\\n 供融\\n\\n\\n3 Final:Quick LookIl Page1 业优化\\n Device Status（lmplanted:27-Oct-2023) 业，\\n\\n Remaining Longevity 13.1years (29-Nov-2023） 发展发\\n 中\\n 0”重\\n\\n RRT >5years 发放\\n (updatedbasedonParameterchange) 京最\\n Atrial RV 车站\\n Lead Impedance 475ohms 380ohms 贷款\\n Capture Threshold 0.375V@0.40ms 0.625V@0.40ms 游业\\n Measured On 29-Nov-2023 29-Nov-2023 当费\\n ProgrammedAmplitude/PulseWidth 1.50V/0.40ms 2.00V/0.40ms 国进\\n MeasuredP/RWave 1.6mV 京粮\\n Programmed Sensitivity 0.30mV 0.90mV 务方\\n\\n 世界\\n 行北\\n 界\\n\\n 客实\\n 务\\n 点\\n\\n 发\\n 育发展\\n 动为推进中国式现代化贡献\\n 造工厂项目融资融智：为风电行业首个获得 金融服务创造美好未来的新篇\\n注人了新的动力 “智能制造标杆企业”称号的三一重能发放贷\\n“马尔代夫国际机场立"
      })
      headers = {
        'Content-Type': 'application/json'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      print(response.text)
