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
from numpy.random import random_sample
from numpy.random import seed
from time import time


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
        elif line_ct <= o + 3:
            tmp = line.strip().split(',')
            obstacle_loc.append([int(tmp[0]), int(tmp[1])])
        elif line_ct <= 3 + o + n:
            tmp = line.strip().split(',')
            start_loc.append([int(tmp[0]), int(tmp[1])])
        else:
            tmp = line.strip().split(',')
            end_loc.append([int(tmp[0]), int(tmp[1])])
    return SpeedRacer(s, n, o, obstacle_loc, start_loc, end_loc)


class SpeedRacer(object):
    def __init__(self, s, n, o, obstacle_loc, start_loc, end_loc):
        self.s = s
        self.n = n
        self.o = o
        self.obstacle_loc = obstacle_loc
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.Rmat = []
        self.Umat = []
        self.iter_ct = []
        self.choice = []

    def set_update_param(self, gamma=0.9, epsilon=0.1):
        self.gamma = gamma
        self.epsilon = epsilon
        self.threshold = epsilon * (1 - gamma) / gamma

    def set_reward_param(self, Rcrash=-100, Rgas=-1, Rdestination=100):
        self.Rcrash = Rcrash
        self.Rgas = Rgas
        self.Rdestination = Rdestination

    def _get_action_order(self, action):
        if action == 'N':
            act_order = ['N', 'W', 'E', 'S']
        elif action == 'S':
            act_order = ['S', 'E', 'W', 'N']
        elif action == 'E':
            act_order = ['E', 'N', 'S', 'W']
        else:
            act_order = ['W', 'S', 'N', 'E']
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

    def _init_Rmat(self, car_id):
        """
        Initialize Rmat for only one car with destination location.
        destination = [dx,dy]
        """
        s = self.s
        destination = self.end_loc[car_id]
        Rmat = np.zeros(shape=(s, s), dtype=np.float32)
        for i in range(s):
            for j in range(s):
                if [i, j] in self.obstacle_loc:  # self.obstacle_loc is a list
                    Rmat[i, j] = self.Rcrash + self.Rgas
                elif [i, j] == destination:
                    Rmat[i, j] = self.Rdestination + self.Rgas
                else:
                    Rmat[i, j] = self.Rgas
        self.Rmat.append(Rmat.astype(np.float32))

    def _init_Umat(self):
        """
        Initialize Umat to all-zero matrix.
        """
        s = self.s
        for car_id in range(self.n):
            destination = self.end_loc[car_id]
            Umat = np.zeros(shape=(s, s), dtype=np.float32)
            for i in range(s):
                for j in range(s):
                    if [i, j] in self.obstacle_loc:  # self.obstacle_loc is a list
                        Umat[i, j] = self.Rcrash + self.Rgas
                    elif [i, j] == destination:
                        Umat[i, j] = self.Rdestination + self.Rgas
                    else:
                        Umat[i, j] = self.Rgas
            self.Umat.append(Umat.astype(np.float32))

    def _map_Utensor(self, car_id):
        """
        map Umat to Utensor for update of the next generation
        """
        s = self.s
        self.Utensor = np.zeros(shape=(s, s, 4, 4), dtype=np.float32)
        for i in range(s):
            i_slice = self.next_state_ltensor[i]
            for j in range(s):
                j_tuple = i_slice[j]
                if [i, j] != self.end_loc[car_id]:
                    for ii in range(4):
                        for jj in range(4):
                            index = j_tuple[ii][jj]
                            self.Utensor[i, j, ii, jj] = self.Umat[car_id][index[0], index[1]]

    def _Umat_convergence(self, car_id, Umat):
        s = self.s
        assert Umat.shape == (s, s)
        delta_Umat = np.abs(Umat - self.Umat[car_id], dtype=np.float32)
        max_delta_U = np.max(delta_Umat)
        if max_delta_U > self.threshold:
            return False  # not convergent yet
        else:
            return True  # already convergent

    def _init_Ptensor(self, car_id):
        """
        Initialize Ptensor with [0.7, 0.1, 0.1, 0.1] for each action,
        except the destination location with [1, 1, 1, 1].
        """
        s = self.s
        destination = self.end_loc[car_id]
        self.Ptensor = np.ones(shape=(s, s, 4, 4), dtype=np.float32)
        self.Ptensor[:, :, :, 0] *= 0.7
        self.Ptensor[:, :, :, 1:] *= 0.1
        dx = destination[0]
        dy = destination[1]
        self.Ptensor[dx, dy, :, :] /= np.array(
            [[0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1]])

    def mdp_solve(self):
        self.set_update_param()
        self.set_reward_param()
        self._init_Umat()
        self._make_state_move_tensor()
        for i in range(self.n):
            self.value_iteration_one_car(car_id=i)

    def value_iteration_one_car(self, car_id):
        s = self.s
        self._init_Rmat(car_id)
        self._init_Ptensor(car_id)
        Umat_tmp = np.zeros(shape=(s, s), dtype=np.float32)
        Utmp = np.zeros(shape=(s, s, 4), dtype=np.float32)

        iter_ct = 0
        while True:
            iter_ct += 1
            self._map_Utensor(car_id)
            Utmp = np.sum(self.Utensor * self.Ptensor, axis=3)
            Umat_tmp = self.gamma * np.max(Utmp, axis=2) + self.Rmat[car_id]
            if self._Umat_convergence(car_id, Umat_tmp):
                self.Umat[car_id] = Umat_tmp.copy()
                self.iter_ct.append(iter_ct)
                break
            self.Umat[car_id] = Umat_tmp.copy()

    def best_policy(self):
        self.action_map = []
        self.action_char_map = []
        for id in range(self.n):
            self.best_policy_one_car(id)

    def best_policy_one_car(self, car_id):
        self._map_Utensor(car_id)
        self._init_Ptensor(car_id)
        expect_U = np.sum(self.Utensor * self.Ptensor, axis=3)
        choice = np.argmax(expect_U, axis=2)
        self.choice.append(choice)
        self._to_move(car_id, choice)

    def _to_move(self, car_id, choice):
        act_list = ['N', 'S', 'E', 'W']
        act_char_list = ['^', 'v', '>', '<']
        s = self.s
        destination = self.end_loc[car_id]
        act_map = [[None for ii in range(s)] for jj in range(s)]
        act_char_map = [[None for ii in range(s)] for jj in range(s)]
        for i in range(s):
            for j in range(s):
                if [i, j] != destination:
                    action = act_list[choice[i, j]]
                    action_char = act_char_list[choice[i, j]]
                    act_map[i][j] = action
                    act_char_map[i][j] = action_char
        act_map[destination[0]][destination[1]] = 'X'
        act_char_map[destination[0]][destination[1]] = 'X'
        self.action_map.append(act_map)
        self.action_char_map.append(act_char_map)

    def print_policy(self, car_id):
        s = self.s
        for i in range(s):
            for j in range(s):
                print(self.action_char_map[car_id][j][i], end=' ')  # reverse the order of x and y!!
            print('')
        print('')

    def simulation(self):
        track = [[[] for i in range(10)] for car_id in range(self.n)]
        move_track = [[[] for i in range(10)] for car_id in range(self.n)]
        score = np.zeros(shape=(self.n))
        for i in range(10):
            seed(i)
            p_list = random_sample(1000000)
            for car_id in range(self.n):
                choice = self.choice[car_id]
                cur_pos = self.start_loc[car_id]
                destination = self.end_loc[car_id]
                best_action_map = self.action_map[car_id]
                step_ct = 0
                while cur_pos != destination:
                    x = cur_pos[0]
                    y = cur_pos[1]
                    best_act_id = choice[x, y]
                    if p_list[step_ct] <= 0.7:
                        next_pos = self.next_state_ltensor[x][y][best_act_id][0]
                        move = self.move_ltensor[x][y][best_act_id][0]
                    elif p_list[step_ct] <= 0.8:
                        next_pos = self.next_state_ltensor[x][y][best_act_id][1]
                        move = self.move_ltensor[x][y][best_act_id][1]
                    elif p_list[step_ct] <= 0.9:
                        next_pos = self.next_state_ltensor[x][y][best_act_id][2]
                        move = self.move_ltensor[x][y][best_act_id][2]
                    else:
                        next_pos = self.next_state_ltensor[x][y][best_act_id][3]
                        move = self.move_ltensor[x][y][best_act_id][3]
                    track[car_id][i].append(cur_pos)
                    move_track[car_id][i].append(move)
                    cur_pos = next_pos
                    score[car_id] += self.Rmat[car_id][cur_pos[0], cur_pos[1]]
                    step_ct += 1
        score = np.floor(score / 10)
        return score.astype(int)


