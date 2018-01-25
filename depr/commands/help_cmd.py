#!/usr/bin/python3
import tweepy

from .cmd import Command

class HelpCmd(Command):

    def process(self, tweet, mention, **kwargs):
        print('-------- HelpCmd -------')
        is_help_called = super().process(tweet, mention, **kwargs)
        if not is_help_called:
            return False

        if kwargs.get('all_cmd', None) is None:
            print('Cant process Help! Missing all_cmd in kwargs list!')
            return False
        msg = 'Available Cmds:\n'
        msg += '\n'.join(kwargs['all_cmd'])
        print('Help Message Response:\n[%s]' % (msg))
        try:
            if kwargs.get('dry_run', False) is True:
                print('Dry run! Doing nothing for Help process!')
                return True

            tweet.update_status(status=msg, in_reply_to_status_id=mention.id_str)
        except tweepy.TweepError as err:
            print('Failed to process "--help" request! Reason: %s' % err)
            return False
        return True

