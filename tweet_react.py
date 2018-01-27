#!/usr/bin/python3
import os
import random
import json
from glob import glob
from pdb import set_trace

from TweetBot.routine import Routiner


class TweetReact(Routiner):

    def __init__(self, path_to_phrases):
        self.path_to_phrases = path_to_phrases
        self.phrases = {}

        file_name = os.path.split(path_to_phrases)[1]
        file_name = file_name.split('.json')[0]
        print(' - Reading phrases for %s' % file_name)
        self.phrases = self.read_phrases(path_to_phrases)


    def read_phrases(self, path):
        '''
        @return: dict. <phrase name> : <Phrase obj>
        '''
        if not os.path.exists(path):
            print('Not a valid path %s for %s' %\
                                (path, self.__class__.name))
            return {}

        file_content = '{}'
        phrases_json = {}
        with open(path, 'r') as file_obj:
            file_content = file_obj.read()

        try:
            phrases_json = json.loads(file_content)
        except ValueError as err:
            print('Failed to parse json phrases at %s!' % (path))
            print(' - Reasong: %s' % err)

        result = {}
        for key, value in phrases_json.items():
            result[value['name']] = Phrase(value)

        return result


    def pick_random_phrase(self):
        keys = list(self.phrases.keys())
        if len(keys) == 0:
            return Phrase(None)
        rand_index = random.randint(0, len(keys) - 1)
        phrase_picked = keys[rand_index]
        phrase = self.phrases[phrase_picked]
        return phrase



class Phrase:

    def __init__(self, phrase):
        '''
        @phrase: dict parsd from phrases/*.json file (just one key) of form:
            "1": {
                "name" : "kw_use_1",
                "text" : "This use of '{target}' make me feel like...",
                "category" : "funny"
            },
        '''
        self.phrase = phrase
        if phrase is None:
            self.phrase = {
                '-1' : {
                    'name' : None,
                    'text' : '',
                    'category' : 'confused'
                }
            }


    @property
    def text(self):
        return self.phrase.get('text', '')

    @text.setter
    def text(self, value):
        self.phrase['text'] = value

    @property
    def category(self):
        return self.phrase.get('category', '')

    @property
    def name(self):
        return self.phrase.get('name', '')