#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/18 10:01 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : xxx.py
# @Software: PyCharm
from __future__ import print_function
import SpeedRacer as sr
import numpy as np
from time import time
import utils

if __name__ == '__main__':
    # utils.make_output_compare()
    # in_path = './HW3_Test_Cases/input11.txt'
    in_path = './input2.txt'
    problem = sr.problem_generator(in_path)
    problem.mdp_solve()
    problem.best_policy()
    score = problem.simulation()
    print(score)
    problem.print_policy(0)

