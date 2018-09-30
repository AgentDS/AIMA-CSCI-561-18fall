#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 3:38 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : homeless_service.py
# @Software: PyCharm

import numpy as np


class HomelessService(object):
    def __init__(self, b, p, L, LASHA_id, S, SPLA_id, A, app_info):
        self.b = b
        self.p = p
        self.L = L
        self.LASHA_id = LASHA_id
        self.S = S
        self.SPLA_id = SPLA_id
        self.A = A
        self.app_info = app_info


class ApplicantInfo(object):
    def __init__(self, info_str):
        self.app_id = int(info_str[:5], 2)
        self.gender = info_str[5]  # 'M'/'F'/'O'
        self.age = int(info_str[6:9])
        self.pets = 1 if info_str[9] == 'Y' else 0
        self.med = 1 if info_str[10] == 'Y' else 0
        self.car = 1 if info_str[11] == 'Y' else 0
        self.driver_license = 1 if info_str[12] == 'Y' else 0
        self.days = self._day_trans(info_str[13:])

    def _day_trans(self, day_str):
        days = np.zeros(shape=(7,), dtype=np.int8)
        for i in range(7):
            if day_str[i] == '1':
                days[i] = 1
        return days


def problem_generator(in_path):
    line_ct = 0
    LASHA_id_list = []
    SPLA_id_list = []
    app_info = []
    with open(in_path, 'r') as f_in:
        for line in f_in:
            line_ct += 1
            if line_ct == 1:
                b = int(line.strip())  # number of beds in the shelter
            elif line_ct == 2:
                p = int(line.strip())  # number of spaces in the parking lot
            elif line_ct == 3:
                L = int(line.strip())  # number of applicants chosen by LAHSA so far
            elif line_ct <= 3 + L:
                LASHA_id_list.append(line.strip())
            elif line_ct == 4 + L:
                S = int(line.strip())  # number of applicants chosen by SPLA so far
            elif line_ct <= 4 + L + S:
                SPLA_id_list.append(line.strip())
            elif line_ct == 5 + L + S:
                A = int(line.strip())  # total number of applicants
            elif line_ct <= 5 + L + S + A:
                app_info.append(ApplicantInfo(line.strip()))
