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
        result = ps_problem.solve_smart()
        with open('./HW1b/solution1.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input2(self):
        """Test on case input2.txt"""
        in_path = './HW1b/input2.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_smart()
        with open('./HW1b/solution2.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input3(self):
        """Test on case input3.txt"""
        in_path = './HW1b/input3.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_smart()
        with open('./HW1b/solution3.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input4(self):
        """Test on case input4.txt"""
        in_path = './HW1b/input4.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_smart()
        with open('./HW1b/solution4.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    def test_input5(self):
        """Test on case input5.txt"""
        in_path = './HW1b/input5.txt'
        ps_problem = ps.problem_generator(in_path)
        result = ps_problem.solve_smart()
        with open('./HW1b/solution5.txt', 'r') as f:
            answer = int(f.readline().strip())
        self.assertEqual(result, answer)

    # # Taking too much time, so comment out this test case
    # def test_input6(self):
    #     """Test on case input6.txt"""
    #     in_path = './HW1b/input6.txt'
    #     ps_problem = ps.problem_generator(in_path)
    #     result = ps_problem.solve_smart()
    #     with open('./HW1b/solution6.txt', 'r') as f:
    #         answer = int(f.readline().strip())
    #     self.assertEqual(result, answer)

    # # Taking too much time, so comment out this test case
    # def test_input7(self):
    #     """Test on case input7.txt"""
    #     in_path = './HW1b/input7.txt'
    #     ps_problem = ps.problem_generator(in_path)
    #     result = ps_problem.solve_smart()
    #     with open('./HW1b/solution7.txt', 'r') as f:
    #         answer = int(f.readline().strip())
    #     self.assertEqual(result, answer)

    # # Taking too much time, so comment out this test case
    # def test_input8(self):
    #     """Test on case input8.txt"""
    #     in_path = './HW1b/input8.txt'
    #     ps_problem = ps.problem_generator(in_path)
    #     result = ps_problem.solve_smart()
    #     with open('./HW1b/solution8.txt', 'r') as f:
    #         answer = int(f.readline().strip())
    #     self.assertEqual(result, answer)

    # # Taking too much time, so comment out this test case
    # def test_input13(self):
    #     """Test on case input13.txt"""
    #     in_path = './HW1b/input13.txt'
    #     ps_problem = ps.problem_generator(in_path)
    #     result = ps_problem.solve_smart()
    #     with open('./HW1b/solution13.txt', 'r') as f:
    #         answer = int(f.readline().strip())
    #     self.assertEqual(result, answer)


if __name__ == "__main__":
    unittest.main()
