from collections import defaultdict
from typing import List, NamedTuple, Optional
import logging
import os.path

from regcore.db import storage
from regcore.layer import LayerParams
from regcore_write.views.layer import child_layers
import yaml


logger = logging.getLogger(__name__)
LAYER_NAME = 'atf-resources'


class Mapping(NamedTuple):
    part: str
    section: str
    subsection: Optional[str] = None

    def label(self):
        """Convert to a hyphen-separated string"""
        components = [self.part, self.section]
        if self.subsection:
            # convert paren syntax into ours
            components.extend(
                p.strip('()') for p in self.subsection.split(')('))
        return '-'.join(components)


class ResourceData(NamedTuple):
    short_title: str
    group: str
    published: str  # this should encode a date, but we don't need to verify
    mappings: List[Mapping]
    url: str
    identifier: Optional[str] = None


def fetch_resource_data(cfr_part: str) -> List[ResourceData]:
    """Read data from ATF. Currently, this is stubbed by a local yaml file."""
    this_file = os.path.abspath(__file__)
    app_dir = os.path.dirname(this_file)
    data_path = os.path.join(app_dir, 'related-docs.yml')
    with open(data_path, 'r') as f:
        data = yaml.safe_load(f.read())
        return [
            ResourceData(
                entry['short_title'],
                entry['group'],
                entry['published'],
                [Mapping(str(m['part']), str(m['section']),
                         m.get('subsection'))
                 for m in entry['mappings']],
                entry['url'],
                entry.get('identifier'),
            )
            for entry in data
        ]


class Entry(NamedTuple):
    short_title: str
    url: str
    identifier: Optional[str] = None


def create_layer(cfr_part: str, data: List[ResourceData]):
    """Convert the ATF data into a layer, keyed by paragraph label_id."""
    data = list(sorted(data, key=lambda d: (d.published, d.short_title),
                       reverse=True))
    layer = defaultdict(lambda: defaultdict(list))

    for resource in data:
        for mapping in resource.mappings:
            if mapping.part == cfr_part:
                entry = Entry(resource.short_title, resource.url,
                              resource.identifier)
                layer[mapping.label()][resource.group].append(entry._asdict())

    return layer


def save_layer(cfr_part, layer, version):
    """Write layer data to the database."""
    params = LayerParams('cfr', '{0}/{1}'.format(version, cfr_part), cfr_part)
    storage.for_layers.bulk_delete(LAYER_NAME, params.doc_type, params.doc_id)
    storage.for_layers.bulk_insert(child_layers(params, layer), LAYER_NAME,
                                   params.doc_type)
    logger.info('Loaded Additional Resources layer for %s@%s', cfr_part,
                version)


def fetch_and_save_resources() -> None:
    versions_by_part = defaultdict(list)
    for version, cfr_part in storage.for_documents.listing('cfr'):
        versions_by_part[cfr_part].append(version)

    for cfr_part, versions in versions_by_part.items():
        data = fetch_resource_data(cfr_part)
        layer = create_layer(cfr_part, data)
        for version in versions:
            save_layer(cfr_part, layer, version)
