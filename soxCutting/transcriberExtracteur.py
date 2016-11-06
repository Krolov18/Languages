# coding: utf-8


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

    # on récupère tous les noeuds 'turn' et de ceux-ci, on retourne 'starttime' et 'endtime'

    import codecs

    file = "Memoire_P3Rec5_30oct_21h.trs"
    print(
        *list(
            extraire(
                input=codecs.open(file, 'r', 'latin-1'),
                node="turn",
                start="starttime",
                end="endtime"
            )
        ),
        sep="\n",
        end=""
    )

if __name__ == '__main__':
    main()
