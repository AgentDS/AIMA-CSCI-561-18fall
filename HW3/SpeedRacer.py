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

    # TODO: THE CORRECTED VRSION
    # def _get_action_order(self, action):
    #     if action == 'N':
    #         act_order = ['N', 'W', 'E', 'S']
    #     elif action == 'S':
    #         act_order = ['S', 'E', 'W', 'N']
    #     elif action == 'E':
    #         act_order = ['E', 'N', 'S', 'W']
    #     else:
    #         act_order = ['W', 'S', 'N', 'E']
    #     return act_order

    # TODO: THE WRONG VRSION
    def _get_action_order(self, action):
        if action == 'N':
            act_order = ['N', 'W', 'E', 'S', 'S']
        elif action == 'S':
            act_order = ['S', 'E', 'W', 'N', 'N']
        elif action == 'E':
            act_order = ['E', 'N', 'S', 'W', 'W']
        else:
            act_order = ['W', 'S', 'N', 'E', 'E']
        return act_order

    def _get_action_dict(self, index):
        if index[0] == 0 and index[1] == 0:  # case 1
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [1, 0], 'W': [0, 0]}
        elif index[0] == 0 and index[1] == self.s - 1:  # case 2
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [1, 0], 'W': [0, 0]}
        elif index[0] == self.s - 1 and index[1] == 0:  # case 3
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [0, 0], 'W': [-1, 0]}
        elif index[0] == self.s - 1 and index[1] == self.s - 1:  # case 4
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [0, 0], 'W': [-1, 0]}
        elif index[1] == 0 and 0 < index[0] < self.s - 1:  # case 5
            act_dict = {'N': [0, 0], 'S': [0, 1], 'E': [1, 0], 'W': [-1, 0]}
        elif index[0] == 0 and 0 < index[1] < self.s - 1:  # case 6
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [1, 0], 'W': [0, 0]}
        elif index[1] == self.s - 1 and 0 < index[0] < self.s - 1:  # case 7
            act_dict = {'N': [0, -1], 'S': [0, 0], 'E': [1, 0], 'W': [-1, 0]}
        elif index[0] == self.s - 1 and 0 < index[1] < self.s - 1:  # case 8
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [0, 0], 'W': [-1, 0]}
        else:  # case 9
            act_dict = {'N': [0, -1], 'S': [0, 1], 'E': [1, 0], 'W': [-1, 0]}
        return act_dict

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
        act_dict = self._get_action_dict(index)

    # TODO: speed
    def trans_numpy(self, index, action):
        act_dict = self._get_action_dict(index)
        act_order = self._get_action_order(action)
        move = np.array([act_dict[d] for d in act_order], dtype=int)
        return {'move': move, 'index': index.astype(int) + move}

    # TODO: speed
    def trans_list(self, index, action):
        act_dict = self._get_action_dict(index)
        act_order = self._get_action_order(action)
        return {'index': [[index[i] + act_dict[d][i] for i in range(2)] for d in act_order],
                'move': [act_dict[d] for d in act_order]}

    # def _map_grid(self):
    #     grid_list = []

    def _make_Rmat(self):
        s = self.s
        Rmat = np.zeros(shape=(s, s))
        for i in range(s):
            for j in range(s):
                if [i, j] in self.obstacle_loc:  # self.obstacle_loc is a list
                    Rmat[i, j] = -101
                elif [i, j] == self.destination:
                    Rmat[i, j] = 99
                else:
                    Rmat[i, j] = -1
        self._Rmat = Rmat

    def _make_Rtensor(self):
        s = self.s
        Rtensor = np.zeros(shape=(s, s, 4, 4))
        for i in range(s):
            i_slice = self._next_state_ltensor[i]   # TODO: Need to clearify 'self._next_state_ltensor'
            for j in range(s):
                j_tuple = i_slice[j]
                for ii in range(4):
                    for jj in range(4):
                        index = j_tuple[ii][jj]
                        Rtensor[i, j, ii, jj] = self._Rmat[index[0], index[1]]
        self._Rtensor = Rtensor

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
