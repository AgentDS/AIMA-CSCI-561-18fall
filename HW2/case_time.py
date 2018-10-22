#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/18/18 3:25 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : case_time.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 5:54 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw2cs561f2018.py
# @Software: PyCharm
from __future__ import print_function
import homeless_service as hs
import time


def case_time(in_path, method):
    answer = {'input0.txt': 1,
              'input1.txt': 3,
              'input2.txt': 4,
              'input6.txt': 1,
              'input7.txt': 3,
              'input8.txt': 6,
              'input10_1.txt': 1,
              'input10_2.txt': 3,
              'input20.txt': 1,
              'input21.txt': 5,
              'input25.txt': 4}

    problem = hs.problem_generator(in_path)
    path = in_path + (13 - len(in_path)) * ' '
    print("case: ", path, end=' ')
    if method == 0:
        s = time.time()
        try:
            problem.solve()
            e = time.time()
            if problem.SPLA_best_first_id == answer[in_path]:
                msg = 'OK,'
            else:
                msg = 'Err,'
            print('..', msg, "SPLA ID: ", problem.SPLA_best_first_id, ", time = %10f s" % (e - s))
        except TypeError:
            print("'NoneType' object has no attribute '__getitem__'")
    else:
        s = time.time()
        try:
            problem.solve_modify()
            e = time.time()
            if problem.SPLA_best_first_id == answer[in_path]:
                msg = 'OK,'
            else:
                msg = 'Err,'
            print('..', msg, "SPLA ID: ", problem.SPLA_best_first_id, ", time = %10f s" % (e - s))
        except TypeError:
            print("'NoneType' object has no attribute '__getitem__'")


def excute_list(method):
    if method == 0:
        msg = 'original version:'
    else:
        msg = 'modified version:'
    print(msg)
    case_time('input0.txt', method)
    case_time('input1.txt', method)
    case_time('input2.txt', method)
    case_time('input6.txt', method)
    case_time('input7.txt', method)
    case_time('input10_1.txt', method)
    case_time('input10_2.txt', method)
    case_time('input20.txt', method)
    case_time('input21.txt', method)
    # case_time('input22.txt', method)
    # case_time('input23.txt', method)
    # case_time('input24.txt', method)
    case_time('input25.txt', method)
    print("")


if __name__ == '__main__':
    excute_list(0)
    excute_list(1)
