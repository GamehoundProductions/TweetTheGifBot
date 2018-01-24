#!/usr/bin/python3
'''
    This script should have the main Loop of the Bot. The 'Brain', if you dare.
'''
import argparse
import os
import tweepy #PIP
from time import sleep
from pprint import pprint

from pdb import set_trace

from auth import TweetAuth
from TweetBot.commands.cmd_manager import CmdManager
from TweetBot.automata.emo_retweet import EmoRetweet



def check_replied(tweet, user_name, t_id):
    result = tweet.search(q='to:@%s' % user_name, since_id=t_id)

    for page in result:
        if '@HiltronParish' in page.text:
            continue
        if page.user.name == 'Parish Hiltron':
            return True
    return False


def check_mentions(tweet, cmd_manager, **kwargs):
    print('Checking mentions...')
    try:
        for mentions in tweepy.Cursor(tweet.mentions_timeline).items():
            who_mentioned = mentions.text.split(' ')[0]
            msg = ''
            print(mentions.user.screen_name)
            print('Mention: [%s]' % mentions.text)
            # if 'how are you' in mentions.text.lower():
            is_replied = check_replied(tweet, who_mentioned, mentions.id_str)
            print('Status "has replied" to %s : %s' % (who_mentioned, is_replied))
            if is_replied:
                continue;

            cmd_manager.Update(tweet=tweet, mention=mentions, t_id=mentions.id_str, dry_run=kwargs.get('dry_run', False))

    except tweepy.TweepError as err:
        print(err.reason)



def main(args):
    cmd_manager = CmdManager()
    emo_retweet = EmoRetweet()

    #twitter Authentication Voodoo
    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    emo_retweet.Update(tweet=tweet, dry_run=args['dry_run'])

    return
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
                check_mentions(tweet, cmd_manager, dry_run=args['dry_run'])
                sleep(45)
        except KeyboardInterrupt:
            print('Stopping bot...')
            return

    check_mentions(tweet, cmd_manager, dry_run=args['dry_run'])
    # check_mentions(tweet, emo)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--msg', default=None,
                        help='One time message to send.')
    parser.add_argument('--gif', default=None,
                        help='Path to a gif file to tweet.')
    parser.add_argument('--loop', action='store_true')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    main(vars(args))
