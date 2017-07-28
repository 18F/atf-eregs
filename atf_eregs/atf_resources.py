"""ATF has associated "ruling" documents, which we'd like to tag to particular
paragraphs. To do that we need to
1) read a config yaml file which maps rulings to regulation paragraphs
2) read a listing of rulings from atf.gov's API
3) connect the two."""
from collections import defaultdict
from typing import Dict, List, NamedTuple, NewType
import logging
import os.path
import re

from regcore.db import storage
from regcore.layer import LayerParams
from regcore_write.views.layer import child_layers
import requests
import yaml


JSON_URL = 'https://www.atf.gov/rules-and-regulations/json'
SPLIT_RE = re.compile(r'(?P<id>[0-9-]+) - (?P<title>.*)')
logger = logging.getLogger(__name__)
LAYER_NAME = 'atf-resources'


ResourceId = NewType('ResourceId', str)
LabelId = NewType('LabelId', str)


class ResourceMeta(NamedTuple):
    url: str
    id: ResourceId
    title: str


ResourceLayer = Dict[LabelId, Dict[ResourceId, Dict[str, str]]]
ResourceConfig = Dict[ResourceId, List[LabelId]]
ResourceMapping = Dict[ResourceId, ResourceMeta]


def load_config() -> ResourceConfig:
    """The config file lives in the code repository; we must find it and parse
    it"""
    this_file = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(this_file))
    data_path = os.path.join(
        root_dir, 'eregs_extensions', 'atf_regparser', 'rulings.yml')
    with open(data_path, 'r') as f:
        data = yaml.safe_load(f)
        # convert types
        return {ResourceId(resource): [LabelId(label) for label in labels]
                for resource, labels in data.items()}


def doc_metadata() -> ResourceMapping:
    """Convert results from www.atf.gov into a dict, associating ruling ids
    with meta data about that ruling"""
    listing = requests.get(JSON_URL).json()
    listing = [n.get('node', {}) for n in listing.get('nodes', [])]
    listing = [n for n in listing if n.get('Document Type') == 'Ruling']
    docs = {}
    for meta in listing:
        match = SPLIT_RE.match(meta.get('Title', ''))
        if not match:
            logging.warning('Could not parse ruling title: %s',
                            meta.get('Title', ''))
        else:
            ident = ResourceId(match.group('id'))
            docs[ident] = ResourceMeta(
                meta.get('URL', ''), ident, match.group('title'))
    if not docs:
        logging.warning('No results from www.atf.gov. Format changed?')
    return docs


def create_layer(config: ResourceConfig, meta: ResourceMapping,
                 cfr_part: LabelId) -> ResourceLayer:
    """Combine configuration with data we retrieved from atf.gov to create a
    layer object suitable for passing over to the regcore machinery."""
    matched = [(ResourceId(ruling), LabelId(label_id))
               for ruling, labels in config.items()
               for label_id in labels
               if ruling in meta and label_id.startswith(cfr_part)]
    layer = defaultdict(dict)
    for ruling, label_id in matched:
        layer[label_id][ruling] = meta[ruling]._asdict()
    return layer


def fetch_and_save_resources() -> None:
    versions_by_part = defaultdict(list)
    for version, cfr_part in storage.for_documents.listing('cfr'):
        versions_by_part[cfr_part].append(version)

    config = load_config()
    meta = doc_metadata()

    for cfr_part, versions in versions_by_part.items():
        layer = create_layer(config, meta, LabelId(cfr_part))
        for version in versions:
            params = LayerParams(
                'cfr', '{0}/{1}'.format(version, cfr_part), cfr_part)
            storage.for_layers.bulk_delete(
                LAYER_NAME, params.doc_type, params.doc_id)
            storage.for_layers.bulk_insert(
                child_layers(params, layer), LAYER_NAME, params.doc_type)
            logger.info('Loaded Additional Resources layer for %s@%s',
                        cfr_part, version)
