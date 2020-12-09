import os
import time
from PIL import Image
import cv2
import numpy as np
import Main
import VehicleInfo


def detect_image(image_path):
    Main.showSteps = True
    DetectChars = Main.startDetection()
    frame = cv2.imread(image_path)
    # get image name by using split method
    image_name = image_path.split('/')[-1]
    image_name = image_name.split('.')[0]
    output = "Output/Images/" + image_name + ".jpeg"

    result,number = Main.main(DetectChars,frame)
    vehicle = VehicleInfo.GetVehicle(number)
    print("Owner: ",vehicle.Owner)
    print("Vehicle Model: ", vehicle.Manufacturer + " " + vehicle.Model)
    print("----------------------------------------")
    print("----------------------------------------\n")
    cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
    
    cv2.imshow("result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(output,result)



def detect_video(video_path):

    input_size = 416
    output_format = 'X264'
    output = "Output/Videos/"

    # get video name by using split method
    video_name = video_path.split('/')[-1]
    video_name = video_name.split('.')[0]

    output = output + video_name + ".mp4"

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    Main.showSteps = False
    DetectChars = Main.startDetection()

    # by default VideoCapture returns float instead of int
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*output_format)
    out = cv2.VideoWriter(output, codec, fps, (width, height))

    frame_num = 0
    while True:
        return_value, frame = vid.read()
        if return_value:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_num += 1
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break

        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = frame.shape

        result,number = Main.main(DetectChars,frame)
        
        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        # result = np.asarray(image)
        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        # result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        cv2.imshow("result", result)
        
        out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()


while True:
    print("What do you wish to run the algo on: ")
    print("1. Image")
    print("2. Video")
    print("0. Exit")
    opt = input()
    if opt == "0" or opt == "Exit":
        break
    if opt == "1" or opt == "Image":
        path = input("Enter the image path: ")
        detect_image(path)
    if opt == "2" or opt == "Video":
        path = input("Enter the video path: ")
        detect_video(path)
