import cv2
import os       # For operating system dependent functionality 
                # eg. listing Return a list containing the names of the entries in the directory given by path
import time     # For time related functionality
import HandTrackingModule as htm


# setting video capture mode
cap = cv2.VideoCapture(0)
cap.set(3,1500) 
cap.set(4,1500)

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



while True:
    success, img = cap.read()
    # Accessing findHands() method from class HandDetection() from HandTrackingModule (htm)
    detector.findHands(img,True)



    # Alloting height X width pixels in outut window for displaying overlay images
    # Note: Pixel height and width of each image may vary
    # using  .shape to get height, width, channel details of each image 
    #  Number of Channels = 4 means ---  Alpha, Red, Green and Blue chann
    height, width, channel = overLay[0].shape
    img[0:height, 0:width] = overLay[5]
    
    # Displaying Frame per Second
    # The time() function returns the number of seconds passed since epoch(the point where time begins)
    currentTime = time.time()
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime
    # Note: f"{} is literal string interpolation. values within {} is dynamic
    cv2.putText(img,f"FPS is {str(int(fps))}",(400,700),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)
    
    cv2.imshow("Finger counter",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break