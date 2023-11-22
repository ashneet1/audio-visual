#Modified vad.py

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# For more details about silero-vad see https://github.com/snakers4/silero-vad
# Usage: python3 vad.py


import torch
import numpy as np
import os
torch.set_num_threads(1)
from pprint import pprint

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=False)

#utils has 5 variables now (before it was 7)
#get_speech_ts_advanced was deleted
print("utils:",utils)
(get_speech_ts,
 _, read_audio,
 _, _) = utils

MAX_NUMBER_OF_FILES = 10000
for n in range(MAX_NUMBER_OF_FILES):
    if not os.path.isfile('audios/' + str(n) + '.wav'):
        continue
    wav = read_audio('audios/' + str(n) + '.wav')
    print(wav.shape[0])
    #was get_speech_ts_advanced
    #deleted some arguments as they aren't supported by get_speech_ts
    speech_timestamps = get_speech_ts(wav, model)
    mask = np.zeros((wav.shape[0],), dtype=int)
    for k in range(len(speech_timestamps)):
        start = speech_timestamps[k]['start']
        end = speech_timestamps[k]['end']
        print(start, end)
        mask[start:end] = 1
    end

    np.savetxt('vads/' + str(n) + '.txt', mask, fmt='%d')
    
