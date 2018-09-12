#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/10/18 11:39 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : pilot_scooter.py
# @Software: PyCharm

from __future__ import print_function
import numpy as np
from itertools import combinations


class ScooterProblem(object):
    def __init__(self, N, P, S, scooter_locations):
        self.N = N  # the width and height of the n x n city area
        self.P = P  # number of police officers
        self.S = S  # number of scooters
        # list of 12 elements, each element is 5 2x1 np.ndarray
        self.sidx_location = self._make_idx_location(scooter_locations)
        self.smap = SLocationMap(self.N, self.sidx_location)
        self.omap = None

    def _make_idx_location(self, locations):
        return [[locations[t + 12 * s] for s in range(self.S)] for t in range(12)]


def office_solver(N, P):
    if N > P:
        all_row_combs = list(combinations(range(N), P))
        for row_comb in all_row_combs:



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
            self.P = sum(mat_map)
            self.mat_map = self._idx2map(idx_location)
        elif idx_location is None and mat_map is not None:
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
            mat_map[row, col] += 1
        return mat_map


def point_calculator(smap, omap):
    """

    :param smap: SLocationMap
    :param omap: OLocationMap
    :return:
    """
    # for loop is faster than map() function
    points = np.sum([np.sum(np.multiply(smap.mat_map[t], omap.mat_map)) for t in range(12)])
    return points


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


def problem_output(m, out_path):
    with open(out_path, 'w') as out_f:
        print('%d' % m, end='', file=out_f)


def scooter_plot(problem):
    N = problem.N
    P = problem.P
    S = problem.S
    # TODO: plot the map in matplotlib?