def move_to_char(move):
    if move == [0, -1]:
        return '^'
    if move == [-1, 0]:
        return '<'
    if move == [1, 0]:
        return '>'
    if move == [0, 1]:
        return 'v'


def index_parse(index_str):
    index = index_str[1:-1].split(', ')
    return [int(index[0]), int(index[1])]


def policy_parse(in_path, s):
    policy = [[None for jj in range(s)] for kk in range(s)]
    for line in open(in_path, 'r'):
        tmp = line.strip().split(': ')
        idx = index_parse(tmp[0])
        if tmp[1] == 'None':
            policy[idx[0]][idx[1]] = 'X'
        else:
            move = index_parse(tmp[1])
            policy[idx[0]][idx[1]] = move_to_char(move)
    for i in range(s):
        for j in range(s):
            print(policy[j][i], end=' ')
        print('')
    print('')
    return policy


def answer_read(in_path):
    ans = []
    print('[', end='')
    for line in open(in_path, 'r'):
        ans.append(int(line.strip()))
    for a in ans:
        print('%d, ' % a, end='')
    print(']', end='')
    print('')
    return ans


def make_simulation_large_case():
    out_path = './my_simulation.txt'
    with open(out_path, 'w') as out_f:
        for case_id in range(47):
            if case_id != 11:
                p = problem_generator('./HW3_Test_Cases/input%d.txt' % case_id)
                s = time()
                p.mdp_solve()
                p.best_policy()
                ans = p.simulation()
                e = time()
                print('======================================================', file=out_f)
                print('Test File: ', end='', file=out_f)
                print('./input%d.txt' % case_id, file=out_f)
                print(ans, file=out_f)
                print('Use Time: %.10f  s' % (e - s), file=out_f)

                print('======================================================')
                print('Test File: ', end='')
                print('./input%d.txt' % case_id)
                print(ans)
                print('Use Time: %.10f  s' % (e - s))
