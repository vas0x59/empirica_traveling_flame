import cv2
import numpy as np
import sys
import pickle
import os


video_path = sys.argv[1]

if os.path.exists(video_path + ".cricle.pickle"):
    circle_center, radius = pickle.load(open(video_path + ".cricle.pickle", "rb"))
else:
    # Initialize variables
    circle_center = None
    radius = 0
is_drawing = False
is_dragging = False
is_resizing = False 
def update_display(frame):
    """Function to update the display window with the current circle."""
    temp_frame = frame.copy()
    if circle_center is not None and radius > 0:
        cv2.circle(temp_frame, circle_center, radius, (0, 255, 0), 2)
        cv2.circle(temp_frame, circle_center, 5, (0, 0, 255), -1)  # Mark center
    cv2.imshow("Interactive Circle Selector", temp_frame)

def mouse_callback(event, x, y, flags, param):
    global circle_center, radius, is_drawing, is_dragging, is_resizing
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if circle_center is None:
            circle_center = (x, y)
            is_drawing = True
        else:
            dist = np.linalg.norm(np.array([x, y]) - np.array(circle_center))
            if dist < 10:  # Clicked near center
                is_dragging = True
            elif abs(dist - radius) < 10:  # Clicked near edge
                is_resizing = True
            else:
                radius = int(dist)
                is_drawing = True
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing and circle_center is not None:
            radius = int(np.linalg.norm(np.array([x, y]) - np.array(circle_center)))
        elif is_dragging:
            circle_center = (x, y)
        elif is_resizing:
            radius = int(np.linalg.norm(np.array([x, y]) - np.array(circle_center)))
        
    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        is_dragging = False
        is_resizing = False
    update_display(param)

# Read video path from command-line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <video_path>")
    sys.exit(1)

cap = cv2.VideoCapture(video_path)

canvas_size = (500, 500, 3)
_, canvas = cap.read()
if not cap.isOpened():
    print("Error: Could not open video.")
    sys.exit(1)

cv2.namedWindow("Interactive Circle Selector")
cv2.setMouseCallback("Interactive Circle Selector", mouse_callback, canvas)

while True:
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key to exit
        break

    if key == ord("s"):
        pickle.dump((circle_center, radius), open(video_path + ".cricle.pickle", "wb"))
    if key == ord("n"):
        ret, frame = cap.read()
        if not ret:
            break
        canvas[:, :, :] = frame[:, :, :]
        update_display(canvas)

cap.release()
cv2.destroyAllWindows()

pickle.dump((circle_center, radius), open(video_path + ".cricle.pickle", "wb"))


