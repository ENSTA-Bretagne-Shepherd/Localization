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


class Sailboat(object):
    """Sailboat pose Container"""

    def __init__(self, x, y, z):
        super(Sailboat, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def setXYZ(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class BuoyLocator(object):
    """docstring for BuoyLocator"""

    def __init__(self):
        super(BuoyLocator, self).__init__()
        self.x = 0
        self.y = 0
        self.z = -10
        # Sailboat list
        self.sb1 = Sailboat(-10, 10, 0)
        self.sb2 = Sailboat(10, 10, 0)
        self.sb3 = Sailboat(10, -10, 0)
        self.sb4 = Sailboat(-10, -10, 0)
        self.sailboats = [self.sb1, self.sb2, self.sb3, self.sb4]

    def onPingReceived(self, sailboatNumber, sbX, sbY, sbZ):
        self.sailboats[sailboatNumber].setXYZ(sbX, sbY, sbZ)

        # because sailboat ping in loop: 4 means we have the 3 others info
        if sailboatNumber == 4:
            self.updatePose()

    def updatePose(self):
        pass


if __name__ == '__main__':
    pass
