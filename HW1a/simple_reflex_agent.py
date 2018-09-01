#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/1/18 11:40 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : simple_reflex_agent.py
# @Software: PyCharm
from __future__ import print_function


def get_percept(string_in):
    location, status = string_in.strip().split(',')
    return location, status


def get_action(location, status):
    clean, dirty = 'Clean', 'Dirty'
    right, left, suck = 'Right', 'Left', 'Suck'
    if status == dirty:
        return suck
    elif location == 'A':
        return right
    elif location == 'B':
        return left


def take_action(action, out_file, action_count):
    if action_count != 1:
        action = '\n' + action
    print(action, end='', file=out_file)


def call_agent(in_path, out_path):
    with open(out_path, 'w') as out_f:
        action_count = 0
        for line in open(in_path, 'r'):
            action_count += 1
            location, status = get_percept(line)
            action = get_action(location, status)
            take_action(action, out_f, action_count)
