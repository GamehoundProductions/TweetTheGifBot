#!/usr/bin/python3
import json
import os
from pdb import set_trace

from TweetBot.routine import Routiner

class TweetAnalyzer(Routiner):

    def __init__(self, db_path):
        self.db_path = db_path
        if not self.validate_dir(db_path):
            raise RuntimeError('%s is not a valid path in %s! '\
                                 ' One of the directories does not exist!' %\
                                    (self.__class__.name, db_path))
        self.db = {}
        self.db = self.read_db(db_path)


    def validate_dir(self, path):
        dir = os.path.split(path)[0]
        return os.path.exists(dir)


    def Update(self, **kwargs):
        '''
        @param tweets: list of tweets to analyze.
        '''
        super().Update(**kwargs)

        a_tweet = kwargs.get('a_tweet', [])
        if kwargs.get('tweets', []) is None:
            print('WordCounter.Update() is missing "tweets" parameter or is an empty list!')

        analyzed = self.process(a_tweet)

        if kwargs.get('dry_run', False) is False:
            self.write_db()

        return analyzed


    def process(self, a_tweet):
        '''
        @param a_tweet: tweet object (with full_text param) to analyze
        @return dict: <str>:<int> occurrence of words in the given tweet
        '''
        raise NotImplementedError('"count() routine is not implemented in the "%s"' %\
                                    self.__class__.name)


    def read_db(self, path):
        db = None
        file_content = None
        print(' - Reading DB: %s' % path)
        if os.path.exists(path):
            with open(path, 'r+') as file_obj:
                file_content = file_obj.read()
        else:
            file_content = '{}'

        if file_content == '': #paranoia when handling "empty" file
            file_content = '{}'

        db = json.loads(file_content)
        return db


    def write_db(self, path=None):
        if path is None:
            path = self.db_path
        if self.db is None:
            self.db = self.read_db(path)

        print(' - Writing DB: %s' % path)
        db_str = json.dumps(self.db)

        with open(path, 'w') as file_obj:
            file_obj.write(db_str)