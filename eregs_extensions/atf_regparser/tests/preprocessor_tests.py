# vim: set encoding=utf-8
from unittest import TestCase

from tests.xml_builder import XMLBuilderMixin
from atf_regparser.preprocs import USCode


class USCodeTests(XMLBuilderMixin, TestCase):
    def test_uscode_transform(self):
        """US Code issues"""
        with self.tree.builder("PART") as part:
            with part.REGTEXT(ID="RT1") as regtext:
                with regtext.SECTION() as section:
                    section.SECTNO(u"§ 478.103")
                    section.HD("18 U.S.C. 922(x)", SOURCE="HD3")
                    section.P("Some Content")
                    section.HD("Whatever", SOURCE="HED")
        xml = self.tree.render_xml()

        USCode().transform(xml)

        uscode = xml.xpath("//USCODE")
        assert(uscode)
