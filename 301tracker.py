#Blake Kohl 2017
from PIL import ImageGrab
import cv2
import numpy as np
import socket
from threading import Thread
import time
from matplotlib import pyplot as plt
import urlparse
import re
import os
import requests

#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_TRIPLEX
canvas = np.zeros((100, 250, 3), np.uint8)
level_bac =  [cv2.imread('temps/bac/bk.png'),cv2.imread('temps/bac/tooie.png'),cv2.imread('temps/bac/dk.png'),cv2.imread('temps/bac/refcheck.png'),cv2.imread('temps/bac/promo.png')]
current_bac = level_bac
blackbac = cv2.imread('temps/bac/blackbac.png')
black_bac = [blackbac,blackbac,cv2.imread('temps/bac/blackbac2.png'),cv2.imread('temps/bac/refcheck.png'),cv2.imread('temps/bac/promo.png')]
ref_bac = current_bac[3]
topleft2 = cv2.imread('temps/topleft.png')
bottomright2 = cv2.imread('temps/bottomright.png')
toggle = False
screenx =0
screeny =0
blackactive=False
toggleCapture=True
directCapture=False

#===Your Capture Card======#
#0 is your default webcam, so if your cam is the feed, change to 1 for the secondary camera#
camera_port = 2
cam = cv2.VideoCapture(camera_port)

#===Game===#
current_game =4
game_list=["Banjo-Kazooie","Banjo-Tooie","Donkey Kong 64","Menu"]
collectables=['0 ','0 ','0  ']
collectable_name=["Jiggy","Jiggy","GB","None"]
bk_jiggy=[0,0,0,0,0,0,0,0,0,0]
gb_name = 'temps/gb.png'
lvl_index =-1
lair_index =-1
center= False

	
#===Templates for image comparison===#
gb_template = cv2.imread(gb_name,0)
w, h = gb_template.shape[::-1]
bk_template = cv2.imread('temps/jiggy.png',0)
w, h = bk_template.shape[::-1]
tooie_template = cv2.imread('temps/tooie.png',0)
w, h = tooie_template.shape[::-1]
ref_template = cv2.imread('temps/bac/refcheck.png',0)
w, h = ref_template.shape[::-1]

topleft = cv2.imread('temps/topleft.png',0)
bottomright = cv2.imread('temps/bottomright.png',0)

#===Server=====#
f = open('settings.txt', 'r')
username = f.readline()
host = f.readline()
f.close()
port = 8888
update = False
quit = True
connect = False
online = False
profile_pic = cv2.imread('temps/jiggy.png',0)


#===Read DK64 Numbers===#
def test_num(img):
	this_number =''
	
	mask = np.zeros(img.shape[:2],np.uint8)
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)
	
	rect = (1,1,50,64)
	cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	img = img*mask2[:,:,np.newaxis]
	for x in range(0, 10):		
		num = cv2.imread('temps/numbers/'+str(x)+'.png',0)
		w, h = num.shape[::-1]
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray,num,cv2.TM_CCOEFF_NORMED)
		threshold = 0.85		
		loc = np.where( res >= threshold)
		if zip(*loc[::-1]):
			for pt in zip(*loc[::-1]):
				this_number = str(x)
											
	return this_number			

#===Read BK Numbers===#
def bk_num(img):
	this_number ='0'
	
	mask = np.zeros(img.shape[:2],np.uint8)
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)

	rect = (1,1,100,60)
	cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	img = img*mask2[:,:,np.newaxis]
	#cv2.imwrite('test.png',img)
	for x in range(0, 11):	
		num = cv2.imread('temps/bk_numbers/'+str(x)+'.png',0)
		w, h = num.shape[::-1]
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray,num,cv2.TM_CCOEFF_NORMED)
		threshold = 0.85	
		loc = np.where( res >= threshold)
		if zip(*loc[::-1]):
			for pt in zip(*loc[::-1]):
				print(x)
				this_number = str(x)
				
				if x==0:
					this_number = 10
					return this_number
				
											
	return this_number			

#===Read Tooie Numbers===#
def tooie_num(img):
	this_number =''
	for x in range(0, 10):	
		num = cv2.imread('temps/tooie_numbers/'+str(x)+'.png',0)
		w, h = num.shape[::-1]
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray,num,cv2.TM_CCOEFF_NORMED)
		threshold = 0.9	
		loc = np.where( res >= threshold)
		if zip(*loc[::-1]):
			for pt in zip(*loc[::-1]):
				#print(x)
				this_number = str(x)
				break;
				
											
	return this_number	

