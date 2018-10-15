#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/15/18 6:11 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : homeless_service_test.py
# @Software: PyCharm
import unittest
import HW2.homeless_service as hs


class HomelessServiceTestCase(unittest.TestCase):
    def test_input0(self):
        """Test on case input0.txt"""
        in_path = './HW2/input0.txt'
        problem = hs.problem_generator(in_path)
        problem.solve()
        result = problem.SPLA_best_first_id
        with open('./HW2/output0.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input1(self):
        """Test on case input1.txt"""
        in_path = './HW2/input1.txt'
        problem = hs.problem_generator(in_path)
        problem.solve()
        result = problem.SPLA_best_first_id
        with open('./HW2/output1.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input2(self):
        """Test on case input2.txt"""
        in_path = './HW2/input2.txt'
        problem = hs.problem_generator(in_path)
        problem.solve()
        result = problem.SPLA_best_first_id
        with open('./HW2/output2.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input7(self):
        """Test on case input7.txt"""
        in_path = './HW2/input7.txt'
        problem = hs.problem_generator(in_path)
        problem.solve()
        result = problem.SPLA_best_first_id
        with open('./HW2/output7.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)


if __name__ == "__main__":
    unittest.main()
