# -*- coding: utf-8 -*-
"""
    Alaa El Jawad
    ~~~~~~~~~~~~~
    We consider a vertical cut of the problem.
    - 4 sailboat are on the water surface
    - 1 buoy is somwhere in the water
"""
from pyibex import *
from vibes import *
from myinterval import mypolarXY, distSep
import numpy as np


# useful functions

def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


def angle(a, b):
    x = np.array(b) - np.array(a)
    return np.arctan2(x[1], x[0])


# --------------------------------------------------------------------------------
# Real data and positions
# --------------------------------------------------------------------------------
# sailboat are all on the water surface
sailboats = [[-10, 50], [-5, 50], [0, 50], [5, 50]]
# Buoy position
buoyR = [0, 0]
# real distance to the sailboats
DR = [dist(buoyR, sb) for sb in sailboats]
# real angle of the sailboats
AR = [angle(buoyR, sb) for sb in sailboats]

# --------------------------------------------------------------------------------
# Received data (noised)
# --------------------------------------------------------------------------------
# noise
nd = 0.1
na = 0.01

D = [Interval(dr - nd, dr + nd) for dr in DR]
Alpha = [Interval(ar - na, ar + na) for ar in AR]

# Separator for one information
# (Geometry tools from pyibex have been move out, how to find them ?)
# sep = Sep
# We'll use our own instead
seps = []
for m, d, alpha in zip(sailboats, D, Alpha):
    # sep = mypolarXY(m[0], m[1], d, alpha)
    sep = distSep(m[0], m[1], d)
    seps.append(sep)

sep = SepQInter(seps)
sep.q = 0

startI = IntervalVector(2)
startI[0] = Interval(-20, 20)
startI[1] = Interval(-20, 20)


# Drawing section
vibes.beginDrawing()
vibes.newFigure('locpie')
vibes.setFigureProperties({'x': 100, 'y': 100, 'width': 700, 'height': 700})
# Draw water
vibes.drawBox(-30, 30, -100, 50, 'blue[cyan]')
res = pySIVIA(startI, sep, 0.1, draw_boxes=False)
for s in sailboats:
    vibes.drawCircle(s[0], s[1], 0.5, 'magenta[red]')
for x in res[0]:
    vibes.drawBox(x[0].lb(), x[0].ub(), x[1].lb(), x[1].ub(), 'yellow[yellow]')
vibes.axisEqual()
# print(x, y, a)
# vibes.drawBox(x[0], x[1], y[0], y[1], 'blue[cyan]')
