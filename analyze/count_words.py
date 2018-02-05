#!/usr/bin/python3
from collections import defaultdict

from pdb import set_trace
from pprint import pprint

from TweetBot.analyze.analyze import TweetAnalyzer
from TweetBot.tweet_react import TweetReact


class WordCounter(TweetAnalyzer):

    def __init__(self, db_path, repeat_limit=1):
        super().__init__(db_path, repeat_limit=repeat_limit)


    def Update(self, **kwargs):
        # print('-------- WordCounter -------')
        return super().Update(**kwargs)


    def read_db(self, path):
        db = super().read_db(path)
        if db: # DB is not empty and constructed
            return db

        db['analyzed_id'] = []
        db['words'] = defaultdict(int)
        return db


    def process(self, a_tweet):
        '''
         Count words in the tweet and update self.db dict counters.

        @param a_tweet: tweet object (with full_text param) to analyze
        @return dict: <str>:<int> occurrence of words in the given tweet
        '''
        has_analyzed = False
        if a_tweet.id in self.db['analyzed_id']:
            print(' -- Words for %s already has been analyzed!' % a_tweet.id)
            has_analyzed = True

        result = defaultdict(int)

        for line in a_tweet.full_text.split('\n'):
            for word in line.split(' '):
                word = word.strip('\n')
                result[word] += 1
                if has_analyzed: #Dont write to DB since already been analyzed before
                    continue

                if word not in self.db['words']:
                    self.db['words'][word] = 1
                else:
                    self.db['words'][word] += 1

        self.db['analyzed_id'].append(a_tweet.id)

        return result


    def react(self, data):
        '''
        @param data: dict data returned by self.process() function
        '''
        tweet_react = TweetReact('./phrases/words_react.json')
        phrase = tweet_react.pick_random_phrase()
        return phrase


    def __str__(self):
        return 'WordsCounter'
