from __future__ import print_function
import os
import socket
import sys
import time
import flask
import pickle
from flask import request, render_template, redirect, Flask, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(2)
#===Max of 15 people in the race===#
index=0

f = open('userdata.txt', 'wb')
pickle.dump([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],f)
f.close()
f = open('timestamp.txt', 'w')
f.write("0.0")
f.close()

user_name = ["Hagginater","FalconxFalcon1","Secrethumorman","ElectricFortune","Icupspeedruns_","MutantsAbyss","Xafication"]
user_pic = []
y =0
a =0
bingoCard = ''
quit= True

if __name__ == '__main__':
	#start_new_thread(write ,())
	#start_new_thread(socketThread ,())
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

	

def write():
	global totals
	print("writing")

	

	
def start_timer():
	f = open('timestamp.txt', 'w')
	f.write(str(time.time()))
	print(str(time.time()))
	f.close()
def read_timer():
	f = open('timestamp.txt', 'r')
	stamp = f.readline()
	f.close()
	if stamp=='0.0':
		return 0.0
	
	return int(time.time() - float(stamp))
	

@app.route('/_update')
def updateStats():
	a = request.args.get('a', 0, type=int)
	f = open('userdata.txt', 'rb')
	user_data = pickle.load(f)
	f.close()			
	totals=''
	for x in range(0,len(user_name)):
		totals = ''+totals + user_name[x] +","+str(user_data[x])[1:-1]+"$"
	return jsonify(result=totals)
	
@app.route('/_time')
def updateTime():
	a = request.args.get('username', 'Konditioner')
	
	return jsonify(result=read_timer())

@app.route('/_socket', methods=['GET', 'POST'])	
def startsocket():
	a = request.args.get('username', 'Konditioner')
	b = request.args.get('BK', 0, type=int)
	c = request.args.get('BT', 1,type=int)
	d = request.args.get('DK', 0,type=int)
	
	f = open('userdata.txt', 'rb')
	user_data = pickle.load(f)
	f.close()

	
	for x in range(0,len(user_name)):
		if user_name[x]==a:
			user_data[x][0]=b
			user_data[x][1]=c
			user_data[x][2]=d
	
	totals=''
	for x in range(0,len(user_name)):
		totals = ''+totals + user_name[x] +","+str(user_data[x])[1:-1]+"$"
	
	f = open('userdata.txt', 'wb')
	pickle.dump(user_data,f)
	f.close()
	
	
	return jsonify(result=totals)

@app.route('/_bingo', methods=['GET', 'POST'])
def updatebingo():
	global bingoCard
	#print(bingoCard)
	f = open('card.txt', 'r')
	bingoCard = f.readlines()
	f.close()
	return jsonify(result=bingoCard)

@app.route('/_bingoClick', methods=['GET', 'POST'])
def updatebingoClicked():
	global bingoCard
	a = request.args.get('board', "goals")
	b = request.args.get('bcolors', "color")
	f = open('card.txt', 'w')
	f.write(""+a + "$" + b)
	f.close()
	return jsonify(result='sent')
	
@app.route('/bingo')
def lockout():
	return render_template('TL.html')

@app.route('/user/', methods=['GET', 'POST'])
@app.route('/user/<name>', methods=['GET', 'POST'])
def userpage(name=None):
	return render_template('user.html', name=name)

@app.route('/')
def homepage():
	return render_template('main.html')

@app.route('/races')
def racepage():
	return render_template('races.html')

@app.route('/stats', methods=['GET', 'POST'])
def statspage():
	write()
	return render_template('viewer.html')

@app.route('/statStream', methods=['GET', 'POST'])
def statStream():
	write()
	start_timer()
	return render_template('301Display.html')

@app.route('/statsHag', methods=['GET', 'POST'])
def statspage2():
	write()
	return render_template('hag.html')	

	

