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

	def doServe(self):
		self.isPlaying=True
		self.ball.dx=1.0
		self.ball.dy=1.0

	def playerLoosing(self,term,i):
		self.isPlaying=False
		self.looser=i
		self.serve=1-i
		self.ball.dx=0.0
		self.ball.dy=0.0
		if i==0:
			self.ball.x=term.width-paddlePositionsFromBorder-1.0
		else:
			self.ball.x=paddlePositionsFromBorder+1.0

		self.ball.y=self.paddle[1-i].y+paddleLength/2

	def updateBall(self,term):
		b=self.ball
		b.x=b.x+b.dx
		b.y=b.y+b.dy
		if b.x > term.width:
			self.playerLoosing(term,1)
		if b.y >= term.height - 2.0:
			b.dy=-b.dy
			b.y=b.y+2.0*b.dy
		if b.x < 0:
			self.playerLoosing(term,0)
		if b.y < -1.0:
			b.dy=-b.dy
			b.y=b.y+2.0*b.dy

		if b.x <= self.paddle[0].x+1.0 and b.x >= self.paddle[0].x and b.y >= self.paddle[0].y and b.y <= self.paddle[0].y+paddleLength:
			b.dx=-b.dx
			b.x=b.x+2.0*b.dx
		if b.x >= self.paddle[1].x-1.0 and b.x <= self.paddle[1].x and b.y >= self.paddle[1].y and b.y <= self.paddle[1].y+paddleLength:
			b.dx=-b.dx
			b.x=b.x+2.0*b.dx


def readLine(ser):
	res=""
	crFound=False
	bytesToRead=ser.inWaiting()
	if bytesToRead > 0:
		while not crFound:
			resPart=ser.read(1)
			if resPart == "\n":
				crFound=True
			elif resPart != "\r":  # Ignore \r
				res=res+resPart
	return res

def initializeBallAndPaddles(term):
	ball=Ball(paddlePositionsFromBorder+1.0,term.height/2.0)
	paddle0=Paddle(paddlePositionsFromBorder*1.0, term.height/2.0-paddleLength/2.0)
	paddle1=Paddle(term.width-paddlePositionsFromBorder*1.0, term.height/2.0-paddleLength/2.0)
	court = Court(ball,paddle0,paddle1,0)
	return court

def drawBall(term,ball):
	print term.move(int(round(ball.y)),int(round(ball.x)))+"*"

def clearBall(term,ball):
	print term.move(int(round(ball.y)),int(round(ball.x)))+" "

def drawPaddle(term,paddle):
	#print "paddle.y={}".format(paddle.y)
	for i in range(0,paddleLength):
		print term.move(int(round(paddle.y))+i,int(round(paddle.x)))+term.reverse+" "+term.normal

def draw(term, court):
	print term.clear
	drawBall(term,court.ball)
	drawPaddle(term,court.paddle[0])
	drawPaddle(term,court.paddle[1])
	print term.move(term.height-2,0)

term = Terminal()

court=initializeBallAndPaddles(term)

ser = serial.Serial(
	port='/dev/ttyACM1',\
	baudrate=9600,\
	parity=serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
		timeout=0)

print "Reading junk"
str=readLine(ser)
print "Done"
ballCount=0
ballInterval=8
with term.fullscreen():
	while True:
		str=readLine(ser)
		if str != "":
			(player,action,argument)=str.split("¤")
			n=int(player)
			#print "player="+player+" action="+action+" argument="+argument+"size={}".format(len(argument))
			if action=="PADL":
				yposition=(term.height-paddleLength-1)*min(int(argument), maxPaddleArgument)/(maxPaddleArgument*1.0)
				court.updatePaddle(n,yposition)
			if action=="FIRE" and argument=="DN":
				court.doServe()
			draw(term,court)
		if ballCount > ballInterval:
			court.updateBall(term)
			draw(term,court)
			ballCount=0
		ballCount+=1




		time.sleep(0.01)