#===Display the tacker app===#				
def display_counter():
	global current_game
	global current_bac
	global collectables
	global quit
	global update
	global connect
	global toggle
	global online
	global center
	global bk_jiggy
	global lvl_index
	global blackactive 
	global toggleCapture
	global directCapture
	while quit: 
		#===Screen Capture===#
		if directCapture:
			ret_val, cap = cam.read()
			img = cap[325: 525, 180: 500]
			cv2.imshow('Place ', cap)
		else:
			screen = ImageGrab.grab(bbox=(screenx+180,screeny+325,screenx+500,screeny+525))
			box = np.array(screen) 
			img= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
			time.sleep(0.1)
		time.sleep(0.01)
		#===Keyboard Commands========
		ch = cv2.waitKey(1)
		if  ch == 27:
			quit= False  # esc to quit
		if  ch == 13:
			if current_game >= 1 and current_game<=2:
				collectables[current_game]= str(int(collectables[current_game])+1)
			if current_game ==0:
				bk_jiggy[0]+=1
			update= True
		if  ch == ord('\\'):
			if current_game >= 0 and current_game<=2:
				collectables[current_game]= str(int(collectables[current_game])-1)
		if ch == ord('a'): 
			cv2.imwrite('screenshot.png',img)
		if ch == ord('d'): 
			update= True
		if ch == ord('u'): 
			if directCapture:
				directCapture= False
			else:
				directCapture =True
		if ch == ord('b'):
			if blackactive:
				current_bac = level_bac
				blackactive =False
			else:
				current_bac = black_bac
				blackactive =True
		if ch == ord(']'):
			if toggleCapture:
				toggleCapture =False
			else:
				toggleCapture =True
		if ch == ord('s'): 
			online=True
			connect= True
		if ch == ord('v'): 
			#cv2.imshow('Top left', topleft2)
			cv2.imshow('Bottom right', bottomright2)	
		if ch == ord('c'): 
			full = ImageGrab.grab(bbox=(0,0,1900,1080))
			set_ref_point(full)
		if ch == ord('p'): 
			collectables[current_game]='0  '
			update= True
		if ch == ord('q'): 
			bk_jiggy=[10,10,10,10,10,10,10,10,10,10]
			collectables[0]='100'
			update= True
		if ch == ord('w'): 
			collectables[1]='90'
			update= True
		if ch == ord('e'): 
			collectables[2]='201'
			update= True
		if ch == ord('z'): 
			if bk_jiggy[lvl_index] <9:
				bk_jiggy[lvl_index]+=1
				if bk_jiggy[lvl_index]==9:
					bk_jiggy[lvl_index]+=1
					lvl_index = 0
				update = True
		if ch == ord('x'): 
			print(bk_jiggy)

			update= True
		if ch == ord('t'): 
			if toggle:
				toggle= False
				cv2.destroyWindow('Display Capture')
				cv2.destroyWindow('Place Game Feed on the desktop so that it fits exactly in this box. Press C to move the box to the center of the screen')
			else:
				toggle= True
		if ch == 2555904:
			current_game+=1
		if ch == 2424832:
			current_game-=1
		
		if current_game<0:
			current_game=4
		if current_game>4:
			current_game=0
		
		if toggleCapture:
			#===Check Game and perform action===#
			if current_game==2:
				check_golden_banana(img)
			if current_game==0:	
				check_bk_jiggies(img)
			if current_game==1:	
				check_tooie_jiggies(img)
		
		#===Draw on Screen===#
		if current_game<3:	
			cv2.destroyWindow('Bottom right')
			cv2.destroyWindow('Place Game Feed on the desktop so that it fits exactly in this box. Press C to move the box to the center of the screen')
			canvas[0:100,0:250]=current_bac[current_game]
			cv2.putText(canvas,'= '+collectables[current_game],(65,35), font, 1,(255,255,255),2)	
			cv2.putText(canvas,game_list[current_game],(10,90), font, 0.6,(255,255,255),2)	
			#if current_game == 0:
				#cv2.putText(canvas, "lvl: "+str(lvl_index)+" J: "+str(bk_jiggy[lvl_index]),(10,65), font, 0.6,(255,255,255),2)	
			
			if toggle:
				cv2.imshow('Display Capture', img)	
		elif current_game == 3:
			canvas[0:100,0:250]=current_bac[current_game]
			cv2.imshow('Bottom right', bottomright2)
			if toggle:
				cv2.imshow('Display Capture', img)	
		else:
			cv2.destroyWindow('Bottom right')
			if toggle:
				cv2.destroyWindow('Display Capture')	
				screen = ImageGrab.grab(bbox=(screenx,screeny,screenx+680,screeny+510))
				box = np.array(screen) 
				feed= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
				#cv2.rectangle(feed, (0,60), (680,570), (0,0,255), 3)		
				cv2.imshow('Place Game Feed on the desktop so that it fits exactly in this box. Press C to move the box to the center of the screen', feed)	
		
			canvas[0:100,0:250]=current_bac[current_game]
			cv2.putText(canvas,username[:-1],(0,95), font, 0.5,(255,255,255),2)
			if online:
				cv2.putText(canvas,'Online',(175,95), font, 0.5,(255,255,255),2)
			else:
				cv2.putText(canvas,'Offline',(175,95), font, 0.5,(255,255,255),2)
			
		
		#==Show Screens===#
		cv2.imshow('Counter App : '+username, canvas)	
	cv2.destroyAllWindows()


