#!/usr/bin/python3
import datetime
import glob
import os
import json
from random import randint

class Emotions:

    def __init__(self, path_to_lib):
        self.emo_lib = path_to_lib
        self.emotion_time = datetime.datetime.now()
        self.index = -1
        self.index = self.get_new_emo_index()
        self.messages = {}

        for emo_dir in self.emotions:
            emo_name = os.path.split(emo_dir)[1]
            self.messages[emo_name] = self.read_state_file('%s/state.json' % emo_dir)


    @property
    def emotions(self):
        return glob.glob('%s/emo_*' % (self.emo_lib))


    @property
    def state(self):
        time_diff = datetime.datetime.now() - self.emotion_time
        time_diff = divmod(time_diff.days * 86400 + time_diff.seconds, 60)
        if time_diff[1] > 5 and time_diff[0] >= 0:
            self.index = self.get_new_emo_index()
        return os.path.split(self.emotions[self.index])[1]


    @property
    def message(self):
        max_range = len(self.messages[self.state])
        msg_index = randint(0, max_range - 1)
        return self.messages[self.state][msg_index]


    @property
    def gif_path(self):
        emo_gifs = glob.glob('%s/%s/*.gif' % (self.emo_lib, self.state))
        max_range = len(emo_gifs)
        gif_index = randint(0, max_range - 1)
        return emo_gifs[gif_index]


    def get_new_emo_index(self):
        max_range = len(self.emotions)
        new_index = randint(0, max_range - 1)
        if new_index == self.index:
            new_index += 1
        if new_index >= max_range:
            new_index = 0
        return new_index


    def read_state_file(self, path):
        if not os.path.exists:
            return []
        state_content = '{ "message" : [] }'
        with open(path, 'r') as file_obj:
            state_content = file_obj.read()

        return json.loads(state_content)['message']
