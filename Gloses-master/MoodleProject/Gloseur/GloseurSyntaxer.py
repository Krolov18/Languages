# coding: utf-8

from latex import build_pdf
import GloseurLexer
tokens = GloseurLexer.tokens

from Node import Node as Gloseur, BTOS
import ply.yacc as yacc


def p_M1(p):
    """M : K"""
    p[0] = Gloseur(
        head="M",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_M2(p):
    """M : K GPHRASES"""
    p[0] = Gloseur(
        head="M",
        children=[p[1],p[2]],
        feedback=BTOS(
            bout=p[1].feedback.B + p[2].feedback.B,
            trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
            syntaxe=p[1].feedback.S + p[2].feedback.S
        )
    )

def p_K1(p):
    """K : R"""
    p[0] = Gloseur(
        head="K",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_K2(p):
    """K : R TS"""
    p[0] = Gloseur(
        head="K",
        children=[p[1],p[2]],
        feedback=BTOS(
            bout=p[1].feedback.B + p[2].feedback.B,
            trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
            syntaxe=p[1].feedback.S + p[2].feedback.S
        )
    )

def p_GPHRASE(p):
    """GPHRASE : PHRASE K"""
    p[0] = Gloseur(
        head="GPHRASE",
        children=[
            Gloseur(
                head="PHRASE",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_GPHRASES1(p):
    """GPHRASES : GPHRASE GPHRASES
    			| GPHRASE
    """
    if len(p) == 3:
        p[0] = Gloseur(
            head="GPHRASES",
            children=[p[1], p[2]],
            feedback=BTOS(
                bout=p[1].feedback.B + p[2].feedback.B,
                trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
                syntaxe=p[1].feedback.S + p[2].feedback.S
            )
        )
    else:
        p[0] = Gloseur(
            head="GPHRASES",
            children=[p[1]],
            feedback=BTOS(
                bout=p[1].feedback.B,
                trait_ordre=p[1].feedback.TO,
                syntaxe=p[1].feedback.S
            )
        )

def p_R1(p):
    """R : LEMME POLYP"""
    p[0] = Gloseur(
        head="R",
        children=[
            Gloseur(
                head="LEMME",
                leaf=p[1],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[1]],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[] + p[2].feedback.B,
            trait_ordre=[p[1]] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_R2(p):
    """R : LEMME INHERP"""
    p[0] = Gloseur(
        head="R",
        children=[
            Gloseur(
                head="LEMME",
                leaf=p[1],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[1]],
                    syntaxe=[p[1]]
                )
            ),
        p[2]
        ],
        feedback=BTOS(
            bout=[] + p[2].feedback.B,
            trait_ordre=[p[1]] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_R3(p):
    """R : POLYP"""
    p[0] = Gloseur(
        head="R",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_R4(p):
    """R : DPTRAIT LEMME"""
    p[0] = Gloseur(
        head="R",
        children=[
            p[1],
            Gloseur(
                head="LEMME",
                leaf=p[2],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[2]],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [],
            trait_ordre=[] + [p[2]],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_GPTRAIT(p):
    """GPTRAIT : PORTMA TRAIT"""
    p[0] = Gloseur(
        head="GPTRAIT",
        children=[
            Gloseur(
                head="PORTMA",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            Gloseur(
                head="TRAIT",
                leaf=p[2],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[2]],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=[p[1]] + [],
            trait_ordre=[] + [p[2]],
            syntaxe=[p[1]] + [p[2]]
        )
    )

def p_GPTRAITS1(p):
    """GPTRAITS : GPTRAIT GPTRAITS
    			| GPTRAIT
    """
    if (len(p) == 3):
        p[0] = Gloseur(
            head="GPTRAITS",
            children=[p[1], p[2]],
            feedback=BTOS(
                bout=p[1].feedback.B + p[2].feedback.B,
                trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
                syntaxe=p[1].feedback.S + p[2].feedback.S
            )
        )
    else:
        p[0] = Gloseur(
            head="GPTRAITS",
            children=[p[1]],
            feedback=BTOS(
                bout=p[1].feedback.B,
                trait_ordre=p[1].feedback.TO,
                syntaxe=p[1].feedback.S
            )
        )

def p_DPTRAIT(p):
    """DPTRAIT : TRAIT PORTMA"""
    p[0] = Gloseur(
        head="DPTRAIT",
        children=[
            Gloseur(
                head="TRAIT",
                leaf=p[1],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[1]],
                    syntaxe=[p[1]]
                )
            ),
            Gloseur(
                head="PORTMA",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout= [] + [p[2]],
            trait_ordre=[p[1]] + [],
            syntaxe=[p[1]] + [p[2]]
        )
    )

def p_POLYP1(p):
    """POLYP : RT"""
    p[0] = Gloseur(
        head="POLYP",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_POLYP2(p):
    """POLYP : RT POLYS"""
    p[0] = Gloseur(
        head="POLYP",
        children=[p[1], p[2]],
        feedback=BTOS(
            bout=p[1].feedback.B + p[2].feedback.B,
            trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
            syntaxe=p[1].feedback.S + p[2].feedback.S
        )
    )

def p_RT1(p):
    """RT : TRAIT"""
    p[0] = Gloseur(
        head="RT",
        children=[
            Gloseur(
                head="TRAIT",
                leaf=p[1],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[1]],
                    syntaxe=[p[1]]
                )
            )
        ],
        feedback=BTOS(
            bout=[],
            trait_ordre=[p[1]],
            syntaxe=[p[1]]
        )
    )

def p_RT2(p):
    """RT : TRAIT GPTRAITS"""
    p[0] = Gloseur(
        head="RT",
        children=[
            Gloseur(
                head="TRAIT",
                leaf=p[1],
                feedback=BTOS(
                    bout=[],
                    trait_ordre=[p[1]],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[] + p[2].feedback.B,
            trait_ordre=[p[1]] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_RT3(p):
    """RT : GPTRAITS"""
    p[0] = Gloseur(
        head="RT",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_POLY(p):
    """POLY : POLYSE RT"""
    p[0] = Gloseur(
        head="POLY",
        children=[
            Gloseur(
                head="POLYSE",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_POLYS1(p):
    """POLYS : POLY POLYS
    		 | POLY
    """
    if len(p) == 3:
        p[0] = Gloseur(
            head="POLYS",
            children=[p[1],p[2]],
            feedback=BTOS(
                bout=p[1].feedback.B + p[2].feedback.B,
                trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
                syntaxe=p[1].feedback.S + p[2].feedback.S
            )
        )
    else:
        p[0] = Gloseur(
            head="POLYS",
            children=[p[1]],
            feedback=BTOS(
                bout=p[1].feedback.B,
                trait_ordre=p[1].feedback.TO,
                syntaxe=p[1].feedback.S
            )
        )

def p_INHERP(p):
    """INHERP : GINHER POLYP DINHER"""
    p[0] = Gloseur(
        head="INHERP",
        children=[
            Gloseur(
                head="GINHER",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2],
            Gloseur(
                head="DINHER",
                leaf=p[3],
                feedback=BTOS(
                    bout=[p[3]],
                    trait_ordre=[],
                    syntaxe=[p[3]]
                )
            )
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B + [p[3]],
            trait_ordre=[] + p[2].feedback.TO + [],
            syntaxe=[p[1]] + p[2].feedback.S + [p[3]]
        )
    )

def p_MORPH0(p):
    """MORPH0 : GMORPH0 POLYP DMORPH0"""
    p[0] = Gloseur(
        head="MORPH0",
        children=[
            Gloseur(
                head="GMORPH0",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2],
            Gloseur(
                head="DMORPH0",
                leaf=p[3],
                feedback=BTOS(
                    bout=[p[3]],
                    trait_ordre=[],
                    syntaxe=[p[3]]
                )
            )
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B + [p[3]],
            trait_ordre=[] + p[2].feedback.TO + [],
            syntaxe=[p[1]] + p[2].feedback.S + [p[3]]
        )
    )

def p_INFIX(p):
    """INFIX : GINFIX POLYP DINFIX"""
    p[0] = Gloseur(
        type=None,
        head="INFIX",
        children=[
            Gloseur(
                head="GINFIX",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2],
            Gloseur(
                head="DINFIX",
                leaf=p[3],
                feedback=BTOS(
                    bout=[p[3]],
                    trait_ordre=[],
                    syntaxe=[p[3]]
                )
            )
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B + [p[3]],
            trait_ordre=[] + p[2].feedback.TO + [],
            syntaxe=[p[1]] + p[2].feedback.S + [p[3]]
        )
    )

def p_T1(p):
    """T : REDUPL POLYP"""
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="REDUPL",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_T2(p):
    """T : POLYP REDUPL"""
    p[0] = Gloseur(
        head="T",
        children=[
            p[1],
            Gloseur(
                head="REDUPL",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_T3(p):
    """T : ABLAUT POLYP"""
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="ABLAUT",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_T4(p):
    """T : POLYP ABLAUT"""
    p[0] = Gloseur(
        head="T",
        children=[
            p[1],
            Gloseur(
                head="ABLAUT",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_T5(p):
    """T : CLITIC POLYP"""
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="CLITIC",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_T6(p):
    """T : POLYP CLITIC"""
    p[0] = Gloseur(
        type=None,
        head="T",
        children=[
            p[1],
            Gloseur(
                head="CLITIC",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_T7(p):
    """T : UNSPEC POLYP"""
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="UNSPEC",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_T8(p):
    """T : POLYP UNSPEC"""
    p[0] = Gloseur(
        head="T",
        children=[
            p[1],
            Gloseur(
                head="UNSPEC",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_T9(p):
    """T : AFFIX POLYP"""
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="AFFIX",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
            syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_T10(p):
    """T : POLYP AFFIX"""
    p[0] = Gloseur(
        head="T",
        children=[
            p[1],
            Gloseur(
                head="AFFIX",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

# def p_T11(p):
#     """T : CIRCONF2 POLYP"""
#     p[0] = Gloseur(
#         head="T",
#         children=[
#             Gloseur(
#                 head="CIRCONF2",
#                 leaf=p[1],
#                 feedback=BTOS(
#                     bout=[p[1]],
#                     trait_ordre=[],
#                     syntaxe=[p[1]]
#                 )
#             ),
#             p[2]
#         ],
#         feedback=BTOS(
#             bout=[p[1]] + p[2].feedback.B,
#             trait_ordre=[] + p[2].feedback.TO,
#             syntaxe=[p[1]] + p[2].feedback.S
#         )
#     )

def p_T12(p):
    """T : POLYP CIRCONF2"""
    p[0] = Gloseur(
        head="T",
        children=[
            p[1],
            Gloseur(
                head="CIRCONF2",
                leaf=p[2],
                feedback=BTOS(
                    bout=[p[2]],
                    trait_ordre=[],
                    syntaxe=[p[2]]
                )
            )
        ],
        feedback=BTOS(
            bout=p[1].feedback.B + [p[2]],
            trait_ordre=p[1].feedback.TO + [],
            syntaxe=p[1].feedback.S + [p[2]]
        )
    )

def p_T13(p):
    """T : INFIX"""
    p[0] = Gloseur(
        head="T",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

def p_T14(p):
    """T : MORPH0"""
    p[0] = Gloseur(
        head="T",
        children=[p[1]],
        feedback=BTOS(
            bout=p[1].feedback.B,
            trait_ordre=p[1].feedback.TO,
            syntaxe=p[1].feedback.S
        )
    )

# il ne@1 faut pas@1 mourir
def p_T15(p):
    "RT : POLYP CIRCONF1"
    p[0] = Gloseur(
        head="T",
        children=[
            Gloseur(
                head="CIRCONF1",
                leaf=p[1],
                feedback=BTOS(
                    bout=[p[1]],
                    trait_ordre=[],
                    syntaxe=[p[1]]
                )
            ),
            p[2]
        ],
        feedback=BTOS(
            bout=[p[1]] + p[2].feedback.B,
            trait_ordre=[] + p[2].feedback.TO,
             syntaxe=[p[1]] + p[2].feedback.S
        )
    )

def p_TS1(p):
    """TS : T TS
    	  | T
    """
    if len(p) == 3:
        p[0] = Gloseur(
            head="TS",
            children=[p[1],p[2]],
            feedback=BTOS(
                bout=p[1].feedback.B + p[2].feedback.B,
                trait_ordre=p[1].feedback.TO + p[2].feedback.TO,
                syntaxe=p[1].feedback.S + p[2].feedback.S
            )
        )
    else:
        p[0] = Gloseur(
            head="TS",
            children=[p[1]],
            feedback=BTOS(
                bout=p[1].feedback.B,
                trait_ordre=p[1].feedback.TO,
                syntaxe=p[1].feedback.S
            )
        )

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parcours_deep(obj):
    if (obj.children == None):
        print("B :  ",obj.head,obj.feedback.B)
        print("TO : ",obj.head,obj.feedback.TO)
        print("S :  ",obj.head,obj.feedback.S)
    else:
        print("B :  ",obj.head,obj.feedback.B)
        for child in obj.children:
            parcours_deep(child)
        print("TO : ",obj.head,obj.feedback.TO)
        print("S :  ",obj.head,obj.feedback.S)

phrases = [
    "DEF.M.SG.NLIAIS"
]

min_latex = """
            \\documentclass[a2paper,landscape]{{article}}\n
            \\usepackage{{qtree}}
            \\usepackage{{geometry}}
            \\begin{{document}}\n\n
            \\small{{
            \\Tree {0}\n\n
            }
            \\end{{document}}\n
"""

for phrase in phrases:
    result = parser.parse(phrase)
    parcours_deep(result)
    #op = open("phrases/"+"".join(result.feedback.S)+".tex","w")
    #op.write(min_latex % result.to_string)