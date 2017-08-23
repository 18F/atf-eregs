from collections import defaultdict
from datetime import date, datetime
from typing import List, NamedTuple, Optional
import logging
import re

import requests
from django.conf import settings

from regcore.db import storage
from regcore.layer import LayerParams
from regcore_write.views.layer import child_layers


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
    published: date
    mappings: List[Mapping]
    url: str
    identifier: Optional[str] = None


def extract_sections(headings):
    for part_section in headings.split(','):
        part_section = part_section.strip()
        part, section_with_tail = re.split(r'[^\d]', part_section, maxsplit=1)
        if '(' in section_with_tail:
            idx = section_with_tail.index('(')
            section = section_with_tail[:idx].strip()
            subsections = section_with_tail[idx:].strip()
            yield Mapping(part, section, subsections)
        else:
            yield Mapping(part, section_with_tail)


def extract_publish_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%y').date()
    except ValueError:
        logger.warning("Can't parse date %s", date_str)
        return date(1970, 1, 1)


def fetch_resource_data(cfr_part: str) -> List[ResourceData]:
    """Read data from ATF. Currently, this is stubbed by a local yaml file."""
    data = requests.get(settings.ATF_API.format(cfr_part=cfr_part),
                        cfr_part, verify=False).json()
    entries = [e['entity'] for e in data['entities']]

    return [
        ResourceData(
            entry['Title'],
            entry['Document Type'],
            extract_publish_date(entry['Created/Revision date']),
            [mapping for mapping in extract_sections(entry['CFR'])],
            entry['URL'],
            entry.get('Document Number'),
        )
        for entry in entries
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
