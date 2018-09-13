#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/9/18 9:57 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw1cs561f2018.py
# @Software: PyCharm

import pilot_scooter as ps


def using_stupid(in_path):
    ps_problem = ps.problem_generator(in_path)
    result = ps_problem.solve_stupid()
    return result


def using_smart(in_path):
    ps_problem = ps.problem_generator(in_path)
    result = ps_problem.solve_smart()
    return result


if __name__ == '__main__':
    in_path = 'input1.txt'
    result = using_smart(in_path)
    # result = using_stupid(in_path)
