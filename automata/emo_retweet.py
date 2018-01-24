#!/usr/bin/python3
import tweepy #PIP3
from rake_nltk import Rake #PIP3

from TweetBot.routine import Routiner
from TweetBot.utils import check_replied
from pdb import set_trace

class EmoRetweet(Routiner):

    def __init__(self):
        super().__init__()
        self.rake = Rake()


    def Update(self, **kwargs):
        print('-------- EmoRetweet -------')
        super().Update(**kwargs)
        # result = kwargs['tweet'].search(q='to:@LimerickDreams',
                                        # count=5, tweet_mode='extended')
        #LimerickDreams
        tweet = kwargs['tweet']
        result = tweet.user_timeline(screen_name = 'HiltronParish',
                                                count = 1, tweet_mode="extended")

        for a_tweet in result:
            try:
                has_replied = check_replied(tweet, 'HiltronParish', a_tweet.id)
                if has_replied:
                    continue

                tweet_text = result[0].full_text
                self.rake.extract_keywords_from_text(tweet_text)
                key_words = self.rake.get_ranked_phrases()

                key_words = self.pick_a_word(key_words)
                msg = 'Key words are: %s' % (', '.join(key_words))
                if kwargs.get('dry_run', False) is False:
                    tweet.update_status(status=msg,
                                    in_reply_to_status_id=a_tweet.id)
                else:
                    print('Dry run for EmoRetweet with the message "%s"!' % msg)

            except tweepy.TweepError as err:
                continue




    def pick_a_word(self, words_list):
        candidates = []
        for phrase in words_list:
            word = phrase
            if ' ' in phrase:
                words = phrase.split(' ')
                word = self.pick_a_word(words)
            if len(word) > 4 and len(word) < 10:
                candidates.append(word)

        return candidates
