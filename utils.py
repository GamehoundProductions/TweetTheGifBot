#!/usr/bin/python3
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