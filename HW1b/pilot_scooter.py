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
        self.smap = SLocationMap(self.N, self.sidx_location)
        self.omap = None
        self.best_point = 0
        self._cexist = None
        self._tmp_row = None
        self._tmp_col = None
        self.oidx_loc = []

    def _reset_cexist(self):
        self._cexist = [False] * self.N

    def _reset_tmp_col(self):
        self._tmp_col = [-1] * self.P

    def _make_idx_location(self, locations):
        return [[locations[t + 12 * s] for s in range(self.S)] for t in range(12)]

    def _point_calculator(self, omap):
        """

        :param smap: SLocationMap
        :param omap: OLocationMap
        :return:
        """
        # for loop is faster than map() function
        smap = self.smap
        if isinstance(omap, OLocationMap):
            point = np.sum([np.sum(np.multiply(smap.mat_map[t], omap.mat_map)) for t in range(12)])
        elif isinstance(omap, np.ndarray):
            point = np.sum([np.sum(np.multiply(smap.mat_map[t], omap)) for t in range(12)])
        return point

    def _check_conflict(self, row, col, recursive=False):
        if recursive == True and col[-1] == -1:
            ct = col.index(-1)  # if is recursive edition and col is not full
        else:
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
        for row in combinations(range(N), P):
            for col in permutations(range(N), P):
                if self._check_conflict(row, col):
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
        best_row = None
        best_col = None
        best_point = 0
        for row in combinations(range(self.N), self.P):
            self._tmp_row = row
            self._reset_cexist()
            self._reset_tmp_col()
            self._recursive_permutation(0)
        # calculate points
        for oidx in self.oidx_loc:
            if self._check_conflict(oidx['row_idx'], oidx['col_idx']):
                omat_map = idx2map(self.N, oidx['row_idx'], oidx['col_idx'])
                point = self._point_calculator(omat_map)
                if point > self.best_point:
                    self.best_point = point
                    best_row = oidx['row_idx']
                    best_col = oidx['col_idx']
        self.omap = OLocationMap(self.N, [(best_row[i], best_col[i]) for i in range(self.P)])
        return {'point': best_point, 'row_idx': best_row, 'col_idx': best_col}

    # N = n, P = m, P_tmp = cnt
    def _recursive_permutation(self, P_tmp):
        if P_tmp == self.P:
            # do not use self.oidx_loc.append(self._tmp_col) !!!!
            self.oidx_loc.append(tuple(self._tmp_col))
            return True
        for i in range(self.N):
            if self._cexist[i] is False:
                self._tmp_col[P_tmp] = i
                self._cexist[i] = True
                self._recursive_permutation(P_tmp + 1)
                self._cexist[i] = False


    def run_permutation(self):
        self._reset_cexist()
        self._reset_tmp_col()
        self._recursive_permutation(0)

    def output_result(self, out_path):
        with open(out_path, 'w') as out_f:
            print('%d' % self.best_point, end='', file=out_f)


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
