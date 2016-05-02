# vim: set encoding=utf-8
from unittest import TestCase

from atf_regparser.preprocs import USCode
from regparser.test_utils.xml_builder import XMLBuilder


class USCodeTests(TestCase):
    def test_uscode_transform(self):
        """US Code issues"""
        with XMLBuilder("PART") as ctx:
            with ctx.REGTEXT(ID="RT1"):
                with ctx.SECTION():
                    ctx.SECTNO(u"§ 478.103")
                    ctx.HD("18 U.S.C. 922(x)", SOURCE="HD3")
                    ctx.P("Some Content")
                    ctx.HD("Whatever", SOURCE="HED")
        xml = ctx.xml

        USCode().transform(xml)

        uscode = xml.xpath("//USCODE")
        assert(uscode)
