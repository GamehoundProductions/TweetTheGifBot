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
