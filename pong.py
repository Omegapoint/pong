from blessings import Terminal
import serial
import time


class Thing:
	x=0
	y=0
	dx=0
	dy=0
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0

class Court:
	paddle0

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

def initializePaddlesAndBall(term):


term = Terminal()
#print term.clear
#print term.move(5,10)+"Hej"+term.reverse+"Kaka"+term.normal

defineObjects(term)

ser = serial.Serial(
	port='/dev/ttyACM0',\
	baudrate=9600,\
	parity=serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
		timeout=0)

while True:
	str=readLine(ser)
	if str != "":
		print str
	time.sleep(0.01)
