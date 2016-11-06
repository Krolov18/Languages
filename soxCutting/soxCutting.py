# coding: utf-8


def decoupe(soundfile: str, start: float, end: float, output=None) -> None:
    import shlex
    import subprocess
    import sys
    import operator

    commande = "sox {input} {output} trim {start} {duration}"

    if output is None:
        output = ".".join(["_".join([soundfile.rpartition('.')[0], str(start)]), "wav"])

    print(
        output,
        "DONE",
        file=sys.stderr,
        sep=" "
    )

    x=subprocess.Popen(
        shlex.split(
            commande.format(
                input=soundfile,
                output=output,
                start=str(start),
                duration=str(operator.sub(float(end), float(start)))
            )
        )
    )
    x.communicate()



def extraire(input: open, node: str, start="", end=""):
    import sys
    import bs4

    soup = bs4.BeautifulSoup(input, 'lxml')

    return map(
        lambda x: (
            x.get(start),
            x.get(end)
        ),
        soup.find_all(node)
    )


def main():
    import codecs
    import argparse
    import sqlite3

    parser = argparse.ArgumentParser(
        prog="soxCutting",
        description="""
            Prend un fichier xml, csv, ou une base de donnée contenant des bornes de début et de fin
            et découpe input (un fichier son) sur ces bornes.
            """,
        usage="%(prog)s [options] input output"
    )

    parser.add_argument(
        "input",
        help="Cet argument prend le nom du son à découper."
    )

    parser.add_argument(
        "--output",
        "-o",
        help="chaine de caractère sans extention qui représentera le nom du fichier son découpé.",
        type=str
    )

    parser.add_argument(
        "--start",
        "-s",
        help="""
            prend un float. Attention un float bien formé est du type 3.2
            soit un point entre la partie entière et la partie décimale
            """,
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
        help="""Cette option permet de prendre un fichier xml en entrée."""
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
        help="""
                On prend en argument un fichier csv
                le csv doit être composé de quatre colonnes (name, id, start, end)
            """
    )

    parser.add_argument(
        "--separator",
        "-sep",
        help='chaine de caractère représentant le séparateur du fichier csv'
    )

    args = parser.parse_args()

    (filename, extention) = args.input.rpartition('.')[::2]

    if all((args.output, args.start, args.end)):
        decoupe(
            soundfile=args.input,
            start=args.start,
            end=args.end,
            output=".".join(
                [
                    "_".join(
                        [
                            args.output,
                            args.start,
                            args.end,
                        ]
                    ),
                    extention
                ]
            )
        )

    elif args.csvFile and args.separators:
        temp = codecs.open(args.csvFile, 'r', 'utf-8').read().splitlines()

        for extraction in map(lambda x: x.split(args.separator), temp):
                (name, id, start, end) = extraction
                decoupe(
                    soundfile=args.input,
                    start=start,
                    end=end,
                    output=".".join(
                        [
                            "_".join(
                                [
                                    args.output,
                                    start,
                                    end
                                ]
                            ),
                            extention
                        ]
                    ) if args.output else ".".join(
                        [
                            "_".join(
                                [
                                    name,
                                    start,
                                    end
                                ]
                            ),
                            extention
                        ]
                    )
                )

    elif args.xmlFile is not None:
        temps = extraire(
            input=codecs.open(args.xmlFile, 'r', 'latin-1'),
            node="turn",
            start="starttime",
            end="endtime"
        )

        list(map(
            lambda x: decoupe(
                soundfile=args.input,
                start=x[0],
                end=x[1],
                output=None
            ),
            temps
        ))

        # print('PROUT')
        # print(list(map(lambda x: (x[0], x[1]), temps)))
        # [
        #     decoupe(
        #         soundfile=args.input,
        #         start=x,
        #         end=y,
        #         output=".".join(
        #             [
        #                 "_".join(
        #                     [
        #                         filename,
        #                         x,
        #                         y
        #                     ]
        #                 ),
        #                 extention
        #             ]
        #         )
        #     ) for x, y in temps
        # ]

    elif args.dataBase:
        curseur = args.dataBase.cursor()
        commande = "SELECT name, start, end FROM stims"
        curseur.execute(commande)
        extractions = curseur.fetchall()

        for extraction in extractions[1:]:
            (name, start, end) = extraction
            if name in args.input.entree:
                args.input.decouper(start, end)


def main2():
    import codecs
    temps = list(extraire(codecs.open("//Volumes/KOKO/test/VOIX_mme_mathon_TD3.trs", 'r', 'latin-1'), node='turn', start="starttime", end="endtime"))
    decoupe(
        soundfile="//Volumes/KOKO/test/VOIX_mme_mathon_TD3.WAV",
        start=temps[0][0],
        end=temps[0][1]
    )

if __name__ == "__main__":
    main()
