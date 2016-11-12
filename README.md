# 301 Tracker
This is an application made solely for the Rareware 301 Collectathon Race http://bombch.us/Bj_W

This program uses opencv to look at an image of gameplay and search for objects, in this case Jiggies and Golden Bananas.
It finds them on the screen then looks at the numbers to the right of them. It then image reconizes the numbers to figure out the totals of that collectable.
The collectables data is now displayed in a small box on the screen which a user can place on their own stream so everyone can see their total count.
The data will also be sent to a server. The server reads everyones incomeing data and displays it on the screen.
This data then can be streamed to the stats tracking stream showing who is in the lead with how many totals.
This automates the process of finding out who is in the lead making it so the helpers do not need to struggle to keep up with the counts.

# How To Use
Only works for n64 right now!!!
The way this program works is that it reads the game for a window which is a small portion of your screen.


Settings File

	Do not mess with Enter, there needs to be only 2 lines in the file
	Line 1: Put your username here
	Line 2: Put the ip of the server you want to connect to. 
	
Setup gameplay reading	

	Open the Application (exe file)
	Once Open press the T key on the keyboard to open the screen positioning window.
		This window is used to display where in your monitor the application is looking for your gameplay.
		The window that pops up is only for visuals and you do not pace your gameplay over it, it only shows what is on your desktop. So move your gameplay around on your desktop.
		The Red Box indecates where your gameplay should be, and shold take up the entirety of the box. That is 4:3 at 680x510 on amaRec.
		The redbox is defaulted to the top left of your sceen to keep it out of the way however you can move it to the center of your screen if you press the C key.
		After you have aligned your gameplay press T again to close the window. 
	Now you can start to use the Application
		
Gameplay

	Use the Arrow keys on your key board to scroll through the games to select the current game you are on.
	If you are on a game and you collect somthing for that game it will automatically update. Its that easy.
	
Online Feature

	This Application has the ablity to connect to a server to send its data.
	To turn on online mode all you need to do is press S. 
	If you have the proper IP adress typed into the settings.txt it will try to connect. 
	If the connection accepts, it will say Online on the main screen.
	You will now be sending your data to the server everytime you collect a collectable.
	To exit online mode jsut press S again.
	
KeyBoard Controls

	Escape: Close the Program
	Arrow Keys: Scroll through games
	S: Start your connection to the server
	T: Toggle current screen tracking. (If on the main screen you can see where you need to place your gameplay on the screen, otherwise it shows the spot where the totals will be tracked from)
	1: Toggle 100 Jiggies (incase app/computer crashes you have a way to get the totals back)
	2: Toggle 90 Jiggies
	3: Toggle 201 Banana
	Q: Give yourself a Jiggy (Bk only)
	W: Subtract a Jiggy (Bk only
	C: Change to center screen captureing
	


# Dev Install (Windows)

Install Anaconda 2.7(A python install that gives easy ways to install modules) https://www.continuum.io/downloads

Once python is installed use the commands in a command prompt: conda install -c https://conda.binstar.org/menpo opencv

There you go everything needed is installed. Now you can go to your folder where the program is and click on it to run.
You may have to open it as a python file by open with; then set the application to c:\where ever your anaconda install is\anaconda2\python
