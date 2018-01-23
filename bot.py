#!/usr/bin/python3
'''
    This script should have the main Loop of the Bot. The 'Brain', if you dare.
'''
import argparse
import os
import tweepy #PIP
from time import sleep
from pprint import pprint

from auth import TweetAuth
from emotions import Emotions

from pdb import set_trace


def check_replied(tweet, user_name, t_id):
    #t_id = '955590160283926533'
    result = tweet.search(q='to:@%s' % user_name, since_id=t_id)
    for page in result:
        #if page.in_reply_to_user_id_str != t_id:
        #    continue
        if '@HiltronParish' in page.text:
            continue
        print(page.user.name)
        if page.user.name == 'Parish Hiltron':
            return True

    return False


def check_mentions(tweet, emo):
    print('Checking mentions...')
    try:
        for mentions in tweepy.Cursor(tweet.mentions_timeline).items():
            who_mentioned = mentions.text.split(' ')[0]
            msg = ''
            if 'how are you' in mentions.text.lower():
                is_replied = check_replied(tweet, 'HiltronParish', mentions.id_str)
                if is_replied:
                    continue;

                msg = emo.message
                gif_path = emo.gif_path
                #uploaded = tweet.media_upload(gif_path)
                #file_list = [uploaded.media_id]
                tweet.update_status(status=msg,
                                    in_reply_to_status_id=mentions.id_str)
                print('Mood message "%s" reply with gif "%s"' % (msg, gif_path))
    except tweepy.TweepError as err:
        print(err.reason)



def main(args):
    emo = Emotions('./gifs')
    '''
    try:
        while True:
            print(emo.state)
            print(emo.message)
            print(emo.gif_path)
            sleep(3)
    except KeyboardInterrupt:
        print('Stopping bot...')
        return

    return
    '''

    #twitter Authentication Voodoo
    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    if args['gif'] is not None:
        if not os.path.exists(args['gif']):
            print('Gif at %s is not found!' % (args['gif']))
        else:
            tweet.update_with_media(args['gif'])
        return

    if args['msg'] is not None:
        print('Prepparing to tweet a msg of size %s' % (len(args['msg'])))
        tweet.update_status(args['msg']) # Tweet a message!
        return

    if args['loop']:
        try:
            while True:
                check_mentions(tweet, emo)
                sleep(10)
        except KeyboardInterrupt:
            print('Stopping bot...')
            return

    check_mentions(tweet, emo)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--msg', default=None,
                        help='One time message to send.')
    parser.add_argument('--gif', default=None,
                        help='Path to a gif file to tweet.')
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    main(vars(args))
