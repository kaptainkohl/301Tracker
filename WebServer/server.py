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

f = open('ip.txt', 'r')
HOST = f.readline()
f.close()
print(HOST)
PORT = 8888 
quit= True
	
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created")
 
#Bind socket to local host and port
try:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
except socket.error as msg:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()
	 
print ('Socket bind complete')
s.listen(15)
print ('Socket now listening')
	

def socketThread():
	print("now connect")
	while quit:
		conn, addr = s.accept()
		print ('Connected with ' + addr[0] + ':' + str(addr[1]))
		start_new_thread(clientthread ,(conn,))
	s.close()

if __name__ == '__main__':
	#start_new_thread(write ,())
	#start_new_thread(socketThread ,())
	
	app.run()
	



 
#Function for handling connections
def clientthread(conn):
	global index
	global user_data
	global quit
	conn.send('connected')
	datam=conn.recv(1024)
	#print(datam)
	
	while quit:
		try:
			data=conn.recv(1024).split(',')
			#print(data[0])
			for x in range(0,len(user_name)):
				if user_name[x] == data[0]:
					user_data[x][0]= str(data[1])
					user_data[x][1]= str(data[2])
					user_data[x][2]= str(data[3])
		except:
			print("quiting")
			quit = False
	conn.close()

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

@app.route('/_socket')	
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
	return 'success'
	
@app.route('/')
def homepage():
	return render_template('main.html')
@app.route('/stats', methods=['GET', 'POST'])
def statspage():
	return render_template('301Display.html')
	

	

