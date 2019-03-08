#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blessings import Terminal
import serial
import time

# Constants
paddleLength=5
paddlePositionsFromBorder=4
maxPaddleArgument=300

class Ball:
	x=0
	y=0
	dx=0
	dy=0
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0

class Paddle:
	x=0
	y=0
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Court:
	isPlaying=False
	ball=None
	paddle=[]
	serve=-1

	def __init__(self,ball,paddle0,paddle1,serve):
		self.ball=ball
		self.paddle=[paddle0,paddle1]
		self.isPlaying=False
		self.serve=serve

	def updatePaddle(self,player,yposition):
		self.paddle[player].y=yposition
		if not self.isPlaying and self.serve==player:
			self.ball.y=self.paddle[player].y+paddleLength/2

	def serve(self,player):
		self.isPlaying=True
		self.ball.dx=1
		self.ball.dy=1

def readLine(ser):
	res=""
	crFound=False
	bytesToRead=ser.inWaiting()
	if bytesToRead > 0:
		while not crFound:
			resPart=ser.read(1)
			if resPart == "\n":
				crFound=True
			else:
				res=res+resPart
	return res

def initializeBallAndPaddles(term):
	ball=Ball(paddlePositionsFromBorder+1,term.height/2)
	paddle0=Paddle(paddlePositionsFromBorder, term.height/2-paddleLength/2)
	paddle1=Paddle(term.width-paddlePositionsFromBorder, term.height/2-paddleLength/2)
	court = Court(ball,paddle0,paddle1,0)
	return court

def drawBall(term,ball):
	print term.move(ball.y,ball.x)+"*"

def clearBall(term,ball):
	print term.move(ball.y,ball.x)+" "

def drawPaddle(term,paddle):
	#print "paddle.y={}".format(paddle.y)
	for i in range(0,paddleLength):
		print term.move(paddle.y+i,paddle.x)+term.reverse+" "+term.normal

def draw(term, court):
	print term.clear
	drawBall(term,court.ball)
	drawPaddle(term,court.paddle[0])
	drawPaddle(term,court.paddle[1])
	print term.move(term.height-2,0)

term = Terminal()

court=initializeBallAndPaddles(term)

ser = serial.Serial(
	port='/dev/ttyACM0',\
	baudrate=9600,\
	parity=serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
		timeout=0)

str=readLine(ser)
with term.fullscreen():
	while True:
		str=readLine(ser)
		if str != "":
			(player,action,argument)=str.split("¤")
			n=int(player)
			if action=="PADL":
				yposition=int((term.height-paddleLength-1)*min(int(argument), maxPaddleArgument)/(maxPaddleArgument*1.0))
				court.updatePaddle(n,yposition)
			#if action=="FIRE" and argument=="DN":
			#	court.serve(n)
		#court.updateBall()
			draw(term,court)




		time.sleep(0.01)
