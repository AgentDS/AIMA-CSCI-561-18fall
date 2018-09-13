#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/13/18 1:00 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : pilot_scooter_test.py
# @Software: PyCharm
import unittest
import HW1b.pilot_scooter as ps



class PilotScooterTestCase(unittest.TestCase):
    def test_input1(self):
        """Test on case input1.txt"""
        in_path = './HW1b/input1.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_stupid()
        with open('./HW1b/solution1.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result['point'], answer)

    def test_input2(self):
        """Test on case input2.txt"""
        in_path = './HW1b/input2.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_stupid()
        with open('./HW1b/solution2.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result['point'], answer)

    def test_input3(self):
        """Test on case input3.txt"""
        in_path = './HW1b/input3.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_stupid()
        with open('./HW1b/solution3.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result['point'], answer)


if __name__ == "__main__":
    unittest.main()
