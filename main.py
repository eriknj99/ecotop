import gpustat
import json
import io 
import os
import math
from termcolor import colored
from time import sleep
import sys
import signal

def drawGraph(lable, unit, val, max, color):
	
	numTicks = 10 
	
	tick = '┼'
	hLine = '─'	
	vLine = '│'
	c0 = '├'
	c1 = '┤'
	c2 = '└'
	c3 = '┘'
	bar = '█'
	halfBar = '▌'
	space = ' '
	
	rows, columns = os.popen('stty size', 'r').read().split()
	columns = int(columns) - (len(str(max) + '          ' + unit))

	#Draw Lable
	out = (lable + " | " + colored(str(val) + unit, color) + "\n")
	
	#Label ticks
	for i in range(0,numTicks):
		tmp = str(int(i*(max/numTicks))) + unit	
		out += tmp
		for j in range(0,int((int(columns)/numTicks) - ((len(tmp) - 1)))):
			out += ' ' 
	out += str(max) + unit + "\n"
	
	#Draw top ticks
	ticks = ''
	for i in range(0,numTicks+1):
		if(i == 0):
			ticks+=c0
		elif(i == numTicks):
			ticks+=c1
		else:
			ticks += tick
		if(i != numTicks):
			for j in range(0,int((int(columns)/numTicks))):
				ticks += hLine			
	out += ticks + "\n"


	
	#Fill in bar
	barLine = ""
	barSize = round((len(ticks) - 1) * float(val/max))
	for i in range(0, barSize - 1):
		barLine += bar	
		#out += "[" + barLine + " : " + str(len(barLine)) + "]\n"
	if(val != 0 and val != max):
		barLine += halfBar
	
	while(val != max and len(barLine) < len(ticks) - 2):
		barLine += space 
		
	out += vLine + colored(barLine,color) + vLine + "\n"
	
	#Draw bottom ticks
	ticks = ''
	for i in range(0,numTicks+1):
		if(i == 0):
			ticks+=c2
		elif(i == numTicks):
			ticks+=c3
		else:
			ticks += hLine
		if(i != numTicks):
			for j in range(0,int((int(columns)/numTicks))):
				ticks += hLine	

	out += ticks + "\n"

	return out



def temp(json, i, color1, color2, color3):
	tmp = float(j['gpus'][i]['temperature.gpu'])
	color = color1
	if(tmp > 70):
		color = color2
	if(tmp > 80):
		color = color3
	return drawGraph("Temperature (°C)", "°", tmp,100, color)	

def util(json,i,color):
	return drawGraph("Utilization", "%", json['gpus'][i]['utilization.gpu'],100, color)

def fan(json,i,color):
	return drawGraph("Fan", "%", json['gpus'][i]['fan.speed'],100, color)

def power(json, i, color):
	return drawGraph("Power", "W", json['gpus'][i]['power.draw'],json['gpus'][i]['enforced.power.limit'], color)

def memoryPercent(json, i, color):
	return drawGraph("Memory", "%", round(100*(json['gpus'][i]['memory.used']/json['gpus'][i]['memory.total'])), 100, color)

def memoryVal(json, i, color):	
	return drawGraph("Memory", "Mb", json['gpus'][i]['memory.used'],json['gpus'][i]['memory.total'], color)

def memory(json, i, color):
	percent = colored(str(round(100*(json['gpus'][i]['memory.used']/json['gpus'][i]['memory.total']))) + '%', color)
	return drawGraph('Memory | ' + percent, 'Mb', json['gpus'][i]['memory.used'],json['gpus'][i]['memory.total'], color)

