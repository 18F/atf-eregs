from regulations.generator.sidebar.base import SidebarBase


class Rulings(SidebarBase):
    """Sidebar displaying any Rulings related to this section"""
    shorthand = 'rulings'

    def context(self, http_client, request):
        """Fetch the rulings layer data from the API, find any relating to
        this section (including its sub paragraphs); pass them to the
        template"""
        data = http_client.layer('atf-rulings', self.label_id, self.version)
        data = data or {}
        rulings = {}
        for key, value in data.items():
            key = key.split('-')
            is_a_child = key[:len(self.label_parts)] == self.label_parts
            if is_a_child:
                rulings.update(value)
        rulings = sorted(rulings.values(), key=lambda r: r['id'],
                         reverse=True)
        return {'rulings': rulings}
