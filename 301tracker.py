from PIL import ImageGrab
import cv2
import numpy as np



#===Templates for image comparison===#
gb_template = cv2.imread('temps/gb.png',0)
w, h = gb_template.shape[::-1]

#===Set up Vars for Screen===#
font = cv2.FONT_HERSHEY_SIMPLEX
canvas = np.zeros((100, 250, 3), np.uint8)

#===Game===#
current_game =0
game_list=["Banjo-Kazooie","Banjo-Tooie","Donkey Kong 64"]
collectables=['0  ','0  ','0  ']
collectable_name=["Jiggy","Jiggy","GB"]



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
		

				
def display_game():
	global current_game
	while True:
		screen = ImageGrab.grab(bbox=(200,400,500,550)) 
		box = np.array(screen) 
		img= cv2.cvtColor(box, cv2.COLOR_RGB2BGR)
		

		#===Keyboard Commands========
		ch = cv2.waitKey(1)
		if  ch == 27:
			break  # esc to quit
		if ch == ord('a'): 
			cv2.imwrite('screenshot.png',img)
		if ch == 2555904:
			current_game+=1
		if ch == 2424832:
			current_game-=1
		
		if current_game<0:
			current_game=0
		if current_game>2:
			current_game=2
		
		check_golden_banana(img)
		
		cv2.rectangle(canvas, (0,0), (300,100), (0,0,0), -1)	
		cv2.putText(canvas,collectable_name[current_game]+'= '+collectables[current_game],(10,30), font, 0.8,(255,255,255),2)	
		cv2.putText(canvas,game_list[current_game],(10,90), font, 0.6,(255,255,255),2)	
		
		cv2.imshow('Counter App', canvas)
		#cv2.imshow('301 App', img)			
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
			if pt[1] <20:
				#=====Menu====================
				roi = img[pt[1]+25:(pt[1]+73), (pt[0]+60):(pt[0]+110)]
				roi2 = img[pt[1]+25:(pt[1]+73), (pt[0]+70):(pt[0]+123)]
				roi3 = img[pt[1]+25:(pt[1]+73), (pt[0]+117):(pt[0]+155)]
				place_hold[0]  =str(test_num(roi))
				place_hold[1]  =str(test_num(roi2))
				place_hold[2]  =str(test_num(roi3))
				#cv2.rectangle(img, (pt[0]+95,pt[1]+25), (pt[0]+143,pt[1]+73), (0,255,0), 1)	
				#cv2.rectangle(img, (pt[0]+117,pt[1]+25), (pt[0]+175,pt[1]+73), (255,0,0), 1)			
							
			else:
				#=====Gameplay====================
				roi = img[pt[1]+25:(pt[1]+73), (pt[0]+70):(pt[0]+120)]
				roi2 = img[pt[1]+25:(pt[1]+73), (pt[0]+105):(pt[0]+153)]
				roi3 = img[pt[1]+25:(pt[1]+73), (pt[0]+147):(pt[0]+185)]
				place_hold[0]  =str(test_num(roi))
				place_hold[1]  =str(test_num(roi2))	
				place_hold[2]  =str(test_num(roi3))				
			
			#print(str(place_hold[0])+str(place_hold[1])+str(place_hold[2]))
			if place_hold[0] is not '':
				final[0] = place_hold[0]				
			if place_hold[1] is not '':
				final[1] = place_hold[1]
			if place_hold[2] is not '':
				final[2] = place_hold[2]
			collectables[2] = "".join(final)
			break;

	
	
	
def main():
	display_game()

if __name__ == '__main__':
	main()