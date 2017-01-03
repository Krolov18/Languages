__author__ = 'korantin'

from subprocess import Popen
import shlex

class DecoupeurFichier:
    def __init__(self,soundFile):
        self.entree = soundFile
        self.mainCommand = "sox {input} {output} trim {start} {duration}"
    def decouper(self, start, end):
        print(self.entree)
        output = ".".join(["_".join([self.entree, str(start)]),".wav"])
        Popen(shlex.split(self.mainCommand.format(input=self.entree,output=output, start=str(start), duration=str(float(end)-float(start)))))