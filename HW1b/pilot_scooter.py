#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/10/18 11:39 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : pilot_scooter.py
# @Software: PyCharm

from __future__ import print_function
from copy import copy
import numpy as np
from itertools import combinations, permutations

CUT_OFF = -1


class ScooterProblem(object):
    def __init__(self, N, P, S, scooter_locations):
        self.N = N  # the width and height of the n x n city area
        self.P = P  # number of police officers
        self.S = S  # number of scooters
        # list of 12 elements, each element is 5 2x1 np.ndarray
        self.sidx_location = self._make_idx_location(scooter_locations)
        self._smap = self._make_smap()  # add up all smap to speed up point calculation
        self.omap = None
        self.best_point = 0
        self._cexist = None
        self._tmp_row = None
        self._tmp_col = None
        self.oidx_loc = []

    def _make_smap(self):
        smap = SLocationMap(self.N, self.sidx_location)
        return reduce(np.add, smap.mat_map)

    def _reset_cexist(self):
        self._cexist = [False] * self.N

    def _reset_tmp_col(self):
        self._tmp_col = [-1] * self.P

    def _make_idx_location(self, locations):
        return [[locations[t + 12 * s] for s in range(self.S)] for t in range(12)]

    def _max_point_estimate(self, P_tmp):
        omat_map = idx2map(self.N, self._tmp_row[:P_tmp + 1], self._tmp_col[:P_tmp + 1])
        cur_point = self._point_calculator(omat_map)
        future_max = np.sum(np.max(self._smap[self._tmp_row[P_tmp + 1:], :], axis=1))
        return cur_point + future_max

    def _point_calculator(self, omap):
        """

        :param smap: SLocationMap
        :param omap: OLocationMap
        :return:
        """
        # for loop is faster than map() function
        if isinstance(omap, OLocationMap):
            point = np.sum(np.multiply(self._smap, omap.mat_map))
        elif isinstance(omap, np.ndarray):
            point = np.sum(np.multiply(self._smap, omap))
        return point

    def _check_conflict(self, row, col):
        ct = len(col)
        if ct >= 2:
            for i in range(ct - 1):
                for j in range(i + 1, ct):
                    if abs(row[i] - row[j]) == abs(col[i] - col[j]):
                        return False
        return True

    def solve_stupid(self):
        best_row = None
        best_col = None
        best_point = 0
        N = self.N
        P = self.P
        omat_map = np.zeros(shape=(N, N))
        for row in combinations(range(N), P):
            for col in permutations(range(N), P):
                if self._check_conflict(row, col):
                    self.oidx_loc.append({'row_idx': tuple(row), 'col_idx': tuple(col)})
                    omat_map = idx2map(N, row, col)
                    point = self._point_calculator(omat_map)
                    if point > best_point:
                        best_point = point
                        best_col = col
                        best_row = row
        self.omap = OLocationMap(self.N, mat_map=omat_map)
        self.best_point = best_point
        return {'point': best_point, 'row_idx': best_row, 'col_idx': best_col}

    def solve_smart(self):
        for row in combinations(range(self.N), self.P):
            self._tmp_row = row
            self._reset_cexist()
            self._reset_tmp_col()
            self._recursive_dfs(0)
        # calculate points
        self.omap = OLocationMap(self.N,
                                 [(self.oidx_loc['row_idx'][i], self.oidx_loc['col_idx'][i]) for i in range(self.P)])
        return self.best_point

    def _recursive_dfs(self, P_tmp):
        if P_tmp == self.P:
            # do not use self.oidx_loc.append(self._tmp_col) !!!!
            if self._check_conflict(self._tmp_row, self._tmp_col):
                omat_map = idx2map(self.N, self._tmp_row, self._tmp_col)
                point = self._point_calculator(omat_map)
                if point > self.best_point:
                    self.best_point = point
                    self.oidx_loc = {'row_idx': tuple(self._tmp_row), 'col_idx': tuple(self._tmp_col)}
        else:
            for i in range(self.N):
                if self._cexist[i] is False:
                    self._tmp_col[P_tmp] = i
                    if self._check_conflict(self._tmp_row[:P_tmp + 1], self._tmp_col[:P_tmp + 1]):
                        if self._max_point_estimate(P_tmp) >= self.best_point:
                            self._cexist[i] = True
                            self._recursive_dfs(P_tmp + 1)
                            self._cexist[i] = False
                    else:
                        self._tmp_col[P_tmp] = -1

    def output_result(self, out_path):
        with open(out_path, 'w') as out_f:
            print('%d' % self.best_point, file=out_f)


class SLocationMap(object):
    """location map for scooters"""

    def __init__(self, N, idx_location):
        """

        :param N:
        :param idx_location: list with length 12, each element is self.S 2x1 np.ndarray
        """
        self.N = N
        self.S = len(idx_location)
        self.mat_map = self._idx2map(idx_location)

    def _idx2map(self, idx_locations):
        mat_map = [np.zeros(shape=(self.N, self.N), dtype=np.uint8) for t in range(12)]
        for t in range(12):
            for scooter in idx_locations[t]:
                col = scooter[0]
                row = scooter[1]
                mat_map[t][row, col] += 1
        return mat_map


class OLocationMap(object):
    """location map for officers"""

    def __init__(self, N, idx_location=None, mat_map=None):
        self.N = N
        if idx_location is not None and mat_map is None:
            self.P = len(idx_location)
            self.mat_map = self._idx2map(idx_location)
        elif idx_location is None and mat_map is not None:
            self.P = sum(mat_map)
            self.mat_map = mat_map

    def _idx2map(self, idx_location):
        """

        :param idx_location: list of length self.P, each element is a 2x1 np.ndarry
        :return:
        """
        mat_map = np.zeros(shape=(self.N, self.N), dtype=np.uint8)
        for officer in idx_location:
            col = officer[0]
            row = officer[1]
            mat_map[row, col] = 1
        return mat_map


def problem_generator(in_path):
    line_ct = 0
    for line in open(in_path, 'r'):
        line_ct += 1
        if line_ct == 1:
            N = int(line.strip())  # the width and height of the N x N city area
        elif line_ct == 2:
            P = int(line.strip())  # number of police officers
        elif line_ct == 3:
            S = int(line.strip())  # number of scooters
    locations = np.loadtxt(in_path, np.int, delimiter=',', skiprows=3)
    return ScooterProblem(N, P, S, locations)


def idx2map(N, row_idx, col_idx):
    P = len(row_idx)
    mat_map = np.zeros(shape=(N, N), dtype=np.uint8)
    for i in range(P):
        mat_map[row_idx[i], col_idx[i]] = 1
    return mat_map
