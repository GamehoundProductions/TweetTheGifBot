#!/usr/bin/python3
'''
    This script should have the main Loop of the Bot. The 'Brain', if you dare.
'''
import argparse
import os
import tweepy #PIP
import random
from time import sleep
from pprint import pprint

from pdb import set_trace

from auth import TweetAuth
from TweetBot.analyze.keywords_finder import KewordsFinder
from TweetBot.analyze.count_words import WordCounter
from TweetBot.analyze.count_letters import LetterCounter
from TweetBot.emotions import Emotions
from TweetBot.history import BotHistory
from TweetBot import utils


class ParishHiltron:

    def __init__(self, args):
        self.args = args
        self.name = args.get('username', 'HiltronParish')
        self.emotions = Emotions('./gifs/')
        self.history = BotHistory('./db/history.json')
        # history of tweet ids this bot replied to
        self.reply_history = BotHistory('./db/reply_history.json', 10000)

        self.reactions = {
            'keywords' : KewordsFinder('./db/keywords.json'),
            'word_counter' : WordCounter('./db/words.json'),
            'letter_counter' : LetterCounter('./db/letters.json')
        }
        self.prev_reaction = None #saves prev reaction during this run


    def choose_react_type(self, reactions=None, max_tries=5):
        '''
            Randomly choose one of the reaction type from the list, but make
        sure to not repeat a type two times in a row.
        @param reactions: self.reactions. A dict of all TweetAnalyzer obj
        @param max_tries: default=5; How many times it will try to pick a tweet
                        when Random number keep gettin an "already used" index.
                        Eventually it will pick any to break out of the loop.
        @return: <TweetAnalyzer> object (in other others - a reaction object/type)
        '''
        if reactions is None:
            reactions = self.reactions

        react_types = list(reactions.keys())
        react_amount = len(react_types)
        tries = max_tries
        while True:
            new_index = random.randint(0, react_amount - 1)
            tries -= 1
            new_reaction = react_types[new_index]
            if tries <= 0: # done picking a reaction.
                break      # Whatever is picked now - go for it.
            if new_reaction != self.prev_reaction:
                break

        self.prev_reaction = new_reaction
        return new_reaction


    def process(self, tweet, reactions=None):
        '''
            Process (analyze) all of the reaction types.
        @param tweet: a single tweet object (the one with .full_text), not an
                      actual tweepy api one.
        @param reactions: self.reactions. A dict of all TweetAnalyzer obj.
        '''
        if reactions is None:
            reactions = self.reactions

        for react_name, react_obj in reactions.items():
            react_obj.Update(a_tweet=tweet, dry_run=self.args['dry_run'])


    def Update(self, tweet):
        '''
            Find args['target'] user's latest tweets, analyze them and post a
        reaction response.

        @param tweet: tweepy API object
        '''
        user_tweets = utils.get_user_tweets(tweet, self.args['target'],
                                            maxTweetCount=self.args['tweet_limit'])

        for target_tweet in user_tweets:
            tweet_text_sample = target_tweet.full_text[:20]
            replied_ids = self.reply_history.get_list('entry')
            if target_tweet.id in replied_ids:
                print(' - Already replied to %s [%s]' %\
                    (target_tweet.id, tweet_text_sample))
                continue

            has_replied = utils.check_replied(tweet, self.name, target_tweet.id)
            if has_replied:
                print(' - ! - %s already replied to %s (%s)!' % \
                        (self.name,target_tweet.id, tweet_text_sample))
                continue

            print(' - Reading tweet %s: %s' % (target_tweet.id, tweet_text_sample))
            self.process(target_tweet)

            reaction_type = self.choose_react_type()
            reaction = self.reactions[reaction_type]
            processed_data = {}
            if reaction is not None:
                processed_data = reaction.last_data
                reaction = reaction.react(processed_data)
            else:
                print(' - ! - reaction is None for tweet: %s ?!' % tweet_text_sample)
                continue

            reply_text = '@%s %s' % (self.args['target'], reaction.text)
            gif_path = self.emotions.pick_gif(reaction.category)
            response = self.reply(tweet, reply_text, gif_path, target_tweet.id,
                        dry_run=self.args['dry_run'])

            if response is None:
                continue

            self.history.save(
                tweet_id=response.id,
                gif_path=gif_path,
                react_text=reply_text,
                react_type=reaction_type,
                dry_run=self.args['dry_run']
            )

            self.reply_history.save(entry=[target_tweet.id, response.id])


    def reply(self, tweet, text, gif_path, target_id, dry_run=False):
        '''
        @return: tweet response object (with id, text and etc)
        '''
        if dry_run is True:
            print(' -- Dry Run to reply is ON: %s' % text)
            return

        response = None
        if gif_path and os.path.isfile(gif_path):
            abs_gif_path = os.path.abspath(gif_path)
            if os.path.exists(abs_gif_path):
                response = tweet.update_with_media(abs_gif_path, status=text,
                                            in_reply_to_status_id=target_id)
        else:
            response = tweet.update_status(status=text, in_reply_to_status_id=target_id)

        return response


    def delete(self, tweet_id_list):
        '''
            Delete all of the tweets in the tweet_id_list.
        '''
        print(' - preparing to delete tweets.')
        pass



def main(args):
    #twitter Authentication Voodoo
    TheBot = ParishHiltron(args)

    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    TheBot.Update(tweet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--target', default='LimerickDreams',
                        help='Twitter Username of whome to reply to.')
    parser.add_argument('--tweet-limit', '-l', default=10,
                        help='How many tweets to analyze at a time.')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    main(vars(args))
