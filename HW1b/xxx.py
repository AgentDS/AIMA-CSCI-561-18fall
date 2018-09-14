#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/9/18 9:57 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw1cs561f2018.py
# @Software: PyCharm

import pilot_scooter as ps
import time


# def using_stupid(in_path):
#     ps_problem = ps.problem_generator(in_path)
#     result = ps_problem.solve_stupid()
#     print "best: " + str(result['point'])
#
#
# def using_smart(in_path):
#     ps_problem = ps.problem_generator(in_path)
#     result = ps_problem.solve_smart()
#     print "best: " + str(result['point'])


if __name__ == '__main__':
    in_path = 'input1.txt'
    out_path = 'output.txt'
    problem = ps.problem_generator(in_path)
    problem.solve_smart()
    problem.output_result(out_path)
    # using_smart('input3.txt')
    # for i in range(5):
    #     in_path = 'input' + str(i + 1) + ".txt"
    #     print '\n' * 2 + "=" * 8 + in_path + "=" * 8
    #     print "==>Using smart:"
    #     s1 = time.time()
    #     using_smart(in_path)
    #     e1 = time.time()
    #     print "Time: %.6f s" % (e1 - s1)
    #
    #     if i != 3:
    #         print "==>Using stupid:"
    #         s2 = time.time()
    #         using_stupid(in_path)
    #         e2 = time.time()
    #         print "Time: %.6f s" % (e2 - s2)
    #     else:
    #         print "==>Using stupid:"
    #         print "best: " + str(16)
    #         print "Time: 680 s"
    #
    #

    # in_path = 'input1.txt'
    # result = using_smart(in_path)
    # result = using_stupid(in_path)

    # psp1 = ps.problem_generator('input1.txt')
    # res1 = psp1.solve_smart()
    #
    # psp2 = ps.problem_generator('input2.txt')
    # res2 = psp2.solve_smart()

    # psp3 = ps.problem_generator('input3.txt')
    # res3 = psp3.solve_smart()
    # # #
    # ps_stupid = ps.problem_generator('input3.txt')
    # res3_stupid = ps_stupid.solve_stupid()
