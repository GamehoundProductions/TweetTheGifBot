#!/usr/bin/python3
from collections import defaultdict
import random
from pdb import set_trace
from pprint import pprint

from TweetBot.analyze.analyze import TweetAnalyzer
from TweetBot.tweet_react import TweetReact


class LetterCounter(TweetAnalyzer):

    def __init__(self, db_path, repeat_limit=1):
        super().__init__(db_path, repeat_limit=repeat_limit)


    def Update(self, **kwargs):
        # print('-------- LetterCounter -------')
        return super().Update(**kwargs)


    def read_db(self, path):
        db = super().read_db(path)
        if db: # DB is not empty and constructed
            return db

        db['analyzed_id'] = []
        db['letters'] = defaultdict(int)
        return db


    def process(self, a_tweet):
        '''
         Count words in the tweet and update self.db dict counters.

        @param a_tweet: tweet object (with full_text param) to analyze
        @return dict: <str>:<int> occurrence of words in the given tweet
        '''
        has_analyzed = False
        if a_tweet.id in self.db['analyzed_id']:
            print(' -- Letters for %s already has been analyzed!' % a_tweet.id)
            has_analyzed = True

        result = defaultdict(int)

        for line in a_tweet.full_text.split('\n'):
            for letter in line:
                if letter == ' ':
                    continue
                result[letter] += 1
                if has_analyzed: #Dont write to DB since already been analyzed before
                    continue

                if letter not in self.db['letters']:
                    self.db['letters'][letter] = 1
                else:
                    self.db['letters'][letter] += 1

        self.db['analyzed_id'].append(a_tweet.id)

        return result


    def most_used_letter(self, data):
        '''
        @param data: dict data returned by self.process() function
        '''
        result = ['-', -1]
        for name, count in data.items():
            if count > result[1]:
                result[0] = name
                result[1] = count
        return result


    def random_used_letter(self, data):
        '''
        @param data: dict data returned by self.process() function
        '''
        letters = list(data.keys())
        pick_one = random.randint(0, len(letters) - 1 )
        pick_one = letters[pick_one]
        result = [pick_one, data[pick_one]]
        return result


    def react(self, data):
        '''
        @param data: dict data returned by self.process() function
        '''
        tweet_react = TweetReact('./phrases/stats.json')
        phrase = tweet_react.pick_random_phrase()

        if random.randint(0, 1) == 0:
            most_used = self.most_used_letter(data)
        else:
            most_used = self.random_used_letter(data)

        phrase.text = phrase.text.format(target=most_used[0], count=most_used[1])
        return phrase


    def __str__(self):
        return 'LetterCounter'
