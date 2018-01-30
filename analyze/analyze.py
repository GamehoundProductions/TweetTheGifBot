#!/usr/bin/python3
import json
import os
from pdb import set_trace

from TweetBot import utils
from TweetBot.routine import Routiner


class TweetAnalyzer(Routiner):

    def __init__(self, db_path, repeat_limit=2):
        self.db_path = db_path
        if not utils.validate_dir(db_path):
            raise RuntimeError('%s is not a valid path in %s! '\
                                 ' One of the directories does not exist!' %\
                                    (self.__class__.name, db_path))
        self.db = {}
        self.db = self.read_db(db_path)
        self.repeat_limit = repeat_limit
        self.last_data = None


    def Update(self, **kwargs):
        '''
        @param tweets: list of tweets to analyze.
        '''
        print(' ------------ %s ------------' % self)
        super().Update(**kwargs)

        a_tweet = kwargs.get('a_tweet', [])
        if kwargs.get('tweets', []) is None:
            print('WordCounter.Update() is missing "tweets" parameter or is an empty list!')

        self.last_data = self.process(a_tweet)

        if kwargs.get('dry_run', False) is False:
            self.write_db()

        return self.last_data


    def process(self, a_tweet):
        '''
        @param a_tweet: tweet object (with full_text param) to analyze
        @return dict: <str>:<int> occurrence of words in the given tweet
        '''
        raise NotImplementedError('"count() routine is not implemented in the "%s"' %\
                                    self.__class__.name)


    def read_db(self, path):
        return utils.read_db(path)


    def write_db(self, path=None):
        if path is None:
            path = self.db_path
        if self.db is None:
            self.db = self.read_db(path)

        print(' - Writing DB: %s' % path)
        db_str = json.dumps(self.db)

        with open(path, 'w') as file_obj:
            file_obj.write(db_str)


    def react(self):
        raise NotImplementedError(' - reac() function of %s is not for use yet!' %\
                                self)
