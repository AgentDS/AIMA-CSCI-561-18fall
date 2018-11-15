#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/13/18 10:22 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : SpeedRacer.py
# @Software: PyCharm

from __future__ import print_function
from copy import copy
import numpy as np
from itertools import combinations, permutations


class SpeedRacer(object):
    def __init__(self, s, n, o, obstacle_loc, start_loc, end_loc):
        self.s = s
        self.n = n
        self.o = o
        self.obstacle_loc = obstacle_loc
        self.start_loc = start_loc
        self.end_loc = end_loc

    def set_reward(self, crash=-100, gas=-1, destination=100):
        self.crash = crash
        self.gas = gas
        self.destination = destination

    def mdp_solve(self):
        pass


def problem_generator(in_path):
    line_ct = 0
    for line in open(in_path, 'r'):
        line_ct += 1
        if line_ct == 1:
            s = int(line.strip())  # size of grid
        elif line_ct == 2:
            n = int(line.strip())  # number of cars
        elif line_ct == 3:
            o = int(line.strip())  # number of obstacles
            break
    location = np.loadtxt(in_path, np.int, delimiter=',', skiprows=3)
    obstacle_loc = location[:o, :]  # the location of obstacles
    start_loc = location[o:o + n, :]
    end_loc = location[o + n:, :]
    return SpeedRacer(s, n, o, obstacle_loc, start_loc, end_loc)


