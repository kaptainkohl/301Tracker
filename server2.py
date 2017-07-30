import socket
import sys
from thread import *
import time

f = open('ip.txt', 'r')
HOST = f.readline()
f.close()
print(HOST)
PORT = 8888 
quit= True

#===Max of 15 people in the race===#
index=0
user_data = [[0,0,0],[0,0,0]]
user_name = ["username","kaptainkohl"]
user_pic = []
overall_totals=[]
y =0
a =0

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
s.listen(15)
print 'Socket now listening'
 
#Function for handling connections
def clientthread(conn):
	global index
	global user_data
	global quit
	conn.send('connected')
	datam=conn.recv(1024)
	print(datam)
	
	while quit:
		try:
			data=conn.recv(1024).split(',')
			print(data[0])
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
	print("writing")
	file = open('player_data.txt', 'w')
	for x in range(0,len(user_name)):
		file.write(user_name[x] +","+str(user_data[x])+"$")
	file.close()
	time.sleep( 10 )
	if quit:
		write();
	
start_new_thread(write ,())	
while quit:
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	start_new_thread(clientthread ,(conn,))

 
s.close()