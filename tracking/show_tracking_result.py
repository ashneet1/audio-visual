#!python3 show_tracking_result.py /content/egocentric/audio-visual/data/v2/clips 222
#modified show_tracking_result.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: python3 show_tracking_result video_directory video_id

import os.path
import cv2 as cv
import numpy as np
import sys

with open('v.txt') as f:
    content = f.readlines()
filenames = [x.strip() for x in content]

# current directory
currDir = os.getcwd()

videodir = sys.argv[1] #replace with video directory
fileno = int(sys.argv[2]) #replace with index of video
res = np.loadtxt('global_tracking/results/' + str(fileno) + '.txt', delimiter=' ')
res = res.astype('int')
if len(res.shape) == 1:
    res = np.expand_dims(res, axis=0)

box = {}

for n in range(res.shape[0]):
    if not (res[n][0] in box):
       box[res[n][0]] = []
    box[res[n][0]].append([res[n][1], res[n][2], res[n][3], res[n][4], res[n][5]])

fname = videodir + '/' + filenames[fileno]

cap = cv.VideoCapture(fname)

# sets up video writer
fps = cap.get(cv.CAP_PROP_FPS)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) // 2)
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) // 2)
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('output.mp4', fourcc, fps, (width, height))

frame_num = 0
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    if frame_num in box:
       b = box[frame_num]
       for k in range(len(b)):
           pid = int(b[k][0])
           x1 = int(b[k][1])
           y1 = int(b[k][2])
           x2 = int(b[k][3])
           y2 = int(b[k][4])

           cv.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 5)
           font = cv.FONT_HERSHEY_SIMPLEX
           fontScale = 2
           color = (255, 0, 0)
           thickness = 5
           cv.putText(frame, str(pid), ((x1+x2)//2,(y1+y2)//2), font,
                   fontScale, color, thickness, cv.LINE_AA)

    frame = cv.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
    #write the video
    out.write(frame)
    frame_num = frame_num + 1

# Release the video capture and writer objects
cap.release()
out.release()
cv.destroyAllWindows()

