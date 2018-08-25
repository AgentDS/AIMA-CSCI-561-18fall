#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/25/18 2:07 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : first_test.py
# @Software: PyCharm

import unittest
import first


class MyTestCase(unittest.TestCase):
    def test_first(self):
        """Test the unittest framework"""
        self.assertEqual(first.func(), "This can be printed.")


if __name__ == "__main__":
    unittest.main()
