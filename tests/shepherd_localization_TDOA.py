from pyibex import *
from vibes import *
from myinterval import distSep3Dtdoa, fuse
from point import *


# --------------------------------------------------------------------------------
# Real data and positions
# --------------------------------------------------------------------------------
# sound wave celerity into water
c = 1500

# sailboat are all on the water surface
sailboats = [Point(-100, 100, 50), Point(-100, -100, 50),
             Point(100, -100, 50), Point(100, 100, 50)]

# Time message sent
t = 10

# Buoy position
buoyR = Point(0, 0, 0)
# real distance to the sailboats
DR = [distance3D(buoyR, sb) for sb in sailboats]

# --------------------------------------------------------------------------------
# Received data (noisy) --> Interval
# --------------------------------------------------------------------------------
# noise
noise = 0.5
noiseGPS = 0.2
noiseTime = 0.5
noisePressure = 1

sailboatsI = [Point(Interval(sb.x).inflate(noiseGPS),
                    Interval(sb.y).inflate(noiseGPS),
                    Interval(sb.z).inflate(noiseGPS)) for sb in sailboats]
D = [Interval(dr).inflate(noise) for dr in DR]

t0 = 0

# information from the pressure sensor
Z = Interval(20).inflate(noisePressure)


# --------------------------------------------------------------------------------
# Separator
# --------------------------------------------------------------------------------
seps = []
for s in sailboatsI:
    sep = distSep3Dtdoa(s.x, s.y, s.z, Z, c, t0)
    seps.append(sep)

sep = SepQInter(seps)
sep.q = 0

startI = IntervalVector(3)
startI[0] = Interval(-20, 20)
startI[1] = Interval(-20, 20)
startI[2] = Interval(-20, 20)

# SIVIA
inside, outside, limit = pySIVIA(startI, sep, 1, draw_boxes=False)
box = fuse(inside + limit)
buoyX, buoyY, buoyZ = box


# --------------------------------------------------------------------------------
# Drawing section
# --------------------------------------------------------------------------------

vibes.beginDrawing()
# Creation des figures
fig_props = {'x': 100, 'y': 100, 'width': 700, 'height': 700}

vibes.newFigure('plan XY')
vibes.setFigureProperties(fig_props)

vibes.newFigure('plan YZ')
vibes.setFigureProperties(fig_props)

vibes.newFigure('plan XZ')
vibes.setFigureProperties(fig_props)

# --------------------------------------------------------------------------------
# PLAN XY
# --------------------------------------------------------------------------------

vibes.selectFigure('plan XY')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.x, s.y, 5, 'magenta[red]')

vibes.drawBox(buoyX.ub(), buoyX.lb(), buoyY.ub(), buoyY.lb(), '[blue]')

vibes.axisEqual()

# --------------------------------------------------------------------------------
# PLAN YZ
# --------------------------------------------------------------------------------

vibes.selectFigure('plan YZ')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.y, s.z, 5, 'magenta[red]')

vibes.drawBox(buoyY.ub(), buoyY.lb(), buoyZ.ub(), buoyZ.lb(), '[blue]')

vibes.axisEqual()

# --------------------------------------------------------------------------------
# PLAN XZ
# --------------------------------------------------------------------------------

vibes.selectFigure('plan XZ')
# Draw Sailboats
for s in sailboats:
    vibes.drawCircle(s.x, s.z, 5, 'magenta[red]')

vibes.drawBox(buoyX.ub(), buoyX.lb(), buoyZ.ub(), buoyZ.lb(), '[blue]')

vibes.axisEqual()
