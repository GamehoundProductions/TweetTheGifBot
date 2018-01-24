#!/usr/bin/python3


class Command:

    def __init__(self, **kwargs):
        '''
        "dsc" : description of the command
        "cmd" : command call, e.g. cmd="--help|--list"
        '''
        self.dsc = kwargs.get('dsc', '')
        self.cmd = kwargs.get('cmd', None)


    def is_cmd_call(self, text):
        if text.startswith('@'):
            trim_mention = text.split(' ')[1:] # @name text here -> ['text', 'here']
            text = ' '.join(trim_mention)
        return text.startswith('--')


    def process(self, tweet, mention, **kwargs):
        '''
        @param tweet: tweepy object, which is an open (authed) tweet connection.
        @param t_id: tweet id to reply to.
        '''
        if mention is None:
            return False
        return self.is_cmd_call(mention.text)