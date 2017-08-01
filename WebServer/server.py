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

user_data = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
user_name = ["Konditioner","connor75","Dickhiskhan","Emoarbiter","icupspeedruns_","Secrethumorman","Kiwikiller67","ElectricFortune","kaptainkohl","HolySanctum","Mittenz","PurpleRupees"]
user_pic = []
totals=''
y =0
a =0


quit= True


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	print(port)
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
	
@app.route('/tracker', methods=['GET', 'POST'])	
def startsocket():
	if request.method == 'POST':
		a = request.form['username']
		b = request.form['BK']
		c = rrequest.form['BT']
		d = request.form['DK']
		print(a+" "+str(b))
		for x in range(0,len(user_name)):
			if user_name[x]==a:
				user_data[x][0]=b
				user_data[x][1]=c
				user_data[x][2]=d
		write()
		return jsonify(result=totals)	
	

@app.route('/user/', methods=['GET', 'POST'])
@app.route('/user/<name>', methods=['GET', 'POST'])
def userpage(name=None):
	return render_template('user.html', name=name)

@app.route('/')
def homepage():
	return render_template('main.html')

@app.route('/stats', methods=['GET', 'POST'])
def statspage():
	write()
	return render_template('301Display.html')
	

	

