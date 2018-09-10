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
        self.location = self._make_location(locations)  # list of S elements, each element is a 12 x 2 np.ndarray

    def _make_location(self, locations):
        return [locations[s:s + 12, :] for s in range(self.S)]


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
