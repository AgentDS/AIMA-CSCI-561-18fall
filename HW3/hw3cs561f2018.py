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
    p0 = sr.problem_generator('input1.txt')
    s = time()
    p0.mdp_solve()
    e = time()
    print("Time: %.10s s" % (e - s))
    p0.best_policy()
    p0.print_policy(0)
    # p0.print_policy(1)
    # p0.print_policy(2)
    # p0.print_policy(3)
    # p0.print_policy(4)
    # prob1 = sr.problem_generator('input1.txt')
    # prob2 = sr.problem_generator('input2.txt')

