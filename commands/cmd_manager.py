#!/usr/bin/python3
from TweetBot.routine import Routiner
from .help_cmd import HelpCmd
from .how_are_you import HowAreYouCmd

from pdb import set_trace

class CmdManager(Routiner):

    def __init__(self):
        super().__init__()
        how_r_u = HowAreYouCmd(cmd='how are you')
        self.all = {
            '--help' : HelpCmd(cmd='help', dsc='List of things I can understand.'),
            'How are you' : how_r_u
        }


    def Update(self, **kwargs):
        super().Update(**kwargs)
        print('CmdManager Update is called!')

        for name, cmd in self.all.items():
            if 'help' in name:
                cmd.process(kwargs.get('tweet', None), kwargs.get('mention', None),
                        all_cmd=list(self.all.keys()),
                        dry_run=kwargs.get('dry_run', False))
            else:
                cmd.process(kwargs.get('tweet', None), kwargs.get('mention', None),
                            dry_run=kwargs.get('dry_run', False))
