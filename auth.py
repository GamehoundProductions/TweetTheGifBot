#!/usr/bin/python3
'''
    Parse, store, manage twitter cridentials from the input file.
'''
import json
import os

from pdb import set_trace


class TweetAuth:


    def __init__(self, auth_file):
        self.credentials = self.read_credentials(auth_file)


    def read_credentials(self, auth_file):
        '''
            Read JSON file with Twitter cridentials in it:
        consumer_key, consumer_secret, access_token, access_token_secret.

        @param 'auth_file': path to a file (JSON format) with Twitter auth vars.
        @return: dict of string:string pair of Twitter auth variables.
        '''
        if not os.path.exists(auth_file):
            print('Auth file at %s not found!' % (auth_file))

        file_content = None
        with open(auth_file, 'r') as file_obj:
            file_content = file_obj.read()

        json_format = None
        try:
            json_format = json.loads(file_content)
        except ValueError:
            print('%s is not JSON format!' % (auth_file))

        return json_format


    @property
    def consumer_secret(self):
        return self.credentials['consumer_secret']

    @property
    def consumer_key(self):
        return self.credentials['consumer_key']

    @property
    def access_token(self):
        return self.credentials['access_token']

    @property
    def access_token_secret(self):
        return self.credentials['access_token_secret']
