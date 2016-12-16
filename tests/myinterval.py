# -*- coding: utf-8 -*-
"""
    Alaa El Jawad
    ~~~~~~~~~~~~~
    Useful methods that creates an abstraction of pyibex
"""
from vibes import *
from pyibex import *


def mypolarXY(x, y, r, alpha):
    myf1 = Function("x", "y", "(x-%f)^2 + (y-%f)^2" % (x, y))
    myf2 = Function("x", "y", "atan2(%f-y,%f-x)" % (y, x))
    # myf2 = Function("x", "y", "atan2(y-%f,x-%f)" % (y, x))
    myC1 = SepFwdBwd(myf1, r**2)
    myC2 = SepFwdBwd(myf2, alpha)
    ctcs = [myC1, myC2]
    # ctc = CtcQInter(ctcs, 0)
    sep = SepQInter(ctcs)
    sep.q = 0
    return sep


def distSep(x, y, r):
    myf1 = Function("x", "y", "(x-%f)^2 + (y-%f)^2" % (x, y))
    myC1 = SepFwdBwd(myf1, r**2)
    return myC1


def distSep3D(x, y, z, r):
    myf1 = Function(
        "x", "y", "z", "(x-%f)^2 + (y-%f)^2 + (z-%f)^2" % (x, y, z))
    myC1 = SepFwdBwd(myf1, r**2)
    return myC1


def fuse(intList):
    a = intList[0]
    for i in intList:
        a = a | i
    return a
