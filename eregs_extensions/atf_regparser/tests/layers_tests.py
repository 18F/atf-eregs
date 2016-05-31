from unittest import TestCase

from mock import patch
import six

from atf_regparser import layers
from regparser.test_utils.http_mixin import HttpMixin


class RulingsTests(HttpMixin, TestCase):
    def test_load_config(self):
        """We shouldn't get an explosion when loading the ruling config"""
        results = layers.Rulings.load_config()
        self.assertTrue(bool(results))

    def _expect_common_json(self):
        """Common JSON to mock atf.gov"""
        self.expect_json_http({'nodes': [
            {'node': {'Title': '1111-22 - A Title Here',
                      'Document Type': 'Ruling',
                      'URL': 'http://example.com/1111-22'}},
            {'node': {'Title': 'Bad Title',
                      'Document Type': 'Ruling',
                      'URL': 'http://example.com/bad'}},
            {'node': {'Title': '1111-33 - Not a Ruling',
                      'Document Type': 'Open Letter',
                      'URL': 'http://example.com/open'}},
            {'node': {'Title': '1111-44 - Last Ruling',
                      'Document Type': 'Ruling',
                      'URL': 'http://example.com/1111-44'}}]})

    def test_doc_metadata(self):
        """Given some expected output, derive the correct metadata"""
        self._expect_common_json()
        self.assertEqual(layers.Rulings.doc_metadata(), {
            '1111-22': {'url': 'http://example.com/1111-22', 'id': '1111-22',
                        'title': 'A Title Here'},
            '1111-44': {'url': 'http://example.com/1111-44', 'id': '1111-44',
                        'title': 'Last Ruling'}})

    @patch.object(layers.Rulings, 'load_config')
    def test_pre_process(self, load_config):
        """Verify that mappings are correct"""
        load_config.return_value = {
            '2222-33': ['123-45', '123-46'],
            '1111-22': ['123-47', '123-48-h']}
        self._expect_common_json()

        rulings = layers.Rulings(None)
        rulings.pre_process()
        six.assertCountEqual(self, ['123-47', '123-48-h'],
                             rulings.label_to_rulings.keys())
        for label_id in ('123-47', '123-48-h'):
            self.assertEqual(rulings.label_to_rulings[label_id], {
                '1111-22': {'url': 'http://example.com/1111-22',
                            'id': '1111-22', 'title': 'A Title Here'}})
