# -*- coding: utf-8 -*-

term_defs = {
    "478": [
        ("Crime punishable by imprisonment for a term exceeding 1 year",
         "Crime punishable by imprisonment for a term exceeding 1 year")
    ]
}

ignores = {
    "479": [
        u"make such return",  # exclude "make"
        u"make returns",  # exclude "make"
        u"make any such returns",  # exclude "make"
        u"Tobacco, Firearms, and Explosives",  # exclude "firearm"
        u"district director of the Internal",  # exclude "director"
        u"director of an Internal",  # exclude "director"
        u"District Director of Customs"  # exclude "district director"
    ],
    "447": [
        "include",
        "including"
    ],
    "555": [u"See definition of “blasting agent.”",
            (u'which meets the definition of “consumer fireworks” or '
             u'“display fireworks” as defined by this section'),
            u'for classification as “consumer fireworks.”']
}
