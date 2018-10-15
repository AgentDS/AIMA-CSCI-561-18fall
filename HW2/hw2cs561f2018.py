#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 5:54 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw2cs561f2018.py
# @Software: PyCharm
from __future__ import print_function
import homeless_service as hs
import numpy as np


prob = hs.problem_generator('input2.txt')

# app_info = []
# app_info.append(hs.ApplicantInfo('00001M035NNYY1111111'))
# app_info.append(hs.ApplicantInfo('00002F020NNYY1100001'))
# app_info.append(hs.ApplicantInfo('00003F020NNYY1001101'))
# app_info.append(hs.ApplicantInfo('00004F025NNYY0000010'))
# app_info.append(hs.ApplicantInfo('00005F020YNYY0011000'))
# app_info.append(hs.ApplicantInfo('00006F020NNYY1001011'))
# app_info.append(hs.ApplicantInfo('00007M016NNYY1101110'))
#
# f = lambda l: [[i - 1 for i in k] for k in l]
# SPLA = f([[1, 5, 2, 7], [1, 4, 5, 7], [3, 1, 5, 7], [3, 5, 2, 7], [3, 4, 5, 7]])
# LAHSA = f([[4, 3, 6], [3, 2, 6], [4, 2, 6], [4, 1, 6], [1, 2, 6]])
#
# plan_cnt = len(SPLA)
# for i in range(plan_cnt):
#     SPLA_eff = hs.cal_point([app_info[k] for k in SPLA[i]], 10)
#     LAHSA_eff = hs.cal_point([app_info[k] for k in LAHSA[i]], 10)
#     print("SPLA:", np.array(SPLA[i]) + 1)
#     print("LAHSA:", np.array(LAHSA[i]) + 1)
#     print("SPLA efficiency = %.5f, LAHSA efficiency = %.5f" % (SPLA_eff, LAHSA_eff))
