#!/usr/bin/env python
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
    in_path = 'input.txt'
    out_path = 'output.txt'
    problem = sr.problem_generator(in_path)
    problem.mdp_solve()
    problem.best_policy()
    score = problem.simulation()
    with open(out_path, 'w') as out:
        for i in range(problem.n):
            print('%d' % score[i], file=out)
