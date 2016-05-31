from collections import defaultdict
import logging
import os
import re

import requests
import yaml

from regparser.layer.layer import Layer


JSON_URL = 'https://www.atf.gov/rules-and-regulations/json'


class Rulings(Layer):
    """ATF has associated "ruling" documents, which we'd like to tag to
    particular paragraphs. To do that we need to
    1) read a config yaml file which maps rulings to regulation paragraphs
    2) read a listing of rulings from atf.gov's API
    3) connect the two
    """
    # Naming format from www.atf.gov
    SPLIT_RE = re.compile(r'(?P<id>[0-9-]+) - (?P<title>.*)')
    shorthand = 'atf-rulings'

    @staticmethod
    def load_config():
        """The config file lives in the code repository; we must find it and
        parse it"""
        this_file = os.path.abspath(__file__)
        package_dir = os.path.dirname(this_file)
        data_path = os.path.join(package_dir, 'rulings.yml')
        with open(data_path, 'r') as f:
            return yaml.load(f)

    @classmethod
    def doc_metadata(cls):
        """Convert results from www.atf.gov into a dict, associating ruling
        ids with meta data about that ruling"""
        listing = requests.get(JSON_URL).json()
        listing = [n.get('node', {}) for n in listing.get('nodes', [])]
        listing = [n for n in listing if n.get('Document Type') == 'Ruling']
        docs = {}
        for meta in listing:
            match = cls.SPLIT_RE.match(meta.get('Title', ''))
            if not match:
                logging.warning('Could not parse ruling title: %s',
                                meta.get('Title', ''))
            else:
                ident = match.group('id')
                docs[ident] = {'url': meta.get('URL', ''),
                               'id': ident,
                               'title': match.group('title')}
        if not docs:
            logging.warning('No results from www.atf.gov. Format changed?')
        return docs

    def pre_process(self):
        """Sets self.label_to_rulings to be of the form:
            {label_id: {ruling_id: {...ruling meta data...}}}.
           We only need to do this once"""
        config = self.load_config()
        meta = self.doc_metadata()
        matched = [(ruling, label_id)
                   for ruling, labels in config.items()
                   for label_id in labels
                   if ruling in meta]
        self.label_to_rulings = defaultdict(dict)    # nested dictionaries
        for ruling, label_id in matched:
            self.label_to_rulings[label_id][ruling] = meta[ruling]

    def process(self, node):
        return self.label_to_rulings.get(node.label_id())
