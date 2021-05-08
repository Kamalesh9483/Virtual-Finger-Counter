import cv2
import os       # For operating system dependent functionality 
                # eg. listing Return a list containing the names of the entries in the directory given by path
import time     # For time related functionality
import HandTrackingModule as htm

# setting video capture mode
cap = cv2.VideoCapture(0)
cap.set(3,1000) 
cap.set(4,1000)

# including images from directory
folderPath = 'Finger images'
fingerList = os.listdir(folderPath) 
print(fingerList)

# creating Overlay list to display on the output window
overLay = []

for finger in fingerList:
    image = cv2.imread(f'{folderPath}/{finger}')
    # print(f'{folderName}/{finger}')
    overLay.append(image)
    
print(len(overLay))
previousTime = 0

# initializing the object 'detector' 
# using the HandDetection() class from the module HandTrackingModule (htm)
detector = htm.HandDetection(DetectionConfidence= 0.75)

# Creating list to store ID no of tip positions of each finger
# Refer Landmarks.png for finger Landmark positions
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    # Accessing findHands() method from class HandDetection() from HandTrackingModule (htm)
    # to draw the landmarks on the webcam output
    detector.findHands(img,True)

    # Accessing detectPosition() method from the class HandDetection() from HandTrackingModule (htm)
    lmList = detector.detectPosition(img, draw=False)
    # print(lmList)

    # Extracting tip position Landmark of thumb, index, middle, ring, pinky fingers
    # from mediapipe source --- tip of (thumb - 4), (index - 8)
    # (middle - 12), (ring - 16), (little - 20)
    # conditionally checking the position of each tip positions of fingers with 2nd node of finger
    # lmList[a][b] means from (a - tip of finger), we are taking (b - y position of corresponding finger)

    if len(lmList) != 0:
        fingers = []

# creating for loop for thumb finger which has 2 sections
# if thumb tip's (landmark 4) x point is to left of  landmark 3
# then the thumb is closed else it is open   
# Conditional command for left and hand right as the left and right hand are lateral inversions 
        if lmList[0][1] < lmList[4][1]:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        else:
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

# Creating for loop for 4 fingers which has 3 sections
# except thumb finger that has only 2 sections 
# and so behave differently from other fingers
        for id in range(1,5):       
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # print(fingers)
# count() is a method in list that counts the number of count of arguments passed
            fingersCount =  fingers.count(1)
            # print(fingersCount)

    # Alloting height X width pixels in outut window for displaying overlay images
    # Note: Pixel height and width of each image may vary
    # using  .shape to get height, width, channel details of each image 
    #  Number of Channels = 4 means ---  Alpha, Red, Green and Blue chann
            height, width, channel = overLay[fingersCount-1].shape
            img[0:height, 0:width] = overLay[fingersCount-1]
    
        # Displaying text count on screen
        cv2.rectangle(img, (0,250),(130,400),(0,255,0),cv2.FILLED)
        cv2.putText(img, str(fingersCount), (45,350), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,0,0),5)

    # Displaying Frame per Second
    # The time() function returns the number of seconds passed since epoch(the point where time begins)
    currentTime = time.time()
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime
    # Note: f"{} is literal string interpolation. values within {} is dynamic
    cv2.putText(img,f"FPS is {str(int(fps))}",(0,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)
    
    cv2.imshow("Finger counter",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break