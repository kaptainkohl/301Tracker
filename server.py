import socket
import sys
from thread import *
import cv2
import numpy as np
import time

HOST = 'localhost'  
PORT = 8888 
quit= True

#===Max of 15 people in the race===#
index=0
user_data = []
user_name = []

#===Layout===$
player_bac = cv2.imread('temps/player_bac.png')

#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_DUPLEX
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
	global index
	conn.send('connected')
	user_name[user_index]=conn.recv(1024)
	user_data[user_index]=conn.recv(1024).split(',')
	while quit:
		try:
			data = conn.recv(1024)
		except:
			data = "quiting"
		print(data)
		if data == "quiting":
			del user_data[user_index]
			del user_name[user_index]
			index-=1;
			break
		user_data[user_index]=data.split(',')

	conn.close()

def display_counts():
		global quit
		while quit:
			ch = cv2.waitKey(1)
			if  ch == 27:
				quit= False
			cv2.rectangle(canvas, (0,0), (720,480), (0,0,0), -1)	
			for x in range(0,len(user_data)):
				canvas[x*125:125+x*125, 0:200] = player_bac
				cv2.putText(canvas,user_name[x][:-1],(55,20+x*125), font, 0.6,(255,255,255),2)
				cv2.putText(canvas,"Game 0/3",(55,45+x*125), font, 0.4,(255,255,255),1)	
				cv2.putText(canvas,"Place: 1",(140,45+x*125), font, 0.4,(255,255,255),1)				
				#cv2.putText(canvas,user_data[x],(80,35*x+35), font, 0.8,(255,255,255),2)	
				cv2.putText(canvas,"Banjo-Kazooie",(6,70+x*125), font, 0.3,(255,255,255),1)
				cv2.putText(canvas,user_data[x][0]+"/100",(155,79+x*125), font, 0.3,(255,255,255),1)
				cv2.rectangle(canvas, (6,75+x*125), (int(int(user_data[x][0])*1.4)+6,79+x*125), (0,0,255), -1)
				cv2.putText(canvas,"Banjo-Tooie",(6,90+x*125), font, 0.3,(255,255,255),1)
				cv2.putText(canvas,user_data[x][1]+"/90",(155,99+x*125), font, 0.3,(255,255,255),1)
				cv2.rectangle(canvas, (6,95+x*125), (int(int(user_data[x][1])*1.55)+6,99+x*125), (0,255,0), -1)
				cv2.putText(canvas,"Donkey Kong 64",(6,110+x*125), font, 0.3,(255,255,255),1)
				cv2.putText(canvas,user_data[x][2]+"/201",(155,119+x*125), font, 0.3,(255,255,255),1)
				cv2.rectangle(canvas, (6,115+x*125), (int(int(user_data[x][2])*0.7)+6,118+x*125), (255,0,0), -1)
				time.sleep(1)
			cv2.imshow('Server App', canvas)

				
	
start_new_thread(display_counts,())
while quit:
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	user_data.append('')
	user_name.append('')
	start_new_thread(clientthread ,(conn,index))
	index+=1
 
s.close()