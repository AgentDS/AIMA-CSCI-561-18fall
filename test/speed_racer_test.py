#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/18 6:28 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : speed_racer_test.py
# @Software: PyCharm
import unittest
import HW3.SpeedRacer as sr
import numpy as np
from numpy.testing import assert_array_equal as assert_array_equal


class SpeedRacerTestCase(unittest.TestCase):
    def _get_answer(self, answer_path):
        for line in open(answer_path, 'r'):
            num_list = line.strip()[1:-1].split(', ')
            ans = []
            for num in num_list:
                ans.append(int(num))
            return np.array(ans, dtype=int)

    def test_input0(self):
        """Test on case input0.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 0
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input1(self):
        """Test on case input1.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 1
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input2(self):
        """Test on case input2.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 2
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input3(self):
        """Test on case input3.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 3
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input4(self):
        """Test on case input4.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 4
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input6(self):
        """Test on case input6.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 6
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input7(self):
        """Test on case input7.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 7
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input8(self):
        """Test on case input8.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 8
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input9(self):
        """Test on case input9.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 9
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input10(self):
        """Test on case input10.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 10
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input13(self):
        """Test on case input13.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 13
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)

    def test_input14(self):
        """Test on case input14.txt"""
        path = './HW3/HW3_Test_Cases/'
        case_id = 14
        in_path = 'input%d.txt' % case_id
        problem = sr.problem_generator(path + in_path)
        problem.mdp_solve()
        problem.best_policy()
        result = problem.simulation()

        out_path = 'output%d.txt' % case_id
        answer = self._get_answer(path + out_path)
        assert_array_equal(result, answer)


if __name__ == "__main__":
    unittest.main()
