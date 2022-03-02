#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Usage: python3 format_asd_with_smoothing_vad.py asd_results_dir vad_results_dir data_set 

import os
import cv2 as cv
import numpy as np
import sys

asd_results_dir = sys.argv[1]
vad_results_dir = sys.argv[2]
data_set = sys.argv[3] # 'test' or 'val'

if not os.path.isfile(data_set + '.txt'):
   sys.exit(data_set + ' list does not exist.')

with open('v.txt') as f:
    content = f.readlines()
filenames = [x.strip() for x in content]

vlist = np.loadtxt(data_set + '.txt')
vlist = vlist.astype('int').tolist()

sys.stdout.write('\033[K')

for fileno in vlist:
    print(fileno, end = '\r')
    vad = np.loadtxt(vad_results_dir + '/' + str(fileno) + '.txt')    
    res = np.loadtxt(asd_results_dir + '/' + str(fileno) + '.txt', delimiter=' ')
    if len(res.shape) == 1:
        res = np.expand_dims(res, axis=0)
    
    box = {};
    for n in range(res.shape[0]):
        if not (res[n][0] in box):
           box[res[n][0]] = []
        box[res[n][0]].append([res[n][1], res[n][2], res[n][3], res[n][4], res[n][5], res[n][6], res[n][7]]);
        

    for frame_num in range(9000):
        asp = []
        if frame_num in box:
           b = box[frame_num]
           for k in range(len(b)):
               pid = int(b[k][0])
               x1 = int(b[k][1])
               y1 = int(b[k][2])
               x2 = int(b[k][3])
               y2 = int(b[k][4])
               speak = int(b[k][5])
               speakf = float(b[k][6])
               for m in range(-5,6):
                   if (frame_num + m in box):
                       for n in range(len(box[frame_num + m])):
                           if box[frame_num + m][n][0] == pid:
                                speakf = max(speakf, box[frame_num + m][n][6])

               aind = int(frame_num/30*16000) 
               if aind >= vad.shape[0]:
                  aind = vad.shape[0]-1 

               if vad[aind] == 0:
                  speakf = 0

               asp.append([1, speakf, x1, y1, x2, y2])

        if len(asp) > 0:       
            np.savetxt('detection-results/' + str(fileno) + '_' + str(frame_num) + '.txt', asp, fmt='%d %f %d %d %d %d', delimiter=' ')
        else:
            np.savetxt('detection-results/' + str(fileno) + '_' + str(frame_num) + '.txt', asp, fmt='%d', delimiter=' ')
            
