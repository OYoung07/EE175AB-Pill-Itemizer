import cv2 #importing cv2 libraries
import os #importing os libraries
import numpy as np #importing numpy libraries
import serial #used to communicate with the arduino
import time #mainly used for the sleep function

## testing opencv functionalities / displaying image from directories

#file_name = os.path.join(os.path.dirname(__file__), 'goku.jpg') #cv2.imread doesn't work immediately for this directory - had to resort to using os.path instead.

#img = cv2.imread(file_name, -1) #reads the file, -1 means that it will print out in color
#img = cv2.resize(img, (500, 500)) #resize 

#cv2.imshow('Image', img) #prints out the image
#cv2.waitKey(0) #waits indefinitely until a user input is registered
#cv2.destroyAllWindows() 

##

ser = serial.Serial('COM8',9600) #interact with arduino 
time.sleep(2)
state = 1

#due to computational limitations, our group has decided to not include the GUI in order to save on processing power. 

#def displayGUI():
#	guiBackground = os.path.join(os.path.dirname(__file__), 'gui_background.jpg')
#	guiBackground = cv2.imread(guiBackground, -1)
#	width = int(guiBackground.shape[1] * 20 / 100)
#	height = int(guiBackground.shape[0] * 20 / 100)
#	dimension = (width, height)
#	resizedGUIBackground = cv2.resize(guiBackground, dimension, interpolation = cv2.INTER_AREA)
#	font = cv2.FONT_HERSHEY_SIMPLEX
#	guiBackground = cv2.putText(resizedGUIBackground, 'Red Pills:', (0, 25), font, 1, (0, 0, 255), 2, cv2.LINE_AA) #name, file, text being displayed, position (starting from top left corner), font, scale, color of text, line thickness, including anti-aliasing)
#	guiBackground = cv2.putText(resizedGUIBackground, 'Blue Pills:', (0, 75), font, 1, (0, 165, 255), 2, cv2.LINE_AA)
#	guiBackground = cv2.putText(resizedGUIBackground, 'Yellow Pills:', (0, 125), font, 1, (0, 215, 255), 2, cv2.LINE_AA)
#	guiBackground = cv2.putText(resizedGUIBackground, 'Total Pills:', (0, 175), font, 1, (0, 25, 0), 2, cv2.LINE_AA)
#	#for position: 
#	#increasing x value will move text to the right
	#increase y value will move text it downwards
#	guiBackground = cv2.putText(resizedGUIBackground, str(redCount), (145, 27), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
#	guiBackground = cv2.putText(resizedGUIBackground, str(blueCount), (198, 77), font, 1, (0, 165, 255), 2, cv2.LINE_AA)
#	guiBackground = cv2.putText(resizedGUIBackground, str(yellowCount), (180, 127), font, 1, (0, 215, 255), 2, cv2.LINE_AA)
#	guiBackground = cv2.putText(resizedGUIBackground, str(totalCount), (160, 177), font, 1, (0, 25, 0), 2, cv2.LINE_AA)
#	cv2.imshow('GUI', resizedGUIBackground)																																																																																																ackground)

def takeScreenshot():
	global screenshot
	screenshot = []
	screenshot = cap.read()[1]
	colorDetection();
	cv2.circle(screenshot, (crosshairColorX, crosshairColorY), 5, (0, 255, 0), 3) #this crosshair will be green 
	cv2.imshow('Screenshot', screenshot) #display screenshot

def shutDown():
	cap.release()
	cv2.destroyAllWindows()

