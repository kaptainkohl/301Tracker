from __future__ import print_function
import os
import socket
import sys
import time
import flask
from flask import request, render_template, redirect, Flask, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(2)
#===Max of 15 people in the race===#
index=0

user_data = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
user_name = ["Connor75","Emoarbiter","Secrethumorman","ObiyoSRL","Dickhiskhan","MutantsAbyss","icupspeedruns_","Hagginater","kaptainkohl","HolySanctum","Mittenz","PurpleRupees","Hagginatersd"]
user_pic = []
totals=''
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
	global user_data
	global totals
	print("writing")
	totals=''
	for x in range(0,len(user_name)):
		totals = ''+totals + user_name[x] +","+str(user_data[x])[1:-1]+"$"
	
	
	

@app.route('/_update')
def updateStats():
	a = request.args.get('a', 0, type=int)
	
	return jsonify(result=totals)

@app.route('/_socket', methods=['GET', 'POST'])	
def startsocket():
	a = request.args.get('username', 'Konditioner')
	b = request.args.get('BK', 0, type=int)
	c = request.args.get('BT', 1,type=int)
	d = request.args.get('DK', 0,type=int)
	print(a+" "+str(b))
	for x in range(0,len(user_name)):
		if user_name[x]==a:
			user_data[x][0]=b
			user_data[x][1]=c
			user_data[x][2]=d
	write()
	return jsonify(result=totals)

@app.route('/_bingo')
def updatebingo():
	global bingoCard
	##print(bingoCard)
	return jsonify(result=bingoCard)

@app.route('/_bingoClick')
def updatebingoClicked():
	global bingoCard
	a = request.args.get('board', "goals")
	b = request.args.get('bcolors', "color")
	bingoCard = ''+a + '$' + b
	return jsonify(result=bingoCard)
	
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
	return render_template('301Display.html')

@app.route('/statsHag', methods=['GET', 'POST'])
def statspage2():
	write()
	return render_template('hag.html')	

	

