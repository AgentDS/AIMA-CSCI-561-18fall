#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/18 5:54 PM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : hw2cs561f2018.py
# @Software: PyCharm

import homeless_service as hs

prob = hs.problem_generator('input2.txt')
for app in prob.app_info:
    print(app)