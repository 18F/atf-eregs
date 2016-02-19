=========
New Rules
=========
eRegs does not have any sort of background process which polls the Federal
Register waiting for new data. Further, it does not currently handle eCFR
data. Instead, it attempts to derive data from the final rules themselves.
Unfortunately, this is a manually triggered, only semi-automated process
requiring significant individual review.

Until we implement a better solution, however, it works, and allows us to
display rules effective `in the future`. After a final rule has been published
in the Federal Register, the parser should be re-ran and the appropriate XML
file modified (if needed) to generate a correct set of changes. See the
parser's more thorough
`docs <http://eregs-parser.readthedocs.org/en/latest/new_rules.html>`_ on this
subject to learn more.
