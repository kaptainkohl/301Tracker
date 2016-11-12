from PIL import ImageGrab
import cv2
import numpy as np
import socket
from threading import Thread
import time


#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_TRIPLEX
canvas = np.zeros((100, 250, 3), np.uint8)
current_bac = [cv2.imread('temps/bac/bk.png'),cv2.imread('temps/bac/tooie.png'),cv2.imread('temps/bac/dk.png'),cv2.imread('temps/bac/promo.png')]
toggle = False

#===Game===#
current_game =3
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

	rect = (1,1,100,45)
	cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	img = img*mask2[:,:,np.newaxis]
	for x in range(1, 11):	
		num = cv2.imread('temps/bk_numbers/'+str(x)+'.png',0)
		w, h = num.shape[::-1]
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray,num,cv2.TM_CCOEFF_NORMED)
		threshold = 0.85		
		loc = np.where( res >= threshold)
		if zip(*loc[::-1]):
			for pt in zip(*loc[::-1]):
				#print(x)
				this_number = str(x)
				
											
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
	global quit
	global update
	global connect
	global toggle
	global online
	global center
	global bk_jiggy
	global lvl_index
	while quit:
		#===Screen Capture===#
		if center:
			screen = ImageGrab.grab(bbox=(600,500,900,650))
		else:
			screen = ImageGrab.grab(bbox=(200,400,500,550))
		box = np.array(screen) 
		img= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
		

		#===Keyboard Commands========
		ch = cv2.waitKey(1)
		if  ch == 27:
			quit= False  # esc to quit
		if ch == ord('a'): 
			cv2.imwrite('screenshot.png',img)
		if ch == ord('d'): 
			update= True
		if ch == ord('s'): 
			connect= True
		if ch == ord('c'): 
			if center:
				center= False
			else:
				center=True				
		if ch == ord('1'): 
			collectables[0]='100'
			update= True
		if ch == ord('2'): 
			collectables[1]='90'
			update= True
		if ch == ord('3'): 
			collectables[2]='201'
			update= True
		if ch == ord('q'): 
			if bk_jiggy[lvl_index] <10:
				bk_jiggy[lvl_index]+=1
				if bk_jiggy[lvl_index]==10:
					lvl_index = 0
					update = True


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
			current_game=3
		if current_game>3:
			current_game=0
		
		#===Check Game and perform action===#
		if current_game==2:
			check_golden_banana(img)
		if current_game==0:	
			check_bk_jiggies(img)
		if current_game==1:	
			check_tooie_jiggies(img)
		
		#===Draw on Screen===#
		if current_game<3:	
			cv2.destroyWindow('Place Game Feed on the desktop so that it fits exactly in this box. Press C to move the box to the center of the screen')
			canvas[0:100,0:250]=current_bac[current_game]
			cv2.putText(canvas,'= '+collectables[current_game],(65,35), font, 1,(255,255,255),2)	
			cv2.putText(canvas,game_list[current_game],(10,90), font, 0.6,(255,255,255),2)	
			if toggle:
				cv2.imshow('Display Capture', img)	
		else:
			if toggle:
				cv2.destroyWindow('Display Capture')
				if center:
					screen = ImageGrab.grab(bbox=(400,100,1200,800))
					box = np.array(screen) 
					feed= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
					cv2.rectangle(feed, (0,60), (680,570), (0,0,255), 3)				
				else:	
					screen = ImageGrab.grab(bbox=(0,0,800,700))
					box = np.array(screen) 
					feed= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
					cv2.rectangle(feed, (0,60), (680,570), (0,0,255), 3)		
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
			place_hold = list(collectables[2])
			final = list(collectables[2])
			#print(pt[1])
			if pt[0]+175 < 301:
				if pt[1] <30:
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
					roi3 = img[pt[1]+20:(pt[1]+73), (pt[0]+140):(pt[0]+185)]
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
	roi = img[50:110, (140):240]
	place_hold  = str(bk_num(roi))
	cv2.rectangle(img, (140,50), (240,110), (0,0,255), 1)
	
	if int(place_hold) == 1 and int(collectables[0]) is not 11:
		lair_index+=1
		lvl_index = lair_index
		bk_jiggy[lvl_index]+=1
		update = True
		time.sleep(4)
		
	elif int(place_hold) == 10:
		bk_jiggy[lvl_index]+=1	
		lvl_index = 0
		time.sleep(6)
		update = True
	elif int(place_hold) == 9 and lvl_index == 2:
		bk_jiggy[lvl_index]+=2	
		lvl_index = 0
		time.sleep(4)
		update = True
		
	elif int(place_hold) is not bk_jiggy[lvl_index] and int(place_hold) is not 0 and int(place_hold):
		bk_jiggy[lvl_index]+=1
		update = True
	total = 0
	for x in range(0, 10):		
		total += bk_jiggy[x]
	collectables[0] = str(total)
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
			if pt[1] < 103:
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

#===Server Thread===#
def server_send():
	global update
	global connect
	s = socket.socket()
	while connect == False or quit == False:
		pass
	connect = False
	try:
		s.connect((host, port))
		print s.recv(1024)
		s.send(username)
		s.send(collectables[0]+","+collectables[1]+","+collectables[2])
	except:
		update = False 
		connect = True
	#===loop while app is active, every 5 seconds check to see if there is an update, if so send the data==#
	while quit:
		online = True 
		time.sleep( 5 )
		if update:	
			try:
				s.send(collectables[0]+","+collectables[1]+","+collectables[2])
			except:
				connect = True
			update = False
		if connect:
			
			connect = False
			break;
	try:
		s.send("quiting")
	except:
		connect = False
	online = False
	s.close()	
	if quit:
		server_send()
	
	
def main():
	t = Thread(target=display_counter, args=())
	t2 = Thread(target=server_send, args=())
	t.start()
	t2.start()

if __name__ == '__main__':
	main()