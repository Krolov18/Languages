# coding: utf-8


def fonction(lex_name, number_name):
    import codecs
    import pickle

    numbers = pickle.load(open(number_name+'.pickle', 'rb')).get('français')

    with codecs.open(lex_name, 'r', 'utf-8') as f:
        f.readline()
        # yield tuple([x.split('_')[1] for x in f.readline().strip().split('\t')]+["isinteger", "integer"])
        for line in f:
            tmp1 = [(0, "")]
            tmp2 = line.strip().split('\t')
            if tmp2[3] == "ADJ:num" or tmp2[0] in ["million", "milliard", "zéro"]:
                tmp1 = [(1, number) for number in numbers if (
                    (
                        tmp2[0] == numbers.get(number).get('graphie')
                    ) and (
                        tmp2[1] == numbers.get(number).get('phonologie')
                    )
                )]
                if not tmp1:
                    tmp1 = [(0, "")]

            yield tuple(line.split("\t"))+tmp1[0]


def main():
    import sqlite3

    tmp = fonction("Lexique381.txt", "exceptions")
    with sqlite3.connect('Lexique.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE Lexique (
                                    ortho STRING,
                                    phon STRING,
                                    lemme STRING,
                                    cgram STRING,
                                    genre STRING,
                                    nombre STRING,
                                    freqlemfilms2 STRING,
                                    freqlemlivres STRING,
                                    freqfilms2 STRING,
                                    freqlivres STRING,
                                    infover STRNG,
                                    nbhomogr STRING,
                                    nbhomoph STRING,
                                    islem STRING,
                                    nblettres STRING,
                                    nbphons STRING,
                                    cvcv STRING,
                                    p STRING,
                                    voisorth STRING,
                                    voisphon STRING,
                                    puorth STRING,
                                    puphon STRING,
                                    syll STRING,
                                    nbsyll STRING,
                                    cv_cv STRING,
                                    orthrenv STRING,
                                    phonrenv STRING,
                                    orthosyll STRING,
                                    cgramortho STRING,
                                    deflem STRING,
                                    defobs STRING,
                                    old20 STRING,
                                    pld20 STRING,
                                    morphoder STRING,
                                    nbmorph STRING,
                                    isinteger STRING,
                                    integer STRING
    )""")
        cursor.executemany(
            '''INSERT INTO Lexique VALUES (
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?,?,?,?,
                        ?,?)''', tmp)
        conn.commit()


def main2():
    import sqlite3
    with sqlite3.connect("Lexique.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Lexique where ortho = ?", ("vingt",))

    print(cursor.fetchone())

if __name__ == '__main__':
    main2()
