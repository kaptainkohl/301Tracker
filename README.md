# 301Tracker
This is an application made solely for the Rareware 301 Collectathon Race http://bombch.us/Bj_W

This program uses opencv to look at an image of gameplay and search for objects, in this case Jiggies and Golden Bananas.
It finds them on the screen then looks at the numbers to the right of them. It then image reconizes the numbers to figure out the totals of that collectable.
The collectables data is now displayed in a small box on the screen which a user can place on their own stream so everyone can see their total count.
The data will also be sent to a server. The server reads everyones incomeing data and displays it on the screen.
This data then can be streamed to the stats tracking stream showing who is in the lead with how many totals.
This automates the process of finding out who is in the lead making it so the helpers do not need to struggle to keep up with the counts.

# Install (Windows)

Install Anaconda (A python install that gives easy ways to install modules) https://www.continuum.io/downloads

Once python is installed use the commands in a command prompt: conda install opencv

There you go everything needed is installed. Now you can go to your folder where the program is and click on it to run.
You may have to open it as a python file by open with; then set the application to c:\where ever your anaconda install is\anaconda2\python
