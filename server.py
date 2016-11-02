import socket
import sys
from thread import *
import cv2
import numpy as np
 
HOST = 'localhost'  
PORT = 8888 
quit= True

#===Max of 15 people in the race===#
index=0
user_data = ['','','','','','','','','','','','','','','']

#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_SIMPLEX
canvas = np.zeros((720, 480, 3), np.uint8)
 
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
def clientthread(conn,user_index):
    conn.send('connected') 
     
    while quit:     
		data = conn.recv(1024)
		print(data)
		user_data[user_index]=data
		if not data: 
			break

    conn.close()

def display_counts():
		global quit
		while quit:
			ch = cv2.waitKey(1)
			if  ch == 27:
				quit= False
			cv2.rectangle(canvas, (0,0), (720,480), (0,0,0), -1)	
			for x in range(0,15):
				cv2.putText(canvas,user_data[x],(10,30*x), font, 0.8,(255,255,255),2)	
			
			cv2.imshow('Server App', canvas)
	
	
start_new_thread(display_counts,())
while quit:
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	start_new_thread(clientthread ,(conn,index))
	index+=1
 
s.close()