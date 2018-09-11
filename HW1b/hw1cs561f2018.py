#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/9/18 9:57 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw1cs561f2018.py
# @Software: PyCharm

import pilot_scooter as ps
import numpy as np

if __name__ == '__main__':
    in_path = 'input1.txt'
    problem = ps.problem_generator(in_path)
    office_map = ps.OLocationMap(problem.N, np.array([[0, 0], [2, 3], [1, 4]], dtype=np.int))
