__author__ = 'korantin'

import sqlite3

class Adresse(sqlite3):
    def __init__(self, database, table, colonne):
        super(sqlite3, self).__init__(database)
        self.database = database
        self.table = table
        self.colonne = colonne
        self.positionMachine = ""
    def __repr__(self):
        pass
    def __str__(self):
        print(self.database, self.table, self.colonne)