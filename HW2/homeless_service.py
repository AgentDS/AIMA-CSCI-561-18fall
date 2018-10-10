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

    def _SPLA_requirement(self):
        candidates = []
        for app in self.app_info:
            if app.car * app.driver_license * (1 - app.med) == 1:
                candidates.append(app)
        self._SPLA_candidates = candidates

    def _LAHSA_requirement(self):
        candidates = []
        for app in self.app_info:
            if app.gender == 'F' and app.age > 17 and app.pets == 0:
                candidates.append(app)
        self._LAHSA_candidates = candidates

    def _check_bed(self, LAHSA_tmp_choose):
        days = [app.days for app in LAHSA_tmp_choose]
        return np.all(reduce(np.add, days) <= self.b)

    def _check_parking(self, SPLA_tmp_choose):
        days = [app.days for app in SPLA_tmp_choose]
        return np.all(reduce(np.add, days) <= self.p)


class ApplicantInfo(object):
    def __init__(self, info_str):
        self.app_id = int(info_str[:5])
        self.gender = info_str[5]  # 'M'/'F'/'O'
        self.age = int(info_str[6:9])
        self.pets = 1 if info_str[9] == 'Y' else 0
        self.med = 1 if info_str[10] == 'Y' else 0
        self.car = 1 if info_str[11] == 'Y' else 0
        self.driver_license = 1 if info_str[12] == 'Y' else 0
        # days = info_str[13:]
        self.days = np.array([int(info_str[13 + i]) for i in range(7)], dtype=np.int8).reshape(1, 7)

    def __repr__(self):
        app_id = "%05d" % self.app_id
        gender = self.gender
        age = "%03d" % self.age
        pets = 'Y' if self.pets == 1 else 'N'
        med = 'Y' if self.med == 1 else 'N'
        car = 'Y' if self.car == 1 else 'N'
        driver = 'Y' if self.driver_license == 1 else 'N'
        days = ''.join([str(i) for i in self.days])
        return app_id + gender + age + pets + med + car + driver + days


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
                LASHA_id_list.append(int(line.strip()))
            elif line_ct == 4 + L:
                S = int(line.strip())  # number of applicants chosen by SPLA so far
            elif line_ct <= 4 + L + S:
                SPLA_id_list.append(int(line.strip()))
            elif line_ct == 5 + L + S:
                A = int(line.strip())  # total number of applicants
            elif line_ct <= 5 + L + S + A:
                app_info.append(ApplicantInfo(line.strip()))
    return HomelessService(b, p, L, LASHA_id_list, S, SPLA_id_list, A, app_info)
