#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/18 5:39 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : xxxx.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/13/18 10:42 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw3cs561f2018.py
# @Software: PyCharm
from __future__ import print_function
import SpeedRacer as sr
import numpy as np
from time import time

if __name__ == '__main__':
    case_id = 0
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
                print(ans, file=out_f)
                print('Use Time: %.10f  s' % (e - s), file=out_f)

                print('======================================================')
                print('Test File: ', end='')
                print('./input%d.txt' % case_id)
                print(ans)
                print('Use Time: %.10f  s' % (e - s))
