#!/usr/bin/python3
'''
    Keep track of the last N responses made by the bot, such as: gifs, reaction
types and reaction comment names.
'''
import json
from pdb import set_trace

from TweetBot import utils


class BotHistory:

    def __init__(self, db_path, limit=10):
        '''
        @param db_path: path to a json file to save/load history data from.
        @param limit: default=10. How many records to keep track of.
        '''
        if not utils.validate_dir(db_path):
            raise RuntimeError('%s is not a valid path in %s! '\
                     ' One of the directories does not exist!' %\
                        (self.__class__.name, db_path))
        self.limit = limit
        self.db_path = db_path
        self.json_data = utils.read_db(db_path)


    def check_gif_dub(self, gif_path, limit=None):
        '''
        @param gif_path: Gif path saved in the history.
        @param limit: default=None. how many of last records to check.
                        None means - check all of them.
        @return: bool. True if gif_path already has been used in the past range.
        '''
        if limit is None:
            limit = self.limit

        latest_records = []
        for record in self.gifs[:limit]:
            if len(record) > 0:
                latest_records.append(record)
        return gif_path in latest_records


    def check_react_dub(self, react_name, limit=None):
        '''
        @param react_name: Name of the reaction type to check for dubs.
        @param limit: default=None. how many of last records to check.
                        None means - check all of them.
        @return: bool. True if react_name already has been used in the past range.
        '''
        if limit is None:
            limit = self.limit

        latest_records = []
        for record in self.reactions[:limit]:
            if len(record) > 0:
                latest_records.append(record)
        return react_name in latest_records


    def check_comment_dub(self, comment_name, dub_size=1, limit=None):
        '''
        @param comment_name: Name of the comment type to check for dubs.
        @param limit: default=None. how many of last records to check.
                        None means - check all of them.
        @return: bool. True if react_name already has been used in the past range.
        '''
        if limit is None:
            limit = self.limit
        '''
        latest_records = []
        for record in self.comments[:limit]:
            if len(record) > 0:
                latest_records.append(record)
        '''
        num_of_records = self.count_occurance(comment_name, limit)
        return num_of_records >= dub_size
        # return comment_name in latest_records


    def count_occurance(self, comment_name, limit=None):
        '''
        @param comment_name: Name of the comment type to check for dubs.
        @param limit: default=None. how many of last records to check.
                        None means - check all of them.
        '''
        if limit is None:
            limit = self.limit

        latest_records = []
        for record in self.reactions[:limit]:
            if len(record) == 0:
                continue
            if comment_name.lower() == record.lower():
                latest_records.append(record)
        return len(latest_records)


    def save(self, **kwargs):
        '''
        @param tweet_id:
        @param gif_path:
        @param react_text:
        @param react_type:
        '''
        if kwargs.get('dry_run', False) is True:
            from pprint import pprint
            print(' -- Dry Run ON for %s.%s' % (__class__.__name__, 'save()'))
            print(' -- args list ---')
            pprint(kwargs)
            print(' ---- -----')
            return

        self.append(kwargs)
        data_str = json.dumps(self.json_data, indent=4)
        utils.write_to_file(self.db_path, data_str)


    def delete(self, key, value):
        to_delete = []

        for entry in self.history:
            if not key in entry:
                continue
            is_delete = False
            if isinstance(entry[key], list):
                is_delete = True if value in entry[key] else False
            else:
                is_delete = True if value == entry[key] else False

            if is_delete:
                print('delete <%s> : <%s>' % (key, value))
                to_delete.append(entry)

        for obj in to_delete:
            self.history.remove(obj)

        data_str = json.dumps(self.json_data)
        utils.write_to_file(self.db_path, data_str)


    def append(self, entry):
        print(' - appending entry to history- ')
        print(entry)
        print(' ---- --- ')
        entries = self.history
        if len(entries) >= self.limit:
            entries = entries[0:self.limit]
            entries.pop(0)
        if self.json_data.get('queue', None) is None:
            self.json_data['queue'] = []

        self.json_data['queue'].append(entry)


    def get_list(self, key):
        result = []
        for entry in self.history:
            result.extend(entry.get(key, []))
        return result


    @property
    def history(self):
        '''
            List (queue) of latest entries.
            [
                {}
            ]
        '''
        return self.json_data.get('queue', [{}])


    @property
    def latest_tweets(self):
        ''' Return list of latest tweet_id posted by the bot. '''
        tweet_ids = []
        for record in self.comments:
            if len(record) == 0:
                tweet_ids.append(record[0])
        return tweet_ids


    @property
    def gifs(self):
        gif_path_list = []
        for entry in self.history:
            path = entry.get('gif_path', '')
            gif_path_list.append(path)
        return gif_path_list


    @property
    def reactions(self):
        reactions = []
        for entry in self.history:
            reaction_type = entry.get('react_type', '')
            reactions.append(reaction_type)
        return reactions


    @property
    def comments(self):
        comments = []
        for entry in self.history:
            react_text = entry.get('react_text', '')
            comments.append(react_text)
        return comments
