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



cap = cv2.VideoCapture(video_path)

_, img = cap.read()
N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) -2)
print("N", N)

# DG = 1
CNT = 300
phis = np.linspace(0, 360, CNT)

for phi_deg in phis:
    p_rad = np.deg2rad(phi_deg)
    cv2.line(img, circle_center, tuple((np.array(circle_center) + radius*np.array([np.cos(p_rad), np.sin(p_rad)])).astype(np.int32))
             , (0, int(255 - 255*phi_deg/360), int(255*phi_deg/360)), 2)

cv2.imshow("lines", img)
cv2.waitKey(0)

xx, yy = np.meshgrid(np.arange(0, img.shape[1]), np.arange(0, img.shape[0]))
xx_s = xx - circle_center[0]
yy_s = yy - circle_center[1]

dist = np.abs(np.sqrt(np.power(xx_s, 2) + np.power(yy_s, 2)) - radius)
phi = np.rad2deg(np.arctan2(yy_s, -xx_s)) +180

phi_i = np.clip(np.round(phi * (CNT-1) / 360).astype(np.int32), 0, CNT-1)


cv2.imshow("dist", (dist/ np.max(dist)).astype(np.float32))
cv2.imshow("phi", (phi / 360).astype(np.float32))
cv2.imshow("phi_i", (phi_i / 360).astype(np.float32))


mask = dist < 10

polar_img_max = np.zeros((N, CNT), np.float32)
polar_img_cnt = np.zeros((N, CNT), np.int32)
polar_img_sum = np.zeros((N, CNT), np.float32)

def scale(i):
    out = i - np.min(i); out /= np.max(out)
    return out

for jj in range(0, N):
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.

    for i, v in zip(phi_i[mask], gray[mask]):
        # print(i, v)
        polar_img_max[jj, i] = max(v, polar_img_max[jj, i])
        # polar_img_cnt[jj, i] += 1
        # polar_img_sum[jj, i] += v
    cv2.imshow("polar_img_max", scale(polar_img_max))
    cv2.waitKey(1)
# polar_img_mean = polar_img_sum/polar_img_cnt
# cv2.imshow("polar_img_mean", scale(polar_img_mean))
# cv2.imshow("polar_img_cnt", scale(polar_img_cnt))
# cv2.waitKey(1)

cap.release()


cv2.waitKey(0)

np.save(open(video_path + ".i_t_phi.npy", "wb"), polar_img_max)





