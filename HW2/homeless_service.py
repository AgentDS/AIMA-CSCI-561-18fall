#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 3:38 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : homeless_service.py
# @Software: PyCharm

import numpy as np


class HomelessService(object):
    def __init__(self, b, p, L, LAHSA_id, S, SPLA_id, A, app_info):
        self.b = b
        self.p = p
        self.L = L
        self.LAHSA_id = LAHSA_id
        self.S = S
        self.SPLA_id = SPLA_id
        self.A = A
        self.app_info = app_info
        self.resolution = []
        self.resolution_modify = []

        # to indicate whether application have been choose, True means having been used
        self._SPLA_tmp = None
        self._LAHSA_tmp = None

        self._SPLA_flag = False  # if True then means choose ends for SPLA
        self._LAHSA_flag = False  # if True then means choose ends for LAHSA

        # to store IDs chosen currently
        self._SPLA_current_list = []
        self._LAHSA_current_list = []

        # to store IDs which are qualified for requirements
        self._SPLA_candidates = None
        self._LAHSA_candidates = None
        self._get_SPLA_candidate()
        self._get_LAHSA_candidate()

    def _reset_SPLA_tmp(self):
        self._SPLA_tmp = [False] * len(self._SPLA_candidates)

    def _reset_LAHSA_tmp(self):
        self._LAHSA_tmp = [False] * len(self._LAHSA_candidates)

    def _get_SPLA_candidate(self):
        candidates = []
        for id in self.app_info:
            app = self.app_info[id]
            if app.car * app.driver_license * (1 - app.med) == 1:
                if app.app_id not in self.SPLA_id and app.app_id not in self.LAHSA_id:
                    candidates.append(id)
        self._SPLA_candidates = candidates
        self._SPLA_candidates_cnt = len(candidates)

    def _get_LAHSA_candidate(self):
        candidates = []
        for id in self.app_info:
            app = self.app_info[id]
            if app.gender == 'F' and app.age > 17 and app.pets == 0:
                if app.app_id not in self.SPLA_id and app.app_id not in self.LAHSA_id:
                    candidates.append(id)
        self._LAHSA_candidates = candidates
        self._LAHSA_candidates_cnt = len(candidates)

    # get application information list given application ID number
    def _get_app_info(self, id_list):
        return [self.app_info[i] for i in id_list]

    def _check_bed(self, LAHSA_tmp_id):
        LAHSA_tmp_app_info = self._get_app_info(LAHSA_tmp_id)
        days = [app.days for app in LAHSA_tmp_app_info]
        # True means still have space
        return np.all(reduce(np.add, days) <= self.b)

    def _check_parking(self, SPLA_tmp_id):
        SPLA_tmp_app_info = self._get_app_info(SPLA_tmp_id)
        days = [app.days for app in SPLA_tmp_app_info]
        # True means still have space
        return np.all(reduce(np.add, days) <= self.p)

    def solve(self):
        self._reset_SPLA_tmp()
        self._reset_LAHSA_tmp()
        self._SPLA_choose()

    def _reset_flag(self):
        if np.all(self._SPLA_tmp):
            self._SPLA_flag = True
        else:
            self._SPLA_flag = False
        if np.all(self._LAHSA_tmp):
            self._LAHSA_flag = True
        else:
            self._LAHSA_flag = False

    def _SPLA_choose(self):
        self._reset_flag()

        if self._SPLA_flag is True and self._LAHSA_flag is True:
            LAHSA_eff = self._calculate_efficiency(self._LAHSA_current_list + self.LAHSA_id,
                                                   self.b)
            SPLA_eff = self._calculate_efficiency(self._SPLA_current_list + self.SPLA_id,
                                                  self.p)
            self.resolution.append(
                {'SPLA': self._SPLA_current_list + self.SPLA_id,
                 'LAHSA': self._LAHSA_current_list + self.LAHSA_id,
                 'SPLA_eff': SPLA_eff,
                 'LAHSA_eff': LAHSA_eff})
        elif self._SPLA_flag is False:
            for i in range(self._SPLA_candidates_cnt):
                if self._SPLA_tmp[i] is False:
                    self._SPLA_tmp[i] = True
                    id = self._SPLA_candidates[i]
                    if id in self._LAHSA_candidates:
                        idx_LAHSA = self._LAHSA_candidates.index(id)
                        self._LAHSA_tmp[idx_LAHSA] = True
                    self._SPLA_current_list.append(id)
                    self._LAHSA_choose()
                    self._SPLA_current_list.pop()
                    self._SPLA_tmp[i] = False
                    if id in self._LAHSA_candidates:
                        self._LAHSA_tmp[idx_LAHSA] = False
                    self._reset_flag()

        elif self._SPLA_flag is True:
            self._LAHSA_choose()

    def _LAHSA_choose(self):
        self._reset_flag()

        if self._SPLA_flag is True and self._LAHSA_flag is True:
            LAHSA_eff = self._calculate_efficiency(self._LAHSA_current_list + self.LAHSA_id,
                                                   self.b)
            SPLA_eff = self._calculate_efficiency(self._SPLA_current_list + self.SPLA_id,
                                                  self.p)
            self.resolution.append(
                {'SPLA': self._SPLA_current_list + self.SPLA_id,
                 'LAHSA': self._LAHSA_current_list + self.LAHSA_id,
                 'SPLA_eff': SPLA_eff,
                 'LAHSA_eff': LAHSA_eff})
        elif self._LAHSA_flag is False:
            for j in range(self._LAHSA_candidates_cnt):
                if self._LAHSA_tmp[j] is False:
                    self._LAHSA_tmp[j] = True
                    id = self._LAHSA_candidates[j]
                    if id in self._SPLA_candidates:
                        idx_SPLA = self._SPLA_candidates.index(id)
                        self._SPLA_tmp[idx_SPLA] = True
                    self._LAHSA_current_list.append(id)
                    self._SPLA_choose()
                    self._LAHSA_current_list.pop()
                    self._LAHSA_tmp[j] = False
                    if id in self._SPLA_candidates:
                        self._SPLA_tmp[idx_SPLA] = False
                    self._reset_flag()
        elif self._LAHSA_flag is True:
            self._SPLA_choose()

    """
    Modification
    """

    # TODO: Modification for maximization

    def solve_modify(self):
        self._reset_SPLA_tmp()
        self._reset_LAHSA_tmp()
        self._SPLA_choose_modify()

    def _calculate_efficiency(self, app_id_list, limit):
        app_list = self._get_app_info(app_id_list)
        days = [app.days[0] for app in app_list]
        return np.sum(reduce(np.add, days)) / np.float(limit * 7)

    def _SPLA_choose_modify(self):
        self._reset_flag()
        if self._SPLA_flag is True and self._LAHSA_flag is True:
            LAHSA_eff = self._calculate_efficiency(self._LAHSA_current_list + self.LAHSA_id,
                                                   self.b)
            SPLA_eff = self._calculate_efficiency(self._SPLA_current_list + self.SPLA_id,
                                                  self.p)
            self.resolution_modify.append(
                {'SPLA': self._SPLA_current_list + self.SPLA_id,
                 'LAHSA': self._LAHSA_current_list + self.LAHSA_id,
                 'SPLA_eff': SPLA_eff,
                 'LAHSA_eff': LAHSA_eff})
        elif self._SPLA_flag is False:
            for i in range(self._SPLA_candidates_cnt):
                if self._SPLA_tmp[i] is False:
                    id = self._SPLA_candidates[i]
                    if self._check_parking(self._SPLA_current_list + [id] + self.SPLA_id):
                        self._SPLA_tmp[i] = True
                        self._SPLA_current_list.append(id)
                        if id in self._LAHSA_candidates:
                            idx_LAHSA = self._LAHSA_candidates.index(id)
                            self._LAHSA_tmp[idx_LAHSA] = True

                        self._LAHSA_choose_modify()
                        self._SPLA_current_list.pop()
                        self._SPLA_tmp[i] = False
                        if id in self._LAHSA_candidates:
                            self._LAHSA_tmp[idx_LAHSA] = False
                        self._reset_flag()

        elif self._SPLA_flag is True:
            self._LAHSA_choose_modify()

    def _LAHSA_choose_modify(self):
        self._reset_flag()
        if self._SPLA_flag is True and self._LAHSA_flag is True:
            LAHSA_eff = self._calculate_efficiency(self._LAHSA_current_list + self.LAHSA_id,
                                                   self.b)
            SPLA_eff = self._calculate_efficiency(self._SPLA_current_list + self.SPLA_id,
                                                  self.p)
            self.resolution_modify.append(
                {'SPLA': self._SPLA_current_list + self.SPLA_id,
                 'LAHSA': self._LAHSA_current_list + self.LAHSA_id,
                 'SPLA_eff': SPLA_eff,
                 'LAHSA_eff': LAHSA_eff})

        elif self._LAHSA_flag is False:
            for j in range(self._LAHSA_candidates_cnt):
                if self._LAHSA_tmp[j] is False:
                    id = self._LAHSA_candidates[j]
                    if self._check_bed(self._LAHSA_current_list + [id] + self.LAHSA_id):
                        self._LAHSA_tmp[j] = True
                        if id in self._SPLA_candidates:
                            idx_SPLA = self._SPLA_candidates.index(id)
                            self._SPLA_tmp[idx_SPLA] = True
                        self._LAHSA_current_list.append(id)
                        self._SPLA_choose_modify()
                        self._LAHSA_current_list.pop()
                        self._LAHSA_tmp[j] = False
                        if id in self._SPLA_candidates:
                            self._SPLA_tmp[idx_SPLA] = False
                        self._reset_flag()
        elif self._LAHSA_flag is True:
            self._SPLA_choose_modify()


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
    LAHSA_id_list = []
    SPLA_id_list = []
    app_info = dict()
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
                LAHSA_id_list.append(int(line.strip()))
            elif line_ct == 4 + L:
                S = int(line.strip())  # number of applicants chosen by SPLA so far
            elif line_ct <= 4 + L + S:
                SPLA_id_list.append(int(line.strip()))
            elif line_ct == 5 + L + S:
                A = int(line.strip())  # total number of applicants
            elif line_ct <= 5 + L + S + A:
                app = ApplicantInfo(line.strip())
                app_info[app.app_id] = app
    return HomelessService(b, p, L, LAHSA_id_list, S, SPLA_id_list, A, app_info)
