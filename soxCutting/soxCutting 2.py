__author__ = 'korantin'

from codecs import open
import transcriberExtracteur
import DecoupeurFichier
import argparse
import sqlite3
import yaml
import DecoupeurRecursif


def soxCutting():
    parser = argparse.ArgumentParser(
        prog="splitter",
        description="",
        usage="%(prog)s [options] input output"
    )
    parser.add_argument(
        "input",
        help="Cet argument prend le nom du son à découper.",
        type=DecoupeurFichier.DecoupeurFichier
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Cet argument prend le nom du son découpé.",
        type=str
    )
    parser.add_argument(
        "--start",
        "-s",
        help="""prend un float. Attention un float bien formé est du type 3.2
                soit un point entre la partie entière et la partie décimale""",
        nargs=1,
        type=float
    )
    parser.add_argument(
        "--end",
        "-e",
        help="""prend un float. Attention un float bien formé est du type 3.2
                soit un point entre la partie entière et la partie décimale""",
        nargs=1,
        type=float
    )
    parser.add_argument(
        "--xmlFile",
        "-xml",
        help="""Cette option permet de prendre un fichier xml en entrée.""",
        type=transcriberExtracteur.transcriberExtracteur,
        nargs=1
    )
    parser.add_argument(
        "--dataBase",
        "-db",
        help="On prend en argument un objet de type bdd.",
        type=sqlite3.connect
    )
    parser.add_argument(
        "--csvFile",
        "-csv",
        help="""On prend en argument un fichier csv avec ses separateurs en parametres
                Attention, les parametres doivent etre de la forme d'une liste soit:
                [['\\n'],[' '],['/','r',1]]
                Cet exemple va donc d'abord découper sur les retours à la ligne (\\n) puis
                sur les espaces (' ') et enfin sur les slashs ('/') en partant
                de la droite et une seul fois.""",
        type=open,
        nargs=1
    )
    parser.add_argument(
        "--separators",
        "-sep",
        help='',
        nargs="?",
        type=list,
        default=[["\n"],[","]]
    )
    args = parser.parse_args()

    if args.output!=None and args.start!=None and args.end!=None:
        args.input.decouper(args.start, args.end)
    # elif args.csvFile != None and args.separators = None:
    #     print("**************************************")
    #     temp = DecoupeurRecursif.DecoupeurRecursif(args.csvFile[0].read())
    #     temp.decouper(args.separators)
    #     print(temp.liste)
    #     for extraction in temp.liste:
    #         if extraction[0] == "Rec2_":
    #             print(len(extraction))
    #             (name,id,start,end) = extraction
    #             args.input.decouper(start,end)
    elif args.xmlFile:
        temps = args.xmlFile.extractions
        for temp in temps:
            (start,end) = temp
            args.input.decouper(start,end)
    elif args.dataBase:
        curseur = args.dataBase.cursor()
        commande = "SELECT * FROM stims"
        curseur.execute(commande)
        extractions = curseur.fetchall()
        for extraction in extractions[1:]:
            (name,id, start, end) = extraction
            if name in args.input.entree:
                args.input.decouper(start,end)
    else:
        args.input.decouper(args.start,args.end)

if __name__ == "__main__":
    soxCutting()