#==Functions for checking for objects on screen===#	
def check_golden_banana(img):
	global update
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
	res = cv2.matchTemplate(img_gray,gb_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):			
			#print("found")
			place_hold = list(collectables[2])
			final = list(collectables[2])
			#print(pt[1])
			if pt[0]+175 < 321:
				if pt[1] <90:
					#=====Menu====================
					roi = img[pt[1]+20:(pt[1]+73), (pt[0]+60):(pt[0]+110)]
					roi2 = img[pt[1]+20:(pt[1]+73), (pt[0]+95):(pt[0]+145)]
					roi3 = img[pt[1]+20:(pt[1]+73), (pt[0]+125):(pt[0]+175)]
					place_hold[0]  =str(test_num(roi))
					place_hold[1]  =str(test_num(roi2))
					place_hold[2]  =str(test_num(roi3))
					cv2.rectangle(img, (pt[0]+60,pt[1]+20), (pt[0]+110,pt[1]+73), (0,0,255), 1)
					cv2.rectangle(img, (pt[0]+90,pt[1]+20), (pt[0]+140,pt[1]+73), (0,255,0), 1)	
					cv2.rectangle(img, (pt[0]+125,pt[1]+20), (pt[0]+175,pt[1]+73), (255,0,0), 1)				
				else:
					#=====Gameplay====================
					roi = img[pt[1]+20:(pt[1]+73), (pt[0]+70):(pt[0]+120)]
					roi2 = img[pt[1]+20:(pt[1]+73), (pt[0]+110):(pt[0]+160)]
					roi3 = img[pt[1]+20:(pt[1]+73), (pt[0]+140):(pt[0]+205)]
					place_hold[0]  =str(test_num(roi))
					place_hold[1]  =str(test_num(roi2))	
					place_hold[2]  =str(test_num(roi3))	
					cv2.rectangle(img, (pt[0]+70,pt[1]+20), (pt[0]+120,pt[1]+73), (0,0,255), 1)
					cv2.rectangle(img, (pt[0]+105,pt[1]+20), (pt[0]+153,pt[1]+73), (0,255,0), 1)	
					cv2.rectangle(img, (pt[0]+140,pt[1]+20), (pt[0]+185,pt[1]+73), (255,0,0), 1)				
			
			#print(str(place_hold[0])+str(place_hold[1])+str(place_hold[2]))
			if place_hold[0] is not '':
				final[0] = place_hold[0]				
			if place_hold[1] is not '':
				final[1] = place_hold[1]
			if place_hold[2] is not '':
				final[2] = place_hold[2]
			collectables[2] = "".join(final)
			update = True
			break;

	
def check_bk_jiggies(img):
	place_hold =0
	global bk_jiggy
	global lvl_index
	global lair_index
	global update
	current_count = collectables[0]
	
	#print("x:"+str(pt[0])+" y:"+str(pt[1]))
	roi = img[85:145, (140):240]
	place_hold  = str(bk_num(roi))
	cv2.rectangle(img, (140,85), (240,145), (0,0,255), 1)
	
	if int(place_hold) == 1 and bk_jiggy[lvl_index]==9 and lvl_index is not 0:
		bk_jiggy[lvl_index]=10	
		lvl_index = 0
		time.sleep(6)
		update = True
		
	elif int(place_hold) == 1 and (bk_jiggy[lvl_index] is not 1 or int(collectables[0]) == 1):
		lair_index+=1
		lvl_index = lair_index
		bk_jiggy[lvl_index]+=1
		update = True
		time.sleep(4)
	elif int(place_hold) == 9 and lvl_index == 2:
		bk_jiggy[lvl_index]=10	
		lvl_index = 0
		time.sleep(4)
		update = True
		
	elif int(place_hold) is not bk_jiggy[lvl_index] and int(place_hold) is not 0 and int(place_hold) > bk_jiggy[lvl_index]:
		bk_jiggy[lvl_index]+=1
		update = True
	total = 0
	if update:
		for x in range(0, 10):		
			total += bk_jiggy[x]
		collectables[0] = str(total)
		#print(bk_jiggy)
	#print(bk_jiggy)

		
		
