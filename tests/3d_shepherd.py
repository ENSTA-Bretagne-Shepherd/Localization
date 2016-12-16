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
from myinterval import distSep3D, fuse
from point import *


# --------------------------------------------------------------------------------
# Real data and positions
# --------------------------------------------------------------------------------
# sailboat are all on the water surface
sailboats = [Point(-100, 100, 50), Point(-100, -100, 50),
             Point(100, -100, 50), Point(100, 100, 50)]
# Buoy position
buoyR = Point(0, 0, 10)
# real distance to the sailboats
DR = [distance3D(buoyR, sb) for sb in sailboats]

# --------------------------------------------------------------------------------
# Received data (noised)
# --------------------------------------------------------------------------------
# noise
noise = 0.5

D = [Interval(dr - noise, dr + noise) for dr in DR]

# Separator for one information
# (Geometry tools from pyibex have been move out, how to find them ?)
# sep = Sep
# We'll use our own instead
seps = []
for m, d in zip(sailboats, D):
    sep = distSep3D(m.x, m.y, m.z, d)
    seps.append(sep)

sep = SepQInter(seps)
sep.q = 0

startI = IntervalVector(3)
startI[0] = Interval(-20, 20)
startI[1] = Interval(-20, 20)
startI[2] = Interval(-20, 20)


# --------------------------------------------------------------------------------
# Drawing section
# --------------------------------------------------------------------------------

# Creation des figures
vibes.beginDrawing()
vibes.newFigure('plan XY')
vibes.newFigure('plan YZ')
vibes.newFigure('plan XZ')
vibes.setFigureProperties({'x': 100, 'y': 100, 'width': 700, 'height': 700})

# SIVIA
res = pySIVIA(startI, sep, 0.1, draw_boxes=False)
res2 = fuse(res[0] + res[2])

# --------------------------------------------------------------------------------
# PLAN XY
# --------------------------------------------------------------------------------

vibes.selectFigure('plan XY')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.x, s.y, 5, 'magenta[red]')

vibes.drawBox(res2[0].ub(), res2[0].lb(), res2[1].ub(), res2[1].lb(), '[blue]')

# --------------------------------------------------------------------------------
# PLAN YZ
# --------------------------------------------------------------------------------

vibes.selectFigure('plan YZ')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.y, s.z, 5, 'magenta[red]')

vibes.drawBox(res2[1].ub(), res2[1].lb(), res2[2].ub(), res2[2].lb(), '[blue]')

# --------------------------------------------------------------------------------
# PLAN XZ
# --------------------------------------------------------------------------------

vibes.selectFigure('plan XZ')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.x, s.z, 5, 'magenta[red]')

vibes.drawBox(res2[0].ub(), res2[0].lb(), res2[2].ub(), res2[2].lb(), '[blue]')

vibes.axisEqual()


# print(x, y, a)
# vibes.drawBox(x[0], x[1], y[0], y[1], 'blue[cyan]')
