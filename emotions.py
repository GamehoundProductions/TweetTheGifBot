#!/usr/bin/python3
import datetime
import glob
import os
import json
from random import randint

from pdb import set_trace

class Emotions:

    def __init__(self, path_to_lib):
        self.emo_lib = path_to_lib


    @property
    def emotions(self):
        return glob.glob('%s/emo_*' % (self.emo_lib))


    def pick_gif(self, category):
        if ('%semo_%s' % (self.emo_lib, category)) not in self.emotions:
            print('No such emo_ gif category: %s' % category)
            return None
        emo_gifs = glob.glob('%s/emo_%s/*.gif' % (self.emo_lib, category))
        max_range = len(emo_gifs)
        gif_index = randint(0, max_range - 1)
        return emo_gifs[gif_index]