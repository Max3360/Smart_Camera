import os
import cv2
import math
import time
import requests
import numpy as np
import cvzone
from ultralytics import YOLO

def send_notification_with_image(image_path, message):
    # Token you received from notify-bot line
    token = 'vkdjrtklldicnywlpefkwytphjawefrgpiolk'  
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # Create payload and files to send
    payload = {'message': message}
    files = {'imageFile': open(image_path, 'rb')}
    response = requests.post(url, headers=headers, data=payload, files=files)
    print(response.text)

last_save_time = time.time()

vdo_folder = "C:/Smart_Camera/Record/VDO" # Address of VDO file
if not os.path.exists(vdo_folder):
    os.makedirs(vdo_folder)
vdo_filename = os.path.join(vdo_folder, "record_video.mp4") # Set the VDO file name
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Create a VideoWriter
out = cv2.VideoWriter(vdo_filename, fourcc, 20.0, (916, 916))  # 20.0 is frame rate, (916, 916) is the size of frame

record_folder = "C:/Smart_Camera/Record/Picture" # Address of Picture file
if not os.path.exists(record_folder):
    os.makedirs(record_folder)

def process_video(video_path):
    model = YOLO('yolov8n.pt') # Run yolov8n.pt

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
                ]

    prev_frame_time = 0
    new_frame_time = 0
    cap = cv2.VideoCapture(video_path)
    # Set area with bounding box
    # (x  width y height )
    x, y, width, height = 110, 410, 650, 400  # Examples of width and height values and given as examples.
    areal = [(x, y), (x, y + height), (x + width, y + height), (x + width, y)]
    last_save_time = time.time()
    while True:
        new_frame_time = time.time()
        success, img = cap.read()
        if not success:
            print('No Video.......')
            break
        desired_size = (916, 916)  # Set VDO size 
        resized_frame = cv2.resize(img, desired_size)
        results = model(resized_frame, stream=True) # Run model (yolov8n.pt)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cx = int((x1 + x2) // 2)
                cy = int((y1 + y2) // 2)
                # Verify that the falling point is within the areal and has the appearance of a person.
                result = cv2.pointPolygonTest(np.array(areal, np.int32), ((cx, cy)), False)
                is_person = int(box.cls[0]) == classNames.index('person')  # Check if it's a person or not.
                cv2.polylines(resized_frame, [np.array(areal, np.int32)], True, (0, 0, 255), 2)
                # If the position falls in areal and is a person
                if result >= 0 and is_person:
                    cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 0, 255), 1) # create red frame
                    conf = math.ceil((box.conf[0] * 100)) / 100 # Calculate the confidence value
                    cls = int(box.cls[0])
                    cvzone.putTextRect(resized_frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                    current_time = time.time()
                    if current_time - last_save_time >= 10:
                        # Save the image to the "Record" folder.
                        image_path = os.path.join(record_folder, f"person_{cx}_{cy}.png")
                        cv2.imwrite(image_path, resized_frame)
                        # Send LINE Notify and delete image files after sending.
                        send_notification_with_image(image_path, "Object detected!")
                        last_save_time = current_time  # Update last recorded time
        out.write(img)
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        print(fps)
        
        # Displays the resized image.
        cv2.imshow("Resized Frame", resized_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

