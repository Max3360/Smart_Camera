import subprocess
from Yolo import process_video
#cap = cv2.VideoCapture(0) # For Webcam
cap.set(3, 1280)
cap.set(4, 720)
subprocess.run(['python','lnstall_Update.py'])
video_path = "C:/Downloads/Smart_Camera/vdo_00.mp4" # For Vidro
process_video(video_path)
