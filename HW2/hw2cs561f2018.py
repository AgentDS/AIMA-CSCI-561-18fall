#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 5:54 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw2cs561f2018.py
# @Software: PyCharm
from __future__ import print_function
import homeless_service as hs

if __name__ == '__main__':
    in_path = 'input.txt'
    out_path = 'output.txt'
    problem = hs.problem_generator(in_path)
    problem.solve()
    problem.output_result(out_path)