def check_tooie_jiggies(img):
	global update
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
	res = cv2.matchTemplate(img_gray,tooie_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):			
			place_hold = list(collectables[1])
			final = list(collectables[1])
			
			roi = img[pt[1]+5:(pt[1]+45), (pt[0]+47):(pt[0]+80)]
			place_hold[0]  =str(tooie_num(roi))
			roi2 = img[pt[1]+5:(pt[1]+45), (pt[0]+65):(pt[0]+105)]
			place_hold[1]  =str(tooie_num(roi2))
			cv2.rectangle(img, (pt[0]+50,pt[1]+5), (pt[0]+75,pt[1]+45), (0,0,255), 1)
			cv2.rectangle(img, (pt[0]+68,pt[1]+5), (pt[0]+105,pt[1]+45), (0,0,255), 1)
			if place_hold[0] is not '':
				final[0] = place_hold[0]				
			if place_hold[1] is not '':
				final[1] = place_hold[1]
			collectables[1] = "".join(final)
			update = True
			break;
			
def set_ref_point(screen):
	global screenx
	global screeny
	point1x = 0
	point1y = 0
	point2x = 0
	point2y = 0
	print("searching for screen")
	box = np.array(screen) 
	img_gray = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)		
	res = cv2.matchTemplate(img_gray,ref_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.7
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):
			point1x = pt[0]
			point1y = pt[1]
			print("found301")
			screenx = point1x
			screeny = point1y
			break;
	
	res = cv2.matchTemplate(img_gray,bottomright,cv2.TM_CCOEFF_NORMED)
	threshold = 0.7
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):
			point2x = pt[0]
			point2y = pt[1]
			print("foundDong")
			break;

	xdis = ((point2x)-point1x)	
	ydis = ((point2y)-point1y)	
	if 	xdis >= 655 and xdis <= 665 and ydis >= 500 and ydis <= 510:
		print("size is good! ("+str(xdis) + ","+str(ydis)+")")
	if xdis > 665:
		print("Screen Size is to0 wide! Current Size: ("+ str(xdis)+","+ str(ydis)+") | Aim (660,505)")
	if xdis < 655:
		print("Screen Size is not wide enough! Current Size: ("+ str(xdis)+","+ str(ydis)+") | Aim (660,505)")
	if ydis > 510:
		print("Screen Size is to0 Tall! Current Size: ("+ str(xdis)+","+ str(ydis)+") | Aim (660,505)")
	if ydis < 500:
		print("Screen Size is not Tall enough! Current Size: ("+ str(xdis)+","+ str(ydis)+") | Aim (660,505)")

#===Server Thread===#
def server_send():
	global update
	global connect
	global quit
	print("connecting...")
	while quit:
		time.sleep( 1 )
		if update:
			print("sending")
			#GET("username="+username[:-1] +"&BK="+collectables[0]+"&BT="+collectables[1]+"&DK="+collectables[2])
			sendRequest()
			update = False
		
	
	s.close()	

socket.setdefaulttimeout = 0.50
os.environ['no_proxy'] = '127.0.0.1,localhost'
linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
CRLF = "\r\n\r\n"

def GET(player_data):
	player_data = player_data.replace(" ","")
	print player_data
	url = urlparse.urlparse('https://rareware-collectathon-race.herokuapp.com')
	path = url.path
	if path == "":
		path = "/"
	HOST = url.netloc
	print(HOST)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#s.setblocking(0)
	s.connect((HOST, 33507))
	s.send("GET /_socket?"+player_data+" HTTP/1.1%s" % (CRLF))
	data = (s.recv(1000000))
	print data
	# https://docs.python.org/2/howto/sockets.html#disconnecting
	s.shutdown(1)
	s.close()
	print 'Received', repr(data)

def sendRequest():
	r = requests.post('https://rareware-collectathon-race.herokuapp.com/_socket', data={'username': username[:-1],'BK':collectables[0],'BT':collectables[1],'DK':collectables[2]})
	if r.ok:
		print("polling response OK")
		print(r.text);
	else:
		print(r.text);
	
def main():
	t = Thread(target=display_counter, args=())
	t2 = Thread(target=server_send, args=())
	t.start()
	t2.start()
if __name__ == '__main__':
	main()