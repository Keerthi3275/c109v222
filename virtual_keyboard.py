import cv2
import mediapipe as mp
#import the Key and controller class from the pynput.keyboard module

#Initialize the controller


cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]
#Create a variable state with initial values as None.


def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmark

        fingers = []

        for lm_index in tipIds:
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)

        
        totalFingers = fingers.count(1)
         # PLAY or PAUSE a Video
        if totalFingers == 4:
            state = "Play"

        if totalFingers == 0 and state == "Play":
            state = "Pause"
            keyboard.press(Key.space)
        # Move Video FORWARD & BACKWARDS   
        finger_tip_x = (landmarks[8].x)*width
 
        if totalFingers == 1:
            if  finger_tip_x < width-400:
                print("Play Backward")
                keyboard.press(Key.left)

            if finger_tip_x > width-50:
                print("Play Forward")
                keyboard.press(Key.right)
        
        
def drawHandLanmarks(image, hand_landmarks):

    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    results = hands.process(image)

    hand_landmarks = results.multi_hand_landmarks

    drawHandLanmarks(image, hand_landmarks)

    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # write condition to Quit the window on pressing Spacebar key
    key = cv2.waitKey(1)
    

cv2.destroyAllWindows()
