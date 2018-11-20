#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/18 9:47 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : utils.py
# @Software: PyCharm
from __future__ import print_function
import numpy as np
import SpeedRacer as sr
from time import time


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
                p = sr.problem_generator('./HW3_Test_Cases/input%d.txt' % case_id)
                s = time()
                p.mdp_solve()
                p.best_policy()
                ans = p.simulation()
                e = time()
                print('======================================================', file=out_f)
                print('Test File: ', end='', file=out_f)
                print('./input%d.txt' % case_id, file=out_f)
                print('[', end='', file=out_f)
                for i in range(ans.shape[0]):
                    print('%d' % ans[i], end='', file=out_f)
                    if i != ans.shape[0] - 1:
                        print(' ', end='', file=out_f)
                print(']', file=out_f)
                print('Use Time: %.10f  s' % (e - s), file=out_f)


def make_case_output():
    file = '../HW3/HW3_Test_Cases/Test Results.txt'
    path = '../HW3/HW3_Test_Cases/output'
    ln_ct = 0
    ans_dict = dict()
    for line in open(file, 'r'):
        ln_ct += 1
        if ln_ct % 5 == 2:
            tmp = line.strip().split('  ')[1]
            case_id = tmp.split('.')[1][6:]
        elif ln_ct % 5 == 3:
            ans = line.strip()
            with open(path + case_id + '.txt', 'w') as f:
                print(ans, file=f)
        else:
            continue


def make_output_compare():
    make_simulation_large_case()  # run the simulation and write the result

    file = '../HW3/HW3_Test_Cases/Test Results.txt'
    ln_ct = 0
    ans_dict = dict()
    for line in open(file, 'r'):
        ln_ct += 1
        if ln_ct % 5 == 2:
            tmp = line.strip().split('  ')[1]
            case_id = tmp.split('.')[1][6:]
        elif ln_ct % 5 == 3:
            ans = line.strip()
            ans_dict[case_id] = ans
        else:
            continue

    file = 'my_simulation.txt'
    ln_ct = 0
    for line in open(file, 'r'):
        ln_ct += 1
        if ln_ct % 4 == 2:
            tmp = line.strip().split('.')[1]
            case_id = tmp[6:]
        elif ln_ct % 4 == 3:
            ans = line.strip()
            if ans_dict[case_id] == ans:
                continue
            else:
                print('case ' + case_id + ' wrong!')
        else:
            continue
