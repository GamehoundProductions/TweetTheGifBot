#!/usr/bin/python3
'''
    This script should have the main Loop of the Bot. The 'Brain', if you dare.
'''
import argparse
import json
import tweepy #PIP
from pprint import pprint

from auth import TweetAuth


def main(args):

    #twitter Authentication Voodoo
    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    if args['msg'] is not None:
        print('Prepparing to tweet a msg of size %s' % (len(args['msg'])))
        tweet.update_status(args['msg']) # Tweet a message!



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--msg', default=None,
                        help='One time message to send.')
    args = parser.parse_args()
    main(vars(args))
