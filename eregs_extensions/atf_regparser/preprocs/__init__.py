# vim: set encoding=utf-8
"""Set of transforms we run on notice XML to account for common inaccuracies
in the XML"""
from defusedxml.lxml import etree
from regparser.tree.xml_parser.preprocessors import PreProcessorBase


class USCode(PreProcessorBase):
    """478.103 contains a chunk of the US Code, but does not delineate it
    clearly from the rest of the text of the containing poster. We've created
    `USCODE` tags to clear up this confusion, but we need to modify the XML to
    insert them in the appropriate spot"""
    MARKER = ("//SECTNO[contains(., '478.103')]/.."     # In 478.103
              "//HD[contains(., '18 U.S.C.')]")  # US Code header

    def transform(self, xml):
        for hd in xml.xpath(self.MARKER):
            uscode = etree.Element("USCODE")
            next_el = hd.getnext()
            while next_el is not None and next_el.tag != 'HD':
                uscode.append(next_el)
                next_el = hd.getnext()

            hd_parent = hd.getparent()
            hd_idx = hd_parent.index(hd)
            hd_parent.insert(hd_idx + 1, uscode)
