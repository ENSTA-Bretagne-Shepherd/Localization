# -*- coding: utf-8 -*-
"""
    Alaa El Jawad
    ~~~~~~~~~~~~~
    A Buoy Locator is a class that takes as input the information received
    from the outside world and outputs an estimation of the position of the
    Buoy
"""

from vibes import *
from pyibex import *
from myinterval import distSep3D, fuse


class Sailboat(object):
    """Sailboat pose Container"""

    def __init__(self, x, y, z, d):
        super(Sailboat, self).__init__()
        self.x = x
        self.y = y
        self.z = z
        self.d = d
        self.updateSeparator()

    def setXYZ(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def setDistance(self, d):
        self.d = d

    def updateSeparator(self):
        self.sep = distSep3D(self.x, self.y, self.z, self.d)

    def getSep(self):
        self.updateSeparator()
        return self.sep


class BuoyLocator(object):
    """docstring for BuoyLocator"""

    def __init__(self, x, y, z):
        super(BuoyLocator, self).__init__()
        self.x = x
        self.y = y
        self.z = z
        # Sailboat list
        self.sb1 = Sailboat(Interval(1), Interval(2), Interval(3), Interval(4))
        self.sb2 = Sailboat(Interval(1), Interval(2), Interval(3), Interval(4))
        self.sb3 = Sailboat(Interval(1), Interval(2), Interval(3), Interval(4))
        self.sb4 = Sailboat(Interval(1), Interval(2), Interval(3), Interval(4))
        self.sailboats = [self.sb1, self.sb2, self.sb3, self.sb4]

    def onPingReceived(self, sailboatNumber, sbX, sbY, sbZ, D):
        self.sailboats[sailboatNumber].setXYZ(sbX, sbY, sbZ)
        self.sailboats[sailboatNumber].setDistance(D)

        # because sailboat ping in loop: 4 means we have the 3 others info
        if sailboatNumber == 4:
            self.updatePose()

    def updatePose(self):
        seps = [sb.getSep() for sb in self.sailboats]
        sep = SepQInter(seps)
        sep.q = 0   # relaxation

        # Start interval
        startI = IntervalVector(3)
        startI[0] = self.x.inflate(3)
        startI[1] = self.y.inflate(3)
        startI[2] = self.z.inflate(3)
        # SIVIA
        res = pySIVIA(startI, sep, 1, draw_boxes=False)
        res2 = fuse(res[0] + res[2])
        # Update Pose
        self.x, self.y, self.z = res2


if __name__ == '__main__':
    # noise
    n = 0.2
    b = BuoyLocator(Interval(0), Interval(0), Interval(0))
    b.onPingReceived(0, Interval(100).inflate(n), Interval(100).inflate(
        n), Interval(50).inflate(n), Interval(150).inflate(n))
    b.onPingReceived(1, Interval(-100).inflate(n), Interval(-100).inflate(
        n), Interval(50).inflate(n), Interval(150).inflate(n))
    b.onPingReceived(2, Interval(-100).inflate(n), Interval(100).inflate(
        n), Interval(50).inflate(n), Interval(150).inflate(n))
    b.onPingReceived(3, Interval(100).inflate(n), Interval(-100).inflate(
        n), Interval(50).inflate(n), Interval(150).inflate(n))
    b.updatePose()
    print(b.x, b.y, b.z)
