from unittest import TestCase

from mock import Mock

from atf_eregs.sidebar import ATFResources, Rulings


class RulingsTest(TestCase):
    def test_returns_children(self):
        """We should be catching rulings related to this section _or any
        subparagraph_. Also verified order"""
        http_client = Mock()
        http_client.layer.return_value = {
            "200-2": {"111-11": {"id": 1}},
            "200-20-a": {"222-22": {"id": 2}, "333-33": {"id": 3}},
            "200-20-g": {"444-44": {"id": 4}}
        }

        results = Rulings("200-2", "version").context(http_client, None)
        self.assertEqual(results, {"rulings": [{"id": 1}]})

        results = Rulings("200-20", "version").context(http_client, None)
        self.assertEqual(results,
                         {"rulings": [{"id": 4}, {"id": 3}, {"id": 2}]})

        results = Rulings("200-20-g", "version").context(http_client, None)
        self.assertEqual(results, {"rulings": [{"id": 4}]})

    def test_combines_duplicates(self):
        """If the same ruling is used by multiple children, include it only
        once"""
        http_client = Mock()
        http_client.layer.return_value = {
            "200-2": {"111-11": {"id": 1}},
            "200-2-a": {"222-22": {"id": 2}, "333-33": {"id": 3}},
            "200-2-g": {"222-22": {"id": 2}, "111-11": {"id": 1}}
        }

        results = Rulings("200-2", "version").context(http_client, None)
        self.assertEqual(results,
                         {"rulings": [{"id": 3}, {"id": 2}, {"id": 1}]})


def test_atf_resources():
    """Integration test to verify that data gets transformed correctly."""
    # We'll use numbers as placeholders for entity content
    http_client = Mock()
    http_client.layer.return_value = {
        '111-22': {'Ruling': [1, 2, 3], 'FAQ': [4, 5], 'Other Thing': [6]},
        '111-22-c': {'FAQ': [7, 8], 'Another': [9, 10, 11]},
        '111-33': {'Ruling': [12]},
    }
    resources = ATFResources('111-22', 'vvvv')

    context = resources.context(http_client, request=Mock())

    assert context == {
        'count': 3 + 2 + 1 + 2 + 3,
        'groups': [
            {'name': 'Ruling', 'count': 3, 'entries': [1, 2, 3]},
            {'name': 'FAQ', 'count': 2 + 2, 'entries': [4, 5, 7, 8]},
            {'name': 'Another', 'count': 3, 'entries': [9, 10, 11]},
            {'name': 'Other Thing', 'count': 1, 'entries': [6]},
        ]
    }


def test_atf_resources_empty():
    """We need to account for empty data."""
    http_client = Mock()
    http_client.layer.return_value = None
    resources = ATFResources('111-22', 'vvvv')

    context = resources.context(http_client, request=Mock())

    assert context == {'count': 0, 'groups': []}
