import socket
import sys
from thread import *
import cv2
import numpy as np
import time

f = open('ip.txt', 'r')
HOST = f.readline()
f.close()
print(HOST)
PORT = 8888 
quit= True

#===Max of 15 people in the race===#
index=0
user_data = []
user_name = []
user_pic = []
overall_totals=[]
y =0
a =0

#===Layout===$
player_bac = cv2.imread('temps/player_bac.png')

#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_DUPLEX
canvas = np.zeros((1000, 500, 3), np.uint8)
 
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
	print(user_name[user_index][:-1])
	user_data[user_index]=conn.recv(1024).split(',')
	user_pic[user_index]= cv2.imread('serverIcons/'+user_name[user_index][:-1]+'.png')
	try:
		user_pic[user_index]= cv2.resize(user_pic[user_index], (50, 50)) 
	except:
		user_pic[user_index]=cv2.imread('serverIcons/unknown.png')
		user_pic[user_index]= cv2.resize(user_pic[user_index], (50, 50)) 
	overall_totals[user_index] = int(user_data[user_index][0])+ int(user_data[user_index][1])+int(user_data[user_index][2])
	while quit:
		try:
			data = conn.recv(1024)
		except:
			data = "quiting"
		print(data)
		if data == "quiting":
			del user_data[user_index]
			del user_name[user_index]
			del user_pic[user_index]
			del overall_totals[user_index]
			index-=1;
			break
		user_data[user_index]=data.split(',')
		overall_totals[user_index] = int(user_data[user_index][0])+ int(user_data[user_index][1])+int(user_data[user_index][2])

	conn.close()

def display_counts():
		global quit
		global y 
		global a
		while quit:
			ch = cv2.waitKey(1)
			if  ch == 27:
				quit= False
			cv2.rectangle(canvas, (0,0), (1000,500), (0,0,0), -1)
			time.sleep(2)
			place = list(overall_totals)
			place.sort(reverse=True)
			#print(place )
			#print(overall_totals)
			for x in range(0,len(user_data)):
				#===Check Place===#
				time.sleep(1)
				current_place = 0
				for y in range(0,len(place)):
					if overall_totals[x] == place[y]:
						current_place= y+1
				#===Get current Game===#
				current_game = 1;
				if int(user_data[x][1])>1:
					current_game = 2
				if int(user_data[x][2])>1:
					current_game = 3
				
				y = x
				a = 0
				if x > 5:
					a= 1
					y=x-6
					#=====Draw totals on sreeen====#
					canvas[y*125:125+y*125, 0+a*200:200+a*200] = player_bac
					canvas[3+y*125:53+y*125, 3+a*200:53+a*200] = user_pic[x]
					cv2.putText(canvas,user_name[x][:-1],(55+a*200,20+y*125), font, 0.6,(255,255,255),2)
					cv2.putText(canvas,"Game "+str(current_game)+"/3",(55+a*200,45+y*125), font, 0.4,(255,255,255),1)	
					cv2.putText(canvas,"Place: "+str(current_place),(140+a*200,45+y*125), font, 0.4,(255,255,255),1)				
					cv2.putText(canvas,"Banjo-Kazooie",(6+a*200,70+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][0]+"/100",(155+a*200,79+y*125), font, 0.3,(255,255,255),1)
					cv2.rectangle(canvas, (6+a*200,75+y*125), (int(int(user_data[x][0])*1.4)+6+a*200,79+y*125), (0,0,255), -1)
					cv2.putText(canvas,"Banjo-Tooie",(6+a*200,90+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][1]+"/90",(155+a*200,99+y*125), font, 0.3,(255,255,255),1)
					cv2.rectangle(canvas, (6+a*200,95+y*125), (int(int(user_data[x][1])*1.55)+6+a*200,99+y*125), (0,255,0), -1)
					cv2.putText(canvas,"Donkey Kong 64",(6+a*200,110+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][2]+"/201",(155+a*200,119+y*125), font, 0.3,(255,255,255),1)
				#print(a)
				else:
					#=====Draw totals on sreeen====#
					canvas[y*125:125+y*125, 0+a*200:200+a*200] = player_bac
					canvas[3+y*125:53+y*125, 3+a*200:53+a*200] = user_pic[x]
					cv2.putText(canvas,user_name[x][:-1],(55+a*200,20+y*125), font, 0.6,(255,255,255),2)
					cv2.putText(canvas,"Game "+str(current_game)+"/3",(55+a*200,45+y*125), font, 0.4,(255,255,255),1)	
					cv2.putText(canvas,"Place: "+str(current_place),(140+a*200,45+y*125), font, 0.4,(255,255,255),1)				
					cv2.putText(canvas,"Banjo-Kazooie",(6+a*200,70+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][0]+"/100",(155+a*200,79+y*125), font, 0.3,(255,255,255),1)
					cv2.rectangle(canvas, (6+a*200,75+y*125), (int(int(user_data[x][0])*1.4)+6+a*200,79+y*125), (0,0,255), -1)
					cv2.putText(canvas,"Banjo-Tooie",(6+a*200,90+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][1]+"/90",(155+a*200,99+y*125), font, 0.3,(255,255,255),1)
					cv2.rectangle(canvas, (6+a*200,95+y*125), (int(int(user_data[x][1])*1.55)+6+a*200,99+y*125), (0,255,0), -1)
					cv2.putText(canvas,"Donkey Kong 64",(6+a*200,110+y*125), font, 0.3,(255,255,255),1)
					cv2.putText(canvas,user_data[x][2]+"/201",(155+a*200,119+y*125), font, 0.3,(255,255,255),1)
				
				
				cv2.rectangle(canvas, (6+a*200,115+y*125), (int(int(user_data[x][2])*0.7)+6+a*200,118+y*125), (255,0,0), -1)
			cv2.imshow('Server App', canvas)

				
	
start_new_thread(display_counts,())
while quit:
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	user_data.append('')
	user_name.append('')
	user_pic.append('')
	overall_totals.append('')
	start_new_thread(clientthread ,(conn,index))
	index+=1
 
s.close()