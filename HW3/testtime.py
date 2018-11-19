#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/19/18 1:55 AM
# @Author  : Siqi Liang
# @Contact : zszxlsq@gmail.com
# @File    : testtime.py
# @Software: PyCharm
from __future__ import print_function
import numpy as np
from time import time


def makeP(s):
    Ptensor = np.ones(shape=(s, s, 4, 4), dtype=float)
    Ptensor[:, :, :, 0] *= 0.7
    Ptensor[:, :, :, 1:] *= 0.1
    Ptensor[1, 1, :, :] /= np.array(
        [[0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1], [0.7, 0.1, 0.1, 0.1]])
    return Ptensor


def use_out(s, Ptensor, Rmat, max_iter):
    Utensor = np.zeros(shape=(s, s, 4, 4))
    Utmp = np.zeros(shape=(s, s, 4))
    Umat_tmp = np.zeros(shape=(s, s))
    for i in range(max_iter):
        np.sum(Utensor * Ptensor, axis=3, out=Utmp)
        np.max(Utmp, axis=2, out=Umat_tmp)
        np.add(Umat_tmp, Rmat, out=Umat_tmp)


def no_out(s, Ptensor, Rmat, max_iter):
    Utensor = np.zeros(shape=(s, s, 4, 4))
    Utmp = np.zeros(shape=(s, s, 4))
    Umat_tmp = np.zeros(shape=(s, s))
    for i in range(max_iter):
        Utmp = np.sum(Utensor * Ptensor, axis=3)
        Umat_tmp = np.max(Utmp, axis=2)
        Umat_tmp = Umat_tmp + Rmat


def cars_out(s, n, max_iter):
    Rmat = np.ones(shape=(s, s)) * (-1)
    Rmat[int(s / 2), :] *= -99
    Rmat[int(s / 3), :] *= 101
    Ptensor = makeP(s)
    for i in range(n):
        use_out(s, Ptensor, Rmat, max_iter)


def cars_no_out(s, n, max_iter):
    Rmat = np.ones(shape=(s, s)) * (-1)
    Rmat[int(s / 2), :] *= -99
    Rmat[int(s / 3), :] *= 101
    Ptensor = makeP(s)
    for i in range(n):
        no_out(s, Ptensor, Rmat, max_iter)


if __name__ =='__main__':
    s = 100
    n = 40
    max_iter = 5000

    s1 = time()
    cars_no_out(s, n, max_iter)
    e1 = time()
    print('No Out:   %.6f min' % ((e1-s1)/60))

    s2 = time()
    cars_out(s, n, max_iter)
    e2 = time()
    print('With Out: %.6f min' % ((e2 - s2) / 60))
