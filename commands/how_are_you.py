#!/usr/bin/python3
import tweepy

from TweetBot.emotions import Emotions
from .cmd import Command

from pdb import set_trace

class HowAreYouCmd(Command):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.emo = Emotions('./gifs')


    def is_cmd_call(self, text):
        return self.cmd.lower() in text.lower()


    def process(self, tweet, mention, **kwargs):
        print('-------- HowAreYouCmd -------')
        is_help_called = super().process(tweet, mention, **kwargs)
        if not is_help_called:
            return False

        msg = self.emo.message
        gif_path = self.emo.gif_path
        if kwargs.get('dry_run', False) is False:
            uploaded = tweet.media_upload(gif_path)
            file_list = [uploaded.media_id]
            tweet.update_status(status=msg, media_ids=file_list,
                                in_reply_to_status_id=mention.id_str)
        else:
            print('Dry run for HowAreYouCmd process!')
        print('Mood message "%s" reply with gif "%s"' % (msg, gif_path))