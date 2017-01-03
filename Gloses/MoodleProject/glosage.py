# coding: utf-8

import itertools

temp = """
":{trait}"
"-{trait}"
"={trait}"
"~{trait}"
"<{trait}>"

"_{trait}"
"/{trait}"
"{trait}i"

"\\{trait}"
"\\{trait}"
"[{trait}]"
".{trait}"
"({trait})"
"""

def grouperElements(liste, function=len):
	return [list(g) for k,g in itertools.groupby(sorted(liste, key=function), function)]

