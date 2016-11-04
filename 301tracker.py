from PIL import ImageGrab
import cv2
import numpy as np
import socket
from threading import Thread
import time


#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_SIMPLEX
canvas = np.zeros((100, 250, 3), np.uint8)
toggle = False

#===Game===#
current_game =0
game_list=["Banjo-Kazooie","Banjo-Tooie","Donkey Kong 64"]
collectables=['0 ','0 ','0  ']
collectable_name=["Jiggy","Jiggy","GB"]
gb_name = 'temps/gb.png'
last_jiggy=0
vc=False
vc_y=0;
if vc:
	vc_y=-5;
	gb_name = 'temps/gb2.png'
	
#===Templates for image comparison===#
gb_template = cv2.imread(gb_name,0)
w, h = gb_template.shape[::-1]
bk_template = cv2.imread('temps/jiggy.png',0)
w, h = bk_template.shape[::-1]

#===Server=====#
f = open('settings.txt', 'r')
username = f.readline()
host = f.readline()
port = 8888
update = False
quit = True
connect = False
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

	rect = (1,1,67,45)
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
				print(x)
				this_number = str(x)
				
											
	return this_number			
		

#===Display the tacker app===#				
def display_counter():
	global current_game
	global quit
	global update
	global connect
	global toggle
	while quit:
		#===Screen Capture===#
		screen = ImageGrab.grab(bbox=(200,400,500,550)) 
		box = np.array(screen) 
		img= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
		

		#===Keyboard Commands========
		ch = cv2.waitKey(1)
		if  ch == 27:
			quit= False  # esc to quit
		if ch == ord('a'): 
			cv2.imwrite('screenshot.png',img)
		if ch == ord('q'): 
			update= True
		if ch == ord('s'): 
			connect= True
		if ch == ord('1'): 
			collectables[0]='100'
		if ch == ord('2'): 
			collectables[1]='90'
		if ch == ord('3'): 
			collectables[2]='201'
		if ch == ord('w'): 
			collectables[0]= str(int(collectables[0])+1)
		if ch == ord('t'): 
			if toggle:
				toggle= False
				cv2.destroyWindow('Display Capture')
			else:
				toggle= True
		if ch == 2555904:
			current_game+=1
		if ch == 2424832:
			current_game-=1
		
		if current_game<0:
			current_game=0
		if current_game>2:
			current_game=2
		
		#===Check Game and perform action===#
		if current_game==2:
			check_golden_banana(img)
		if current_game==0:	
			check_bk_jiggies(img)
		
		#===Draw on Screen===#
		cv2.rectangle(canvas, (0,0), (300,100), (0,0,0), -1)	
		cv2.putText(canvas,collectable_name[current_game]+'= '+collectables[current_game],(10,30), font, 0.8,(255,255,255),2)	
		cv2.putText(canvas,game_list[current_game],(10,90), font, 0.6,(255,255,255),2)	
		
		#==Show Screens===#
		cv2.imshow('Counter App : '+username, canvas)
		if toggle:
			cv2.imshow('Display Capture', img)		
	cv2.destroyAllWindows()
	
def check_golden_banana(img):

	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
	res = cv2.matchTemplate(img_gray,gb_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):			
			place_hold = list(collectables[2])
			final = list(collectables[2])
			#print(pt[1])
			if pt[1] <30:
				#=====Menu====================
				roi = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+60+vc_y):(pt[0]+110)]
				roi2 = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+90+vc_y):(pt[0]+140)]
				roi3 = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+125+vc_y):(pt[0]+175)]
				place_hold[0]  =str(test_num(roi))
				place_hold[1]  =str(test_num(roi2))
				place_hold[2]  =str(test_num(roi3))
				cv2.rectangle(img, (pt[0]+60+vc_y,pt[1]+25+vc_y), (pt[0]+110,pt[1]+73), (0,0,255), 1)
				cv2.rectangle(img, (pt[0]+90+vc_y,pt[1]+25+vc_y), (pt[0]+140,pt[1]+73), (0,255,0), 1)	
				cv2.rectangle(img, (pt[0]+125+vc_y,pt[1]+25+vc_y), (pt[0]+175,pt[1]+73), (255,0,0), 1)				
			else:
				#=====Gameplay====================
				roi = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+70):(pt[0]+120)]
				roi2 = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+105):(pt[0]+153)]
				roi3 = img[pt[1]+25+vc_y:(pt[1]+73), (pt[0]+140):(pt[0]+185)]
				place_hold[0]  =str(test_num(roi))
				place_hold[1]  =str(test_num(roi2))	
				place_hold[2]  =str(test_num(roi3))	
				cv2.rectangle(img, (pt[0]+70,pt[1]+25), (pt[0]+120,pt[1]+73), (0,0,255), 1)
				cv2.rectangle(img, (pt[0]+105,pt[1]+25), (pt[0]+153,pt[1]+73), (0,255,0), 1)	
				cv2.rectangle(img, (pt[0]+140,pt[1]+25), (pt[0]+185,pt[1]+73), (255,0,0), 1)				
			
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
	global last_jiggy
	current_count = collectables[0]
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
	res = cv2.matchTemplate(img_gray,bk_template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.77
	loc = np.where( res >= threshold)		
	if zip(*loc[::-1]):
		for pt in zip(*loc[::-1]):
			if pt[0] <110:
				print("x:"+str(pt[0])+" y:"+str(pt[1]))
				roi = img[pt[1]+10:(pt[1]+65), (pt[0]+80):(pt[0]+155)]
				place_hold  =str(bk_num(roi))
				cv2.rectangle(img, (pt[0]+60,pt[1]+10), (pt[0]+110,pt[1]+65), (0,0,255), 1)
				cv2.rectangle(img, (pt[0],pt[1]), (pt[0]+67,pt[1]+72), (0,0,255), 1)
			break;
		if int(place_hold) is not last_jiggy and int(place_hold) is not 0:
			collectables[0]= str(int(current_count)+1)
			last_jiggy =int(place_hold)
		if int(place_hold) == 1 and int(collectables[0]) == 0:
			collectables[0]= str(int(current_count)+1)
			last_jiggy = 1
			time.sleep(4)
		update = True
#===Server Thread===#
def server_send():
	global update
	global connect
	s = socket.socket()
	print("Ready")
	while connect == False or quit == False:
		pass
	connect = False
	s.connect((host, port))
	print s.recv(1024)
	s.send(username)
	s.send(collectables[0]+","+collectables[1]+","+collectables[2])
	#===loop while app is active, every 5 seconds check to see if there is an update, if so send the data==#
	while quit:
		time.sleep( 5 )
		if update:	
			try:
				s.send(collectables[0]+","+collectables[1]+","+collectables[2])
			except:
				connect = True
			update = False
		if connect:
			print("ending connection")
			connect = False
			break;
	try:
		s.send("quiting")
	except:
		connect = False
	
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