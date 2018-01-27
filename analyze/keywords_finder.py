#!/usr/bin/python3
import tweepy #PIP3
from collections import defaultdict
import random
from rake_nltk import Rake #PIP3

from TweetBot.tweet_react import TweetReact
from TweetBot.analyze.analyze import TweetAnalyzer
from TweetBot.utils import check_replied
from pdb import set_trace

class KewordsFinder(TweetAnalyzer):

    def __init__(self, db_path):
        super().__init__(db_path)
        self.rake = Rake()


    def Update(self, **kwargs):
        '''
        @param tweet: a tweet object. If nothing passed - not reply will be made.
        @param a_tweet: a tweet object that has not been handled yet
        '''
        # print('-------- EmoRetweet -------')
        data_set = super().Update(**kwargs) # { <tweet_id> : <key words list> }

        return data_set


    def process(self, a_tweet):
        '''
         Count words in the tweet and update self.db dict counters.

        @param a_tweet: tweet object (with full_text param) to analyze
        @return dict: <str>:<int> occurrence of words in the given tweet
        '''
        if a_tweet.id in self.db:
            print(' -- Keywords for %s already has been analyzed!' % a_tweet.id)
            return self.db[analyzed_id]

        #Parse tweet full text to extract key words from
        tweet_text = a_tweet.full_text
        self.rake.extract_keywords_from_text(tweet_text)
        key_words = self.rake.get_ranked_phrases()
        key_words = self.pick_a_word(key_words)
        self.db[a_tweet.id] = key_words

        return key_words


    def pick_a_word(self, words_list):
        candidates = []
        for phrase in words_list:
            word = phrase
            if len(word) < 4:
                continue
            if ' ' in phrase:
                words = phrase.split(' ')
                word = self.pick_a_word(words)
                if len(word) == 0:
                    continue
                if len(word) > 1:
                    word = word[random.randint(0, len(word) - 1)]
                else:
                    word = word[0]
            if len(word) > 4:
                candidates.append(word)

        return list(set(candidates))


    def pick_words(self, data, max=3):
        if len(data) <= max:
            return data

        result = []
        for i in range(max):
            if len(data) == 0: #paranoia
                break
            if len(data) == 1:
                result.append(data[0])
                break

            index = random.randint(0, len(data) - 1)
            result.append(data.pop(index))
        return result


    def react(self, data):
        if data is None:
            return ''

        tweet_react = TweetReact('./phrases/keywords.json')
        phrase = tweet_react.pick_random_phrase()

        keywords = self.pick_words(data)
        join_with = [', ', ' and ', 'and then ']
        pick_join = random.randint(0, len(join_with) - 1)
        join_symbol = join_with[pick_join]
        phrase.text = phrase.text.format(target=join_symbol.join(keywords))
        return phrase



    def __str__(self):
        return 'KeywordsFinder'