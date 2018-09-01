#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/25/18 1:56 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : test_bench.py
# @Software: PyCharm

import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('./test/', pattern='*_test.py')
    unittest.TextTestRunner(verbosity=2).run(suite)
