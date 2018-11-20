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
    case_id = 0
    p0 = sr.problem_generator('input%d.txt' % case_id)
    s = time()
    p0.mdp_solve()
    e = time()
    print("Time: %.10s s" % (e - s))
    p0.best_policy()
    print("Mean Score:")
    print(p0.simulation())
    print("Answer:")
    sr.answer_read('output%d.txt' % case_id)
