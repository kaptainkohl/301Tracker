# 301 Tracker
This is an application made solely for the Rareware 301 Collectathon Race http://bombch.us/Bj_W

This program uses opencv to look at an image of gameplay and search for objects, in this case Jiggies and Golden Bananas.
It finds them on the screen then looks at the numbers to the right of them. It then image reconizes the numbers to figure out the totals of that collectable.
The collectables data is now displayed in a small box on the screen which a user can place on their own stream so everyone can see their total count.
The data will also be sent to a server. The server reads everyones incomeing data and displays it on the screen.
This data then can be streamed to the stats tracking stream showing who is in the lead with how many totals.
This automates the process of finding out who is in the lead making it so the helpers do not need to struggle to keep up with the counts.

Important Notes

	Your Gamplay needs to be around 660x505 pixels to work perfectly and dk is slightly wider by 20 pixels than bk bt when cropped.
	You need to crop 10 extra pixels from both side then your gamplay will fit nicely and work well with the others
	Your layout is good if your splits are the same size for all 3 games, and your gamefeed fits inside the space left.
	I good measuement i used is croped BK so there was no black space then used that as the box size since BK is the finicy tracker.
	Then Tooie was about the same size as bk when cropped, but then dk was to wide so i cropped edges out of its gameplay.
	The size if the gameplay is more able getting the numbers to be the right size and not the entire gamefeed box so croping it out works.
	
	I recomend turning the tracking off for BK if you have never tried it and tick each jiggy manually. 
	BK is very dumb with how they manage their jiggy count and display it on screen and you need a perfect size screen to read the numbers comapred to the other games.
	You can start off the 301 thinking it might work then if you realize it doesnt you can start ticking it up with Enter anyways.
	
	Both BT and DK work very well with tracking and you should be able to get it to work if its with in the set range values. 
	
	* If you Press the T key when in a gamemode you will see the exact tracking. You can put anything on your screen as long as it does not cover that area that box shows.
	
	
	Hopefully you set this all up and try it before the 301 so there are no problems when starting.

# How To Use


Settings File

	Do not mess with Enter, there needs to be only 2 lines in the file
	Line 1: Put your username here
	Line 2: Put the ip of the server you want to connect to. 
	
Setup gameplay reading	

	https://gyazo.com/76e9b675dbb508b24bb227931531505f
	Open the Application (exe file)
	once the App is Open use the left arrow to go to the 301 page. This will open a new pop up saying 'Dong'.
	You are now goint to use the red arrows drawn on the pictures of the two boxes and line them up with corners of the gameplay.
	the 301 goes to the Top Left corner, and the dong goes to the bottom right.
	once you have them Lined up press the C key and it will try to locate them. In the terminal that opened it will give you information.
	It will say if its wide or tall and tell you its current size and the aim size. Resize your game feed and move the boxes to the corners again and press C.
	Do this untill it says your gameplay is optimal size.
	Now you can start to use the Application
	
Setup Not using image tracking

	You can use this application as a counter without having to go through the set up of image tracking.
	However, you will have to manually tick the counter every collectable you get in the games.
	This is for people who dont want to deal with having to set up and having tracking running as they play.
	To do this all you need to do is press ] and tracking is turned off.
	Now ever collectable you get you will press Enter and it will add 1.
	
Gameplay

	Use the Arrow keys on your key board to scroll through the games to select the current game you are on.
	If you are on a game and you collect somthing for that game it will automatically update. Its that easy.
	
Online Feature

	This Application has the ablity to connect to a server to send its data.
	To turn on online mode all you need to do is press S. 
	If you have the proper IP adress typed into the settings.txt it will try to connect. 
	If the connection accepts, it will say Online on the main screen.
	You will now be sending your data to the server everytime you collect a collectable.
	To exit online mode just press S again.
	
KeyBoard Controls

	Escape: Close the Program
	Arrow Keys: Scroll through games	
	C: Center your screen capture using the image boxes
	S: Start your connection to the server
	T: Toggle current screen tracking.
	Enter: Add a collectable
	\: Subtract a collectable
	
	p: clear collectable for current game
	]: Toggle Image Tracking
	q: Toggle 100 Jiggies (incase app/computer crashes you have a way to get the totals back)
	w: Toggle 90 Jiggies
	e: Toggle 201 Banana
	z: Give yourself a Jiggy (Bk only)

	

# Dev Install (Windows)

Install Anaconda 2.7(A python install that gives easy ways to install modules) https://www.continuum.io/downloads

Once python is installed use the commands in a command prompt: conda install -c https://conda.binstar.org/menpo opencv

There you go everything needed is installed. Now you can go to your folder where the program is and click on it to run.
You may have to open it as a python file by open with; then set the application to c:\where ever your anaconda install is\anaconda2\python
