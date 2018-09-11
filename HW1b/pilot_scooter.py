#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/10/18 11:39 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : pilot_scooter.py
# @Software: PyCharm

from __future__ import print_function
import numpy as np


class ScooterProblem(object):
    def __init__(self, N, P, S, locations):
        self.N = N  # the width and height of the n x n city area
        self.P = P  # number of police officers
        self.S = S  # number of scooters
        self.idx_location = self._make_location2(locations)
        location1 = self._make_location1(locations)  # list of S elements, each element is a 12 x 2 np.ndarray
        self.smap = SLocationMap(self.N, location1)
        self.omap = None


    def _make_location1(self, locations):
        return [locations[s:s + 12, :] for s in range(self.S)]

    def _make_location2(self, locations):
        return [[locations[t + 12 * s] for s in range(self.S)] for t in range(12)]


class SLocationMap(object):
    """location map for scooters"""

    def __init__(self, N, locations):
        self.N = N
        self.S = len(locations)
        self.bin_str_map = self._idx2bin_str(locations)
        self.int_map = self._bin_str2int(self.bin_str_map)

    def _idx2bin_str(self, locations):
        N = self.N
        bin_str_map = [['0' * N for n in range(N)] for i in range(12)]
        for scooter in locations:
            for t in range(12):
                # for each location index of scooter, [col, row]
                col = scooter[t, 0]
                row = scooter[t, 1]
                bin_str_map[t][row] = bin_str_map[t][row][:col] + '1' + bin_str_map[t][row][col + 1:]
        return bin_str_map

    def _bin_str2int(self, bin_str_map):
        N = self.N
        int_map = [[0 for n in range(N)] for i in range(12)]
        for t in range(12):
            for row in range(self.N):
                # convert bin string, like (0b)'1010', to integer with base 10, that is, 10
                int_map[t][row] = int(bin_str_map[t][row], base=2)
        return int_map


class OLocationMap(object):
    """location map for officers"""

    def __init__(self, N, location):
        self.N = N
        self.P = len(location)
        self.bin_str_map = self._idx2bin_str(location)
        self.int_map = self._bin_str2int(self.bin_str_map)

    def _idx2bin_str(self, location):
        N = self.N
        bin_str_map = ['0' * N for n in range(N)]
        for officer in location:
            # for each location index of officer, [col, row]
            col = officer[0]
            row = officer[1]
            bin_str_map[row] = bin_str_map[row][:col] + '1' + bin_str_map[row][col + 1:]
        return bin_str_map

    def _bin_str2int(self, bin_str_map):
        int_map = [0 for n in range(self.N)]
        for row in range(self.N):
            int_map[row] = int(bin_str_map[row], base=2)
        return int_map


def point_calculator(scooter_map, officer_map):
    """

    :param scooter_map: SLocationMap
    :param officer_map: OLocationMap
    :return:
    """
    points = 0
    N = scooter_map.N
    # TODO: is 'for' faster or 'map' faster????
    for row in range(N):
        for t in range(12):
            points += bin(scooter_map.int_map[t][row] & officer_map.int_map[row]).count('1')
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
