
        # Displaying text count on screen
        cv2.rectangle(img, (0,250),(130,400),(0,255,0),cv2.FILLED)
        cv2.putText(img, str(fingersCount), (45,350), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,0,0),5)

    # Displaying Frame per Second
    # The time() funct