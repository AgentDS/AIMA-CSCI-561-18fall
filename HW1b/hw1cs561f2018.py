#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/9/18 9:57 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw1cs561f2018.py
# @Software: PyCharm

import pilot_scooter as ps
from __future__ import print_function
import numpy as np
import sys

if __name__ == '__main__':
    in_path = 'input.txt'
    ps_problem = ps.problem_generator(in_path)
    print("N = %d, P = %d, S = %d:" % (ps_problem.N, ps_problem.P, ps_problem.S))
    result = ps_problem.solve_stupid()
    ps_problem.output_result('output.txt')


