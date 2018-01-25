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
from TweetBot import utils
# from TweetBot.commands.cmd_manager import CmdManager


class ParishHiltron:

    def __init__(self, args):
        self.args = args
        self.name = 'Parish Hiltron'
        self.emotions = Emotions('./gifs/')
        self.kewords_finder = KewordsFinder('./db/keywords.json')
        self.word_counter = WordCounter('./db/words.json')
        self.letter_counter = LetterCounter('./db/letters.json')


    def Update(self, tweet):
        user_tweets = utils.get_user_tweets(tweet, self.args['target'],
                                            maxTweetCount=self.args['tweet_limit'])
        prev_react_index = -1

        for target_tweet in user_tweets:
            print(' - Reading tweet %s: %s' % (target_tweet.id,
                                                target_tweet.full_text[:20]))

            kwords = self.kewords_finder.Update(a_tweet=target_tweet,
                                                dry_run=self.args['dry_run'])
            print(' - Keywords are: %s' % kwords)
            word_c = self.word_counter.Update(a_tweet=target_tweet,
                                                dry_run=self.args['dry_run'])
            print(' - Words are: %s' % word_c)
            letter_c = self.letter_counter.Update(a_tweet=target_tweet,
                                                dry_run=self.args['dry_run'])
            print(' - Letters are: %s' % letter_c)

            print(' ************************************* ')
            new_index = random.randint(0, 1)
            tries = 5
            while True:
                new_index = random.randint(0, 1)
                tries -= 1
                if tries <= 0:
                    break
                if new_index != prev_react_index:
                    break

            if new_index == 0:
                phrase = self.letter_counter.react(letter_c)
            else:
                phrase = self.kewords_finder.react(kwords)

            prev_react_index = new_index

            gif_path = self.emotions.pick_gif(phrase.category)
            print(' - Msg: %s\n- Gif: %s' % (phrase.text, gif_path))
            if self.args.get('dry_run', False) is False:
                self.reply(tweet, '@%s %s' % (self.args['target'], phrase.text),
                            gif_path, target_tweet.id)
            else:
                print(' - ! - Dry Run! No action!')


    def reply(self,tweet, text, gif_path, target_id):
        abs_gif_path = os.path.abspath(gif_path)
        if os.path.exists(abs_gif_path):
            tweet.update_with_media(abs_gif_path, status=text,
                                        in_reply_to_status_id=target_id)
        else:
            tweet.update_status(status=text, in_reply_to_status_id=target_id)


def main(args):
    #twitter Authentication Voodoo
    TheBot = ParishHiltron(args)

    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    if args['loop']:
        try:
            while True:
                TheBot.Update(tweet)
                sleep(45)
        except KeyboardInterrupt:
            print('Stopping bot...')
            return
    else:
        TheBot.Update(tweet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--msg', default=None,
                        help='One time message to send.')
    parser.add_argument('--gif', default=None,
                        help='Path to a gif file to tweet.')
    parser.add_argument('--loop', action='store_true')
    parser.add_argument('--target', default='LimerickDreams',
                        help='Twitter Username of whome to reply to.')
    parser.add_argument('--tweet-limit', '-l', default=10,
                        help='How many tweets to analyze at a time.')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    main(vars(args))