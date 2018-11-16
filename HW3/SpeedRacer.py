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

    def idx_trans(self, index, action):
        """
        Return index list [(x1,y1), (x2,y2), (x3,y3), (x4,y4)] and moving []
        after action applied on original index.

        If action='N',
        (x1,y1) is the index after moving toward North with probability 0.7, (prob <= 0.7)
        (x2,y2) is the index after moving toward East with probability 0.1, (0.7 < prob <= 0.8)
        (x3,y3) is the index after moving toward West with probability 0.1, (0.8 < prob <= 0.9)
        (x4,y4) is the index after moving toward South with probability 0.1; (0.9 < prob <= 1.0)

        If action='S',
        (x1,y1) is the index after moving toward South with probability 0.7, (prob <= 0.7)
        (x2,y2) is the index after moving toward West with probability 0.1, (0.7 < prob <= 0.8)
        (x3,y3) is the index after moving toward East with probability 0.1, (0.8 < prob <= 0.9)
        (x4,y4) is the index after moving toward North with probability 0.1; (0.9 < prob <= 1.0)

        If action='E',
        (x1,y1) is the index after moving toward East with probability 0.7, (prob <= 0.7)
        (x2,y2) is the index after moving toward South with probability 0.1, (0.7 < prob <= 0.8)
        (x3,y3) is the index after moving toward North with probability 0.1, (0.8 < prob <= 0.9)
        (x4,y4) is the index after moving toward West with probability 0.1; (0.9 < prob <= 1.0)

        If action='W',
        (x1,y1) is the index after moving toward West with probability 0.7, (prob <= 0.7)
        (x2,y2) is the index after moving toward North with probability 0.1, (0.7 < prob <= 0.8)
        (x3,y3) is the index after moving toward South with probability 0.1, (0.8 < prob <= 0.9)
        (x4,y4) is the index after moving toward East with probability 0.1; (0.9 < prob <= 1.0)
        """
        if index[0] == 0 and index[1] == 0:  # case 1
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == 0 and index[1] == self.n - 1:  # case 2
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == self.n - 1 and index[1] == 0:  # case 3
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and index[1] == self.n - 1:  # case 4
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[1] == 0 and 0 < index[0] < self.n - 1:  # case 5
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == 0 and 0 < index[1] < self.n - 1:  # case 6
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[1] == self.n - 1 and 0 < index[0] < self.n - 1:  # case 7
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and 0 < index[1] < self.n - 1:  # case 8
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        else:  # case 9
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}

    # TODO: speed
    def trans_numpy1(self, index, action):
        if index[0] == 0 and index[1] == 0:  # case 1
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == 0 and index[1] == self.n - 1:  # case 2
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == self.n - 1 and index[1] == 0:  # case 3
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and index[1] == self.n - 1:  # case 4
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[1] == 0 and 0 < index[0] < self.n - 1:  # case 5
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == 0 and 0 < index[1] < self.n - 1:  # case 6
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[1] == self.n - 1 and 0 < index[0] < self.n - 1:  # case 7
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and 0 < index[1] < self.n - 1:  # case 8
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        else:  # case 9
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}

        if action == 'N':
            return {'move': np.array([act_dict['N'], act_dict['E'], act_dict['W'], act_dict['S']]),
                    'index': np.array(
                        [index + act_dict['N'], index + act_dict['E'], index + act_dict['W'], index + act_dict['S']])}
        elif action == 'S':
            return {'move': np.array([act_dict['S'], act_dict['W'], act_dict['E'], act_dict['N']]),
                    'index': np.array(
                        [index + act_dict['S'], index + act_dict['W'], index + act_dict['E'], index + act_dict['N']])}
        elif action == 'E':
            return {'move': np.array([act_dict['E'], act_dict['S'], act_dict['N'], act_dict['W']]),
                    'index': np.array(
                        [index + act_dict['E'], index + act_dict['S'], index + act_dict['N'], index + act_dict['W']])}
        else:
            return {'move': np.array([act_dict['W'], act_dict['N'], act_dict['S'], act_dict['E']]),
                    'index': np.array(
                        [index + act_dict['W'], index + act_dict['N'], index + act_dict['S'], index + act_dict['E']])}

    # TODO: speed
    def trans_numpy2(self, index, action):
        if index[0] == 0 and index[1] == 0:  # case 1
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == 0 and index[1] == self.n - 1:  # case 2
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[0] == self.n - 1 and index[1] == 0:  # case 3
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and index[1] == self.n - 1:  # case 4
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        elif index[1] == 0 and 0 < index[0] < self.n - 1:  # case 5
            act_dict = {'N': np.array([0, 0]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == 0 and 0 < index[1] < self.n - 1:  # case 6
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([0, 0])}
        elif index[1] == self.n - 1 and 0 < index[0] < self.n - 1:  # case 7
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 0]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}
        elif index[0] == self.n - 1 and 0 < index[1] < self.n - 1:  # case 8
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([0, 0]), 'W': np.array([-1, 0])}
        else:  # case 9
            act_dict = {'N': np.array([0, -1]), 'S': np.array([0, 1]), 'E': np.array([1, 0]), 'W': np.array([-1, 0])}

        if action == 'N':
            # return index + np.array([act_dict['N'],act_dict['E'],act_dict['W'],act_dict['S']])
            return {'move': np.array([act_dict['N'], act_dict['E'], act_dict['W'], act_dict['S']]),
                    'index': index + np.array([act_dict['N'], act_dict['E'], act_dict['W'], act_dict['S']])}
        elif action == 'S':
            # return index + np.array([act_dict['S'],act_dict['W'],act_dict['E'],act_dict['N']])
            return {'move': np.array([act_dict['S'], act_dict['W'], act_dict['E'], act_dict['N']]),
                    'index': index + np.array([act_dict['S'], act_dict['W'], act_dict['E'], act_dict['N']])}
        elif action == 'E':
            # return index + np.array([act_dict['E'],act_dict['S'],act_dict['N'],act_dict['W']])
            return {'move': np.array([act_dict['E'], act_dict['S'], act_dict['N'], act_dict['W']]),
                    'index': index + np.array([act_dict['E'], act_dict['S'], act_dict['N'], act_dict['W']])}
        else:
            # return index + np.array([act_dict['W'],act_dict['N'],act_dict['S'],act_dict['E']])
            return {'move': np.array([act_dict['W'], act_dict['N'], act_dict['S'], act_dict['E']]),
                    'index': index + np.array([act_dict['W'], act_dict['N'], act_dict['S'], act_dict['E']])}

    # TODO: speed
    def trans_list(self, index, action):
        if index[0] == 0 and index[1] == 0:  # case 1
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [1, 0], 'W': [0, 0]}
        elif index[0] == 0 and index[1] == self.n - 1:  # case 2
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [1, 0], 'W': [0, 0]}
        elif index[0] == self.n - 1 and index[1] == 0:  # case 3
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [0, 0], 'W': [-1, 0]}
        elif index[0] == self.n - 1 and index[1] == self.n - 1:  # case 4
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [0, 0], 'W': [-1, 0]}
        elif index[1] == 0 and 0 < index[0] < self.n - 1:  # case 5
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [1, 0], 'W': [-1, 0]}
        elif index[0] == 0 and 0 < index[1] < self.n - 1:  # case 6
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [1, 0], 'W': [0, 0]}
        elif index[1] == self.n - 1 and 0 < index[0] < self.n - 1:  # case 7
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [1, 0], 'W': [-1, 0]}
        elif index[0] == self.n - 1 and 0 < index[1] < self.n - 1:  # case 8
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [0, 0], 'W': [-1, 0]}
        else:  # case 9
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [1, 0], 'W': [-1, 0]}

        if action == 'N':
            # TODO
            new_index = []
            pass
        elif action =='S':
            # TODO
            pass
        elif action == 'E':
            # TODO
            pass
        else:
            # TODO
            pass




    def _map_grid(self):
        grid_list = []

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
