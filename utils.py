#!/usr/bin/python3
import os
import json
import tweepy #PIP


def check_replied(tweet, user_name, t_id):
    result = tweet.search(q='to:@%s' % user_name, since_id=t_id)

    for page in result:
        if '@HiltronParish' in page.text:
            continue
        if page.user.name == 'Parish Hiltron':
            return True
    return False


def get_user_tweets(tweet, target_user, **kwargs):
        '''
        @param whoIsReplying: username of the one who is replying to a target_user.
                              Default is 'HiltronParish'
        @param maxTweetCount: max amount of latest tweets to extract. Default = 10
        '''
        whoIsReplying = kwargs.get('whoIsReplying', 'HiltronParish')
        maxTweets = kwargs.get('maxTweetCount', 10)

        result = tweet.user_timeline(screen_name = target_user,
                                            count = maxTweets,
                                            tweet_mode="extended")
        non_replied_tweets = []
        for a_tweet in result:
            try:
                has_replied = check_replied(tweet, whoIsReplying, a_tweet.id)
                if has_replied:
                    continue

                #new non replied tweet found. Save it into the list to return
                non_replied_tweets.append(a_tweet)
            except tweepy.TweepError as err:
                print('Error found while getting "%s" tweets by "%s": %s' %\
                        (target_user, whoIsReplying, err))
                continue

        return non_replied_tweets


def validate_dir(path):
    dir = os.path.split(path)[0]
    return os.path.exists(dir)


def read_db(path, verbose=True):
    db = None
    file_content = None
    if verbose:
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


def write_to_file(path, data, verbose=True):
    '''
    @param path: destination to a file to write to.
    @param data: text to write to file
    '''
    if verbose:
        if not os.path.exists(path):
            print(' -- Creating a new file at %s' % path)

    with open(path, 'w+') as file_obj:
        file_obj.write(data)