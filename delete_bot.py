#!/usr/bin/python3
import argparse
import tweepy #PIP3
from pdb import set_trace

from auth import TweetAuth
from TweetBot.history import BotHistory
from TweetBot import utils


def wait_for_user():
    confirm_delete = input('Press Y/N to continue...\n')
    if confirm_delete.lower() == 'y':
        return True
    else:
        return False


def delete(tweet_api, a_tweet, dry_run=False):
    try:
        print(' - Are you sure you want to delete: %s' % a_tweet.id)
        print('  - [%s]' % a_tweet.text[:20])
        is_delete = wait_for_user()
        if is_delete and dry_run is False:
            print(' - Deleting %s' % a_tweet.id)
            tweet_api.destroy_status(a_tweet.id)
        if dry_run is True:
            print(' -- Dry Run is ON')
            return False
        return True
    except:
        print("Failed to delete: %s" % a_tweet.id)
        return False


def history_delete(tweet, dry_run=False):
    reply_history = BotHistory('./db/reply_history.json')
    history = BotHistory('./db/history.json')
    for entry in reply_history.history:
        origin = entry['entry'][0]
        reply = entry['entry'][1]
        a_tweet = tweet.get_status(id=reply)

        has_deleted = delete(tweet, a_tweet, dry_run)
        has_deleted = True
        if has_deleted:
            reply_history.delete('entry', reply)
            history.delete('tweet_id', reply)


def main(args):
    usr_auth = TweetAuth(args['auth'])
    tweeter_auth = tweepy.OAuthHandler(usr_auth.consumer_key,
                                        usr_auth.consumer_secret)
    tweeter_auth.set_access_token(usr_auth.access_token, usr_auth.access_token_secret)
    tweet = tweepy.API(tweeter_auth)

    if args['history']:
        history_delete(tweet, args['dry_run'])
        return

    user_tweets = utils.get_user_tweets(tweet, args['target'],
                                        maxTweetCount=args['tweet_limit'])

    for a_tweet in user_tweets:
        delete(tweet, a_tweet, dry_run=args['dry_run'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', '-a',
                        help='Path to JSON file with Tweeter credentials')
    parser.add_argument('--target', default='HiltronParish',
                        help='Twitter Username of whome to reply to.')
    parser.add_argument('--tweet-limit', '-l', default=1,
                        help='How many tweets to analyze at a time.')
    parser.add_argument('--history', action='store_true')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    main(vars(args))
