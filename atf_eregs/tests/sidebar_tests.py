from unittest import TestCase

from mock import Mock

from atf_eregs.sidebar import Rulings


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
