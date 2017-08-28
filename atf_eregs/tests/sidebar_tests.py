from mock import Mock

from atf_eregs.sidebar import ATFResources


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
