__author__ = 'korantin'

from bs4 import BeautifulSoup as bs

class transcriberExtracteur:
    """
        A long terme,cette classe va dépouiller un fichier trs.
        Elle prendra en compte toutes les étiquettes.
        (racine)
        Trans [scribe, audio_filename, version, version_date]
            Topics []
                Topic [id, desc]
            Speakers []
                Speaker [id, name, check, dialect, accent, scope]
            Episode []
                Section [type, startTime, endTime]
                    Turn [startTime, endTime]
                        Sync [time]
    """
    def __init__(self,xmlFile):
        if not xmlFile.endswith(".xml"):
            raise TypeError("Le fichier fourni doit être au format xml.")
        self.entree = bs(open(xmlFile))
        self.extractions = []
    def extraireTemps(self,noeud="Turn", attributs=["startTime","endTime"]):
        """
            Il sera extrait tous les noeuds (ayant pour noeud "node") du fichier avec pour attributs attributes.
            Cette méhode remplie self.extractions.

        :param nodeAttribute: dictionnaire
        :return: None
        """
        (debut,fin) = attributs
        temp = self.entree.find_all(noeud)
        [self.extractions.append((x.get(debut),x.get(fin))) for x in temp]