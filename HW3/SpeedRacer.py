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

    def set_update_param(self, gamma=0.9, epsilon=0.1):
        self.gamma = gamma
        self.epsilon = epsilon
        self.threshold = epsilon * (1 - gamma) / gamma

    def set_reward_param(self, Rcrash=-100, Rgas=-1, Rdestination=100):
        self.Rcrash = Rcrash
        self.Rgas = Rgas
        self.Rdestination = Rdestination

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

    def _idx_trans(self, index, action):
        """
        Return index list [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] after action applied on original index,
        and movement [[delta_x1,delta_y1], [delta_x2,delta_y2], [delta_x3,delta_y3], [delta_x4,delta_y4]]


        If action='N',
        [x1,y1] is the index after moving toward North with probability 0.7, (prob <= 0.7)
        [x2,y2] is the index after moving toward West with probability 0.1, (0.7 < prob <= 0.8)
        [x3,y3] is the index after moving toward East with probability 0.1, (0.8 < prob <= 0.9)
        [x4,y4] is the index after moving toward South with probability 0.1; (0.9 < prob <= 1.0)

        If action='S',
        [x1,y1] is the index after moving toward South with probability 0.7, (prob <= 0.7)
        [x2,y2] is the index after moving toward East with probability 0.1, (0.7 < prob <= 0.8)
        [x3,y3] is the index after moving toward West with probability 0.1, (0.8 < prob <= 0.9)
        [x4,y4] is the index after moving toward North with probability 0.1; (0.9 < prob <= 1.0)

        If action='E',
        [x1,y1] is the index after moving toward East with probability 0.7, (prob <= 0.7)
        [x2,y2] is the index after moving toward North with probability 0.1, (0.7 < prob <= 0.8)
        [x3,y3] is the index after moving toward South with probability 0.1, (0.8 < prob <= 0.9)
        [x4,y4] is the index after moving toward West with probability 0.1; (0.9 < prob <= 1.0)

        If action='W',
        [x1,y1] is the index after moving toward West with probability 0.7, (prob <= 0.7)
        [x2,y2] is the index after moving toward South with probability 0.1, (0.7 < prob <= 0.8)
        [x3,y3] is the index after moving toward North with probability 0.1, (0.8 < prob <= 0.9)
        [x4,y4] is the index after moving toward East with probability 0.1; (0.9 < prob <= 1.0)
        """
        act_dict = self._get_action_dict(index)
        act_order = self._get_action_order(action)
        return {'index': [[index[i] + act_dict[d][i] for i in range(2)] for d in act_order],
                'move': [act_dict[d] for d in act_order]}

    def _make_state_move_tensor(self):
        """
        make lists for movement and next state index for any possible actions,
        can be used for all cars.
        """
        actions = ['N', 'S', 'E', 'W']
        self.next_state_ltensor = []
        self.move_ltensor = []
        s = self.s
        for i in range(s):
            move_i_row = []
            state_i_row = []
            for j in range(s):
                move_j_column = []
                state_j_column = []
                for a in range(4):
                    action = actions[a]
                    ans = self._idx_trans([i, j], action)
                    move_j_column.append(ans['move'])
                    state_j_column.append(ans['index'])
                move_i_row.append(move_j_column)
                state_i_row.append(state_j_column)
            self.next_state_ltensor.append(state_i_row)
            self.move_ltensor.append(move_i_row)

    def _init_Rmat(self, destination):
        """
        Initialize Rmat for only one car with destination location.
        destination = [dx,dy]
        """
        s = self.s
        Rmat = np.zeros(shape=(s, s))
        for i in range(s):
            for j in range(s):
                if [i, j] in self.obstacle_loc:  # self.obstacle_loc is a list
                    Rmat[i, j] = self.Rcrash + self.Rgas
                elif [i, j] == destination:
                    Rmat[i, j] = self.Rdestination + self.Rgas
                else:
                    Rmat[i, j] = self.Rgas
        self.Rmat = Rmat

    # def _set_Rtensor(self):
    #     s = self.s
    #     Rtensor = np.zeros(shape=(s, s, 4, 4))
    #     for i in range(s):
    #         i_slice = self.next_state_ltensor[i]
    #         for j in range(s):
    #             j_tuple = i_slice[j]
    #             for ii in range(4):
    #                 for jj in range(4):
    #                     index = j_tuple[ii][jj]
    #                     Rtensor[i, j, ii, jj] = self._Rmat[index[0], index[1]]
    #     self.Rtensor = Rtensor

    def _init_Umat(self):
        """
        Initialize Umat to all-zero matrix before the value iteration algorithm.
        """
        s = self.s
        self.Umat = np.zeros(shape=(s, s))

    def _map_Utensor(self, destination):
        """
        map Umat to Utensor for update of the next generation
        """
        s = self.s
        self.Utensor = np.zeros(shape=(s, s, 4, 4))
        for i in range(s):
            i_slice = self.next_state_ltensor[i]
            for j in range(s):
                j_tuple = i_slice[j]
                if [i, j] != destination:
                    for ii in range(4):
                        for jj in range(4):
                            index = j_tuple[ii][jj]
                            self.Utensor[i, j, ii, jj] = self.Umat[index[0], index[1]]

    def _Umat_convergence(self, Umat):
        s = self.s
        assert Umat.shape == (s, s)
        delta_Umat = np.abs(Umat - self.Umat)
        max_delta_U = np.max(delta_Umat)
        if max_delta_U > self.threshold:
            return False  # not convergent yet
        else:
            return True  # already convergent

    def _init_Ptensor(self, destination):
        """
        Initialize Ptensor with [0.7, 0.1, 0.1, 0.1] for each action,
        except the destination location with [1, 1, 1, 1].
        """
        s = self.s
        self.Ptensor = np.ones(shape=(s, s, 4, 4), dtype=float)
        self.Ptensor[:, :, :, 0] *= 0.7
        self.Ptensor[:, :, :, 1:] *= 0.1
        dx = destination[0]
        dy = destination[1]
        self.Rtensor[dx, dy, :, :] /= np.array(
            [[0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1]])

    def mdp_solve(self):
        self.set_update_param()
        self.set_reward_param()
        self._make_state_move_tensor()
        for i in range(self.n):
            self.value_iteration_one_car(start=self.start_loc[i], destination=self.end_loc[i])

    def value_iteration_one_car(self, start, destination):
        self._init_Rmat(destination)
        self._init_Ptensor(destination)
        while True:
            self._map_Utensor(destination)


def problem_generator(in_path):
    # using list is 3-4 times faster than using Numpy.load()
    line_ct = 0
    obstacle_loc = []
    start_loc = []
    end_loc = []
    for line in open(in_path, 'r'):
        line_ct += 1
        if line_ct == 1:
            s = int(line.strip())  # size of grid
        elif line_ct == 2:
            n = int(line.strip())  # number of cars
        elif line_ct == 3:
            o = int(line.strip())  # number of obstacles
        elif line_ct < o + 3:
            tmp = line.strip().split(',')
            obstacle_loc.append([int(tmp[0]), int(tmp[1])])
        elif line_ct < 3 + o + n:
            tmp = line.strip().split(',')
            start_loc.append([int(tmp[0]), int(tmp[1])])
        else:
            tmp = line.strip().split(',')
            end_loc.append([int(tmp[0]), int(tmp[1])])
    return SpeedRacer(s, n, o, obstacle_loc, start_loc, end_loc)
