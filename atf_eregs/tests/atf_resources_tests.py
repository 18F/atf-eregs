from datetime import date
import json
import pathlib
from unittest.mock import call, Mock

import httpretty
import pytest
from regcore.layer import LayerParams

from atf_eregs import atf_resources


@pytest.mark.parametrize('mapping, expected', [
    (atf_resources.Mapping('123', '456'), '123-456'),
    (atf_resources.Mapping('123', '456', ''), '123-456'),
    (atf_resources.Mapping('1', '2', '(a)'), '1-2-a'),
    (atf_resources.Mapping('222', '33', '(z)(2)(A)(ii)'), '222-33-z-2-A-ii'),
])
def test_mapping_label(mapping, expected):
    assert mapping.label() == expected


def test_create_layer():
    """Layer should be keyed by label and correctly sorted."""
    data = [
        atf_resources.ResourceData(
            short_title='First', group='Ruling', identifier='111-22',
            published='2001-01-01', url='http://example.com/111-22',
            mappings=[atf_resources.Mapping('123', '45'),
                      atf_resources.Mapping('123', '48'),
                      atf_resources.Mapping('123', '51', '(h)'),
                      atf_resources.Mapping('other-part', 'xx')]),
        atf_resources.ResourceData(
            short_title='Second', group='Form', published='2001-01-01',
            url='http://example.com/Form',
            mappings=[atf_resources.Mapping('123', '48')]),
        atf_resources.ResourceData(
            short_title='Third', group='Ruling', identifier='111-11',
            published='2002-02-02', url='http://example.com/111-11',
            mappings=[atf_resources.Mapping('123', '48')]),
    ]
    resource1 = atf_resources.Entry(
        'First', 'http://example.com/111-22', '111-22')._asdict()
    resource2 = atf_resources.Entry(
        'Second', 'http://example.com/Form')._asdict()
    resource3 = atf_resources.Entry(
        'Third', 'http://example.com/111-11', '111-11')._asdict()

    assert atf_resources.create_layer('123', data) == {
        '123-45': {'Ruling': [resource1]},
        '123-48': {'Ruling': [resource3, resource1], 'Form': [resource2]},
        '123-51-h': {'Ruling': [resource1]},
    }


@pytest.mark.django_db
def test_save_layer(monkeypatch):
    monkeypatch.setattr(atf_resources, 'storage', Mock())
    monkeypatch.setattr(atf_resources, 'child_layers', Mock())

    atf_resources.save_layer('partpart', {'some': 'data'}, 'verver')

    assert atf_resources.storage.for_layers.bulk_delete.call_args == call(
        'atf-resources', 'cfr', 'verver/partpart')
    assert atf_resources.child_layers.call_args == call(
        LayerParams('cfr', 'verver/partpart', 'partpart'), {'some': 'data'})
    assert atf_resources.storage.for_layers.bulk_insert.call_args == call(
        atf_resources.child_layers.return_value, 'atf-resources', 'cfr')


def test_fetch_and_save_resources(monkeypatch):
    """Verify that the correct calls are being made to the storage backend."""
    monkeypatch.setattr(atf_resources, 'storage', Mock())
    monkeypatch.setattr(atf_resources, 'fetch_resource_data', Mock())
    monkeypatch.setattr(atf_resources, 'create_layer', Mock())
    monkeypatch.setattr(atf_resources, 'save_layer', Mock())
    atf_resources.storage.for_documents.listing.return_value = [
        ('v1', 'cfrpart1'), ('v2', 'cfrpart1'), ('va', 'cfrpart2'),
    ]

    atf_resources.fetch_and_save_resources()

    assert atf_resources.save_layer.call_args_list == [
        call('cfrpart1', atf_resources.create_layer.return_value, 'v1'),
        call('cfrpart1', atf_resources.create_layer.return_value, 'v2'),
        call('cfrpart2', atf_resources.create_layer.return_value, 'va'),
    ]


@pytest.mark.parametrize("headings,expected_labels", [
    ("111.22, 333.44, 555.66", ["111-22", "333-44", "555-66"]),
    ("111.22a, 333.44, 555.66", ["111-22a", "333-44", "555-66"]),
    ("111.22(a)(b), 333.44 (a), 555›66", ["111-22-a-b", "333-44-a", "555-66"]),

], ids=repr)
def test_extract_sections(headings, expected_labels):
    labels = [mapping.label() for mapping in
              atf_resources.extract_sections(headings)]
    assert labels == expected_labels


@pytest.mark.parametrize("date_string, date_object", [
    ("07/01/00", date(2000, 7, 1)),
    ("7/01/00", date(2000, 7, 1)),
    ("7/1/00", date(2000, 7, 1)),
    ("7-1-00", date(1970, 1, 1)),  # Unparseable dates return 1970-01-01.
    ("", date(1970, 1, 1)),  # Missing dates return 1970-01-01.
], ids=repr)
def test_extract_publish_date(date_string, date_object):
    assert atf_resources.extract_publish_date(date_string) == date_object


def test_fetch_resource_data():
    api_data_filepath = pathlib.Path(pathlib.Path(__file__).parent,
                                     "atf_resources_tests.json")
    with api_data_filepath.open() as f:
        fake_api_response = f.read()

    fake_api_json = json.loads(fake_api_response)
    entries = [e["entity"] for e in fake_api_json["entities"]]

    httpretty.enable()
    test_url = atf_resources.settings.ATF_API.format(cfr_part="478")
    httpretty.register_uri(httpretty.GET, test_url, body=fake_api_response)
    fetched = atf_resources.fetch_resource_data("478")
    httpretty.disable()

    for raw_entry, parsed_entry in zip(entries, fetched):
        assert raw_entry["Title"] == parsed_entry.short_title
        assert raw_entry["Document Type"] == parsed_entry.group
        assert raw_entry["URL"] == parsed_entry.url
        if "Document Number" in raw_entry:
            assert raw_entry["Document Number"] == parsed_entry.identifier
        pub_date = atf_resources.extract_publish_date(
            raw_entry["Created/Revision date"])
        assert pub_date == parsed_entry.published
        mappings = [m for m in
                    atf_resources.extract_sections(raw_entry["CFR"])]
        assert mappings == parsed_entry.mappings
