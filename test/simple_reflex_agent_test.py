#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/1/18 11:52 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : simple_reflex_agent_test.py
# @Software: PyCharm
import unittest
import HW1a.simple_reflex_agent as sra




class MyTestCase(unittest.TestCase):
    def test_get_percept(self):
        """Test get_percept"""
        line = "A,Clean\n"
        location, status = sra.get_percept(line)
        self.assertEqual(location, "A")
        self.assertEqual(status, "Clean")

    def test_get_action(self):
        """Test get_action"""
        ac1 = sra.get_action('A', 'Clean')
        self.assertEqual(ac1, "Right")
        ac2 = sra.get_action('A', 'Dirty')
        self.assertEqual(ac2, "Suck")
        ac3 = sra.get_action('B', 'Clean')
        self.assertEqual(ac3, "Left")
        ac4 = sra.get_action('B', 'Dirty')
        self.assertEqual(ac4, "Suck")


if __name__ == "__main__":
    unittest.main()