def help():
	print(""+
	"   _____________  __             \n"
	"  / __/ ___/ __ \/ /____  ___    \n"
	" / _// /__/ /_/ / __/ _ \/ _ \   \n"
	"/___/\___/\____/\__/\___/ .__/   \n"
	"                       /_/       \n")

	print("---HELP---\n"
	"Usage: ecotop <Gauge1> [Color(s)] ... <GaugeN> [Color(s)] \n"
	"╔════════════╦════╦═════════════╗  \n"
	"║Gauge       ║Arg ║Color(s)     ║  \n"
	"╠════════════╬════╬═════════════╣  \n"
	"┃Utilization ┃-u  ┃<color1>     ┃  \n"
	"┃Temperature ┃-t  ┃<color1,2,3> ┃  \n"
	"┃Fan Speed   ┃-f  ┃<color1>     ┃  \n"
	"┃Power Usage ┃-p  ┃<color1>     ┃  \n"
	"┃Memory      ┃-m  ┃<color1>     ┃  \n"
	"┃Memory (%)  ┃-mp ┃<color1>     ┃  \n"
	"┃Memory (Mb) ┃-mv ┃<color1>     ┃  \n"
	"┗━━━━━━━━━━━━┻━━━━┻━━━━━━━━━━━━━┛  \n\n"

	"-All Color Arguments are optional.\n"
	"-Gauges will be desplayed in the order they are entered.\n"
	"\n Colors\n"
	"┏━━━━━━━━┓\n"
	"┃"+colored('grey','grey')+"    ┃\n"
	"┃"+colored('red','red')+"     ┃\n"
	"┃"+colored('green','green')+"   ┃\n"
	"┃"+colored('yellow','yellow')+"  ┃\n"
	"┃"+colored('blue','blue')+"    ┃\n"
	"┃"+colored('magenta','magenta')+" ┃\n"
	"┃"+colored('cyan','cyan')+"    ┃\n"
	"┃"+colored('white','white')+"   ┃\n"
	"┗━━━━━━━━┛\n")
#This function with the line below it will clear the screen and exit when ctrl+c is pressed
def clear_on_exit(sig, frame):
	os.system('clear')
	sys.exit(0)

signal.signal(signal.SIGINT, clear_on_exit)




orderedArgs = []

#Default colors
cu = 'red'
ct1 = 'blue'
ct2 = 'yellow'
ct3 = 'red'
cf = 'cyan' 
cp = 'yellow'
cm = 'green'
cmp = 'green'
cmv = 'green'


#Parse input args
for i in range(1,len(sys.argv)):
	if(sys.argv[i] == 'help' or sys.argv[i] == '--help' or sys.argv[i] == '-h'):
		help()
		exit(0)		

	if(sys.argv[i] == '-u'):
		orderedArgs.append("u")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cu = sys.argv[i+1]
	if(sys.argv[i] == '-t'):
		orderedArgs.append("t")	
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			ct1 = sys.argv[i+1]
		if(i < len(sys.argv)-2 and "-" not in sys.argv[i+2]):
			ct2 = sys.argv[i+2]	
		if(i < len(sys.argv)-3 and "-" not in sys.argv[i+3]):
			ct3 = sys.argv[i+3]	
	if(sys.argv[i] == '-f'):
		orderedArgs.append("f")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cf = sys.argv[i+1]
	if(sys.argv[i] == '-p'):
		orderedArgs.append("p")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cp = sys.argv[i+1]
	if(sys.argv[i] == '-m'):
		orderedArgs.append("m")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cm = sys.argv[i+1]
	if(sys.argv[i] == '-mp'):
		orderedArgs.append("mp")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cmp = sys.argv[i+1]	
	if(sys.argv[i] == '-mv'):
		orderedArgs.append("mv")
		if(i < len(sys.argv)-1 and "-" not in sys.argv[i+1]):
			cmv = sys.argv[i+1]	

output = ''

if(len(orderedArgs) == 0):
	output = ("No arguments given, using default config.\nType 'ecotop help' for more options.\n\n\n")
	orderedArgs.append("u")
	orderedArgs.append("t")
	orderedArgs.append("p")
	orderedArgs.append("mp")
	

while(True):
	#Use GPUStat to retrieve GPU data as JSON
	g = gpustat.GPUStatCollection.new_query() 
	sio= io.StringIO()
	g.print_json(sio)
	j=json.loads(sio.getvalue())
	
	#Execute functions for each gpu in the argument specified order. 
	for i in range(0, len(j["gpus"])):
		output += ("["+str(i)+"] " + str(j["gpus"][i]["name"]) + "\n")
		for arg in orderedArgs:
			if(arg == 'u'):
				output += util(j,i,cu)
			if(arg == 't'):	
				output += temp(j,i,ct1,ct2,ct3)
			if(arg == 'f'):
				output += fan(j, i, cf)
			if(arg == 'p'):
				output += power(j, i, cp)
			if(arg == 'm'):
				output += memory(j, i, cm)
			if(arg == 'mp'):
				output += memoryPercent(j, i, cmp)
			if(arg == 'mv'):
				output += memoryVal(j, i, cmv)	

	#Clear screen and print output 	
	os.system('clear')
	print(output)
	output = ''
	
	#Sleep 1 sec before repeating
	sleep(1)


