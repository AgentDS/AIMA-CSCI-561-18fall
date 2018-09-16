#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/16/18 12:23 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : xxx.py
# @Software: PyCharm

import pilot_scooter as ps
from time import time

if __name__ == '__main__':
    in_path = 'input.txt'
    out_path = 'output.txt'
    problem = ps.problem_generator(in_path)
    print("Read In End ...")
    s = time()
    problem.solve_smart()
    e = time()
    print("time: %.5s, best point = %d" % (e - s, problem.best_point))
    problem.output_result(out_path)