def colorDetection():
	global color
	global hueValue #range is 0-179
	global saturationValue #range is 0-255
	global brightnessValue #range is 0-255
	global hsv
	global totalCount #this will only count red,orange,yellow pills
	global redCount 
	global blueCount 
	global yellowCount 
	global differentCount 
	global state

	screenshotConversion = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV) #hsv - hue, saturation, value
	crosshairColorCenter = screenshotConversion[crosshairColorY, crosshairColorX]
	hueValue = crosshairColorCenter[0] 
	saturationValue = crosshairColorCenter[1] 
	brightnessValue = crosshairColorCenter[2]

	#print("THE HUE VALUE IS")
	#print(hueValue)
	#print("THE SATURATION VALUE IS")
	#print(saturationValue)
	#print("THE BRIGHTNESS VALUE IS")
	#print(brightnessValue)

	#initializing the boundaries for the colors' hsv

	#for red/blue/yellow, the hsv values are not standard. they are altered to make it work in our current lighting conditions.

	redLB = np.array([0, 50, 65]); 
	redUB = np.array([3, 255, 255]);

	blueLB = np.array([100, 50, 40]);
	blueUB = np.array([128, 255, 255]);

	yellowLB = np.array([19, 50, 70]);
	yellowUB = np.array([35, 255, 255]);

	#assigns with hsv
	hsv = np.array([hueValue, saturationValue, brightnessValue]);

	print("HSV IS");
	print(hsv);

	if (np.all(hsv >= redLB)) and (np.all(hsv <= redUB)):
		color = "RED"
		if(state == 2):
			mes = "CW"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
		elif(state == 3):
			mes = "CCW"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
		redCount += 1 
		totalCount += 1
		print("THE OBJECT IS RED")
		state = 1;
	elif (np.all(hsv >= blueLB)) and (np.all(hsv <= blueUB)):
		color = "BLUE"
		if(state == 1):
			mes = "CCW"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
		elif(state == 3):
			mes = "CCW2"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
		blueCount += 1
		totalCount += 1
		state = 2;
		print("THE OBJECT IS BLUE")
	elif (np.all(hsv >= yellowLB)) and (np.all(hsv <= yellowUB)):
		if(state == 1):
			mes = "CW"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
		elif(state == 2):
			mes = "CW2"
			ser.write(mes.encode('utf-8'))
			time.sleep(5)
			mes = "RESET"
			ser.write(mes.encode('utf-8'))
		print("THE OBJECT IS YELLOW")
		color = "YELLOW"
		yellowCount += 1
		totalCount += 1
		state = 3
	else:
		color = "DIFFERENT"
		differentCount += 1
		print("THE OBJECT IS NOT RED/BLUE/YELLOW")

	#print("CROSSHAIR ONE COLOR IS:")
	#print(crosshairBlueColor)

	#print("CROSSHAIR TWO COLOR IS: ")
	#print(crosshairRedColor)

	return color

cap = cv2.VideoCapture(1) #this will turn on the USB camera
#cap = cv2.VideoCapture(0); #this will turn on the laptop's camera
totalCount = 0;
redCount = 0;
blueCount = 0;
yellowCount = 0;
differentCount = 0;


while True: #loop infintely, take feedback from camera
	ret, frame = cap.read() #ret -> will return false if the camera is being used in another application

	width = int(cap.get(3))
	height = int(cap.get(4))
	#print(width) - 640p
	#print(height) - 480p

	crosshairColorX = int(width / 3)
	crosshairColorY = int(height / 1.35)

	crosshairBlueX = int(width / 2.5)
	crosshairBlueY = int(height / 1.35)

	crosshairRedX = int(width / 3)
	crosshairRedY = int(height / 1.35)

	#the idea is to have two crosshairs displayed on the live feed.
	#the red crosshair is the same location as the crosshair that will read the color of the object
	#to automate this process, we want to compare the red and blue crosshair's color
	#initially, the red and blue crosshairs are reading the background of the shaking mechanism, which will be the same color.
	#whenever the two crosshairs' color are different, this will indicate that a pill has crossed the location

	cv2.circle(frame, (crosshairBlueX, crosshairBlueY), 5, (255, 0, 0), 3) #this crosshair is blue
	cv2.circle(frame, (crosshairRedX, crosshairRedY), 5, (0, 0, 255), 3) #this crosshair is red

	liveFeedConversion = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	crosshairBlueCenter = liveFeedConversion[crosshairBlueY, crosshairBlueX]
	crosshairBlueColor = crosshairBlueCenter[0]

	crosshairRedCenter = liveFeedConversion[crosshairRedY, crosshairRedX]
	crosshairRedColor = crosshairRedCenter[0]

	cv2.imshow('Live Feed', frame)

	#displayGUI()

	if cv2.waitKey(1) == ord('q'): #live feed will stop when q is pressed
		shutDown();
	if (crosshairRedColor > (crosshairBlueColor + 10)) or ((crosshairRedColor + 10) < crosshairBlueColor):
		takeScreenshot();
		time.sleep(0.5)
	#if cv2.waitKey(1) == ord('w'): #take a screenshot of the live feed when w is pressed
	#	takeScreenshot();