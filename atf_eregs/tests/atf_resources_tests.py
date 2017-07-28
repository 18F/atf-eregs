import json
import re
from unittest.mock import call, Mock

import httpretty
import pytest
from regcore.layer import LayerParams

from atf_eregs import atf_resources


def test_load_config():
    """We shouldn't get an explosion when loading the ruling config."""
    results = atf_resources.load_config()
    assert results


@httpretty.activate
def test_doc_metadata():
    data = {'nodes': [
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
                  'URL': 'http://example.com/1111-44'}},
    ]}
    httpretty.register_uri(httpretty.GET, re.compile('.*'), json.dumps(data),
                           content_type='application/json')
    assert atf_resources.doc_metadata() == {
        '1111-22': atf_resources.ResourceMeta(
            'http://example.com/1111-22', '1111-22', 'A Title Here'),
        '1111-44': atf_resources.ResourceMeta(
            'http://example.com/1111-44', '1111-44', 'Last Ruling'),
    }


def test_create_layer():
    config = {'2222-33': ['123-45', '123-46'],
              '1111-22': ['123-47', '123-48-h']}
    meta = {'1111-22': atf_resources.ResourceMeta(
                'http://example.com/1111-22', '1111-22', 'A Title Here'),
            '1111-44': atf_resources.ResourceMeta(
                'http://example.com/1111-44', '1111-44', 'Last Ruling')}
    results = atf_resources.create_layer(config, meta, '123')
    assert {'123-47', '123-48-h'} == results.keys()
    for data in results.values():
        assert data == {'1111-22': {
            'url': 'http://example.com/1111-22', 'id': '1111-22',
            'title': 'A Title Here'
        }}


@pytest.mark.django_db
def test_fetch_and_save_resources(monkeypatch):
    """Verify that the correct calls are being made to the storage backend."""
    monkeypatch.setattr(atf_resources, 'storage', Mock())
    monkeypatch.setattr(atf_resources, 'load_config', Mock())
    monkeypatch.setattr(atf_resources, 'doc_metadata', Mock())
    monkeypatch.setattr(atf_resources, 'create_layer', Mock())
    monkeypatch.setattr(atf_resources, 'child_layers', Mock())
    storage = atf_resources.storage
    storage.for_documents.listing.return_value = [
        ('v1', 'cfrpart1'), ('v2', 'cfrpart1'), ('va', 'cfrpart2'),
    ]

    atf_resources.fetch_and_save_resources()

    assert storage.for_documents.listing.call_args == call('cfr')
    assert storage.for_layers.bulk_delete.call_args_list == [
        call('atf-resources', 'cfr', 'v1/cfrpart1'),
        call('atf-resources', 'cfr', 'v2/cfrpart1'),
        call('atf-resources', 'cfr', 'va/cfrpart2'),
    ]
    assert atf_resources.child_layers.call_args_list == [
        call(LayerParams('cfr', 'v1/cfrpart1', 'cfrpart1'),
             atf_resources.create_layer.return_value),
        call(LayerParams('cfr', 'v2/cfrpart1', 'cfrpart1'),
             atf_resources.create_layer.return_value),
        call(LayerParams('cfr', 'va/cfrpart2', 'cfrpart2'),
             atf_resources.create_layer.return_value),
    ]
    assert storage.for_layers.bulk_insert.call_args_list == [
        call(atf_resources.child_layers.return_value, 'atf-resources', 'cfr')
    ]*3
