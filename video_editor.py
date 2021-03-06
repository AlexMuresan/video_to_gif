import sys
import time
import pathlib
import datetime

import cv2
import imageio

def onChange(trackbarValue):
    global play_video
    if play_video:
        cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
        _,img = cap.read()

        scale_percent = 70 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        time.sleep(0.03)
        cv2.imshow("Video", img)
        pass


end = 10e-5

cv2.namedWindow('Video')
cv2.moveWindow('Video', 10, 40)

gathering = False
play_video = True

frames_for_gif = []


print("left and right arrows - scroll through video\n"
      "space or 'p' - pause and play the video\n"
      "'s' - select the start frame\n"
      "'e' - select the end frame and start gif greation\n"
      "esc - stop the program\n")

# Path for the video
# At the moment it is given as the first parameter 
# in the command line
video_path = pathlib.Path(sys.argv[1])
path_parent = video_path.parent / "gifs"
print(f"Loaded video from: {video_path}")
print(f"Gifs will be saved to: {path_parent}\n")

cap = cv2.VideoCapture(str(video_path))
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
cv2.createTrackbar("Progress", "Video", 0, int(total_frames), onChange)

while cap.isOpened():
    start = time.time()
    if play_video:
        _, img = cap.read()
    
    if gathering == True:
        frames_for_gif.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    k = cv2.waitKey(1) & 0xff
    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    cv2.setTrackbarPos("Progress", "Video", current_frame)

    # if k != 255:
    #     print(k)
    if k == 27:
        break
    if k == ord('p') or k == 32:
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        # cv2.waitKey(-1)
        play_video = not play_video
    if k == 81 or k == 123:
        cv2.setTrackbarPos("Progress", "Video", current_frame - 50)
    if k == 83 or k == 124:
        cv2.setTrackbarPos("Progress", "Video", current_frame + 50)
    if k == ord('s'):
        start_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        gathering = True
    if k == ord('e'):
        end_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        now = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
        gathering = False
        export_name = f"{start_frame}_{end_frame}_{now}.gif"
        export_path = path_parent / export_name
        print(f"Saving gif as {export_name}...")
        imageio.mimsave(export_path, frames_for_gif, 'GIF')
        frames_for_gif = []

    if play_video:
        scale_percent = 70 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
        time.sleep(0.03)
        cv2.imshow("Video", img)
        print(f"{int(current_frame)} / {int(total_frames)} - {int(1/end)} fps   ", end='\r')

    end = time.time() - start
    
