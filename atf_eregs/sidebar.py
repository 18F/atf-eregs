from collections import defaultdict
from typing import List

from regulations.generator.sidebar.base import SidebarBase


def filter_to_children(data, root_label: List[str]):
    """The data that we get back from the API may include more than we desire.
    Filter only to nodes that are children of the root."""
    data = data or {}
    result = {}
    for label_str, values in data.items():
        label = label_str.split('-')
        is_a_child = label[:len(root_label)] == root_label
        if is_a_child:
            result[label_str] = values
    return result


class Rulings(SidebarBase):
    """Sidebar displaying any Rulings related to this section"""
    shorthand = 'rulings'

    def context(self, http_client, request):
        """Fetch the rulings layer data from the API, find any relating to
        this section (including its sub paragraphs); pass them to the
        template"""
        data = http_client.layer('atf-rulings', 'cfr', self.label_id,
                                 self.version)
        rulings = {}
        for key, value in filter_to_children(data, self.label_parts).items():
            rulings.update(value)
        rulings = sorted(rulings.values(), key=lambda r: r['id'],
                         reverse=True)
        return {'rulings': rulings}


def order_groups(groups):
    """Re-order groups by priority and convert them to dicts."""
    for name in ('Ruling', 'Form', 'FAQ', 'Open Letter'):
        if name in groups:
            entries = groups.pop(name)
            yield {'name': name, 'count': len(entries), 'entries': entries}
    for name in sorted(groups):
        entries = groups[name]
        yield {'name': name, 'count': len(entries), 'entries': entries}


class ATFResources(SidebarBase):
    shorthand = 'atf-resources'

    def context(self, http_client, request):
        data = http_client.layer('atf-resources', 'cfr', self.label_id,
                                 self.version)
        data = filter_to_children(data, self.label_parts)
        groups = defaultdict(list)
        for label_id, group_dict in data.items():
            for group_name, values in group_dict.items():
                groups[group_name].extend(values)

        ordered_groups = list(order_groups(groups))
        return {
            'count': sum(g['count'] for g in ordered_groups),
            'groups': ordered_groups,
        }
