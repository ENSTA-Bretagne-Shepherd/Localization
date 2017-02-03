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
import json
from pprint import pprint
import socket


def localisation(messagePosBateau, messageCaptBouee):
	# --------------------------------------------------------------------------------
	# Socket creation (client)
	# --------------------------------------------------------------------------------
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("127.0.0.1", 13000))

	# --------------------------------------------------------------------------------
	# Message received from the simulator
	# --------------------------------------------------------------------------------
	with open('pingPositionBateau.json') as data_file_voilier:    
		pingPositionBateau = json.load(data_file_voilier)
	with open('capteurPositionBouee.json') as data_file_bouee:    
		capteurPositionBouee = json.load(data_file_bouee)
	#pingPositionBateau = json.load(messagePosBateau)
	xVoilier = Interval(pingPositionBateau["xmin"], pingPositionBateau["xmin"])
	yVoilier = Interval(pingPositionBateau["ymin"], pingPositionBateau["ymax"])
	zVoilier = Interval(pingPositionBateau["zmin"], pingPositionBateau["zmax"])
	idVoilier = pingPositionBateau["id"]
	distanceEmission = Interval(pingPositionBateau["distanceEmissionmin"], pingPositionBateau["distanceEmissionmax"])

	#capteurPositionBouee = json.load(messageCaptBouee)
	idBouee = capteurPositionBouee["id"]
	zBouee = Interval(capteurPositionBouee["zmin"], capteurPositionBouee["zmax"])

	sailboatsI = [Interval(0), Interval(0), Interval(0), Interval(0)]
	sailboatsI[idVoilier] = Point(xVoilier, yVoilier, zVoilier)
	D = [Interval(0), Interval(0), Interval(0), Interval(0)]
	D[idVoilier] = distanceEmission

	# --------------------------------------------------------------------------------
	# Real data and positions
	# --------------------------------------------------------------------------------
	# sailboat are all on the water surface
	sailboats = [Point(-100, 100, 50), Point(-100, -100, 50),
		         Point(100, -100, 50), Point(100, 100, 50)]

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

	sailboatsI = [Point(Interval(sb.x).inflate(noiseGPS),
		                Interval(sb.y).inflate(noiseGPS),
		                Interval(sb.z).inflate(noiseGPS)) for sb in sailboats]
	D = [Interval(dr).inflate(noise) for dr in DR]


	# --------------------------------------------------------------------------------
	# Separator
	# --------------------------------------------------------------------------------
	seps = []
	for s, d in zip(sailboatsI, D):
		sep = distSep3D(s.x, s.y, s.z, d)
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
	# Message sent
	# --------------------------------------------------------------------------------
	messageSent = json.dumps({"id":idBouee,"xmin":buoyX.lb(),"xmax":buoyX.ub(),"ymin":buoyY.lb(),"ymax":buoyY.ub()})
	pprint(messageSent)
	client.sendall(messageSent)

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
