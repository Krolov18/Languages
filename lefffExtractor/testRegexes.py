import re
morphologie = {'3fs', '3m', '3', '3ms', 'F3s', 'pcasdevant', 'ms_P1p', 'CtrlSubjA', 'J12s', 's_P3p', 'fs_P3p', 'P3s',
               'pcasaprès', 'AAPourPro', 'P2s', 'J3s', 'pcaspour', 'CtrlObjA', 'mp_P1s', 'C1p', '1p', 'F2s', 'CtrlObjDe',
               'ms_P1s', 'SCompSubj', 'fs', 'C3s', 'CtrlSubjDe', 'F1s', 'fp_P2s', 'pcaspar', 'pro_nom', 'CtrlProA', 'ASCompSubj',
               'fs_P1s', 'Kfs', 'PFIJTSC', 'P2p', 'T2p', 'S2s', 'fêtre', 'f', 'p_P1p', 'loc', 'CtrlProDe', 'J2s', 'DeSCompSubj',
               'fp_P1p', '3mp', 'Y', 'p_P2s', 'CtrlAObjDe', 'pro_acc', '2p', 'pcasen', 'C3p', 'pcascontre', 'fs_P2s', 'pcasavec',
               'I12s', 'T3s', 'PS3s', 'CtrlSubj', 'PS3p', 'PS13s', 'F3p', 'P12s', 'mp_P2p', 'S1p', 'mp', 'K', 'I2p', 'ST2s', 'CtrlAObjA',
               'CtrlPro', 'AAPro', 'pcascomme', 'T2s', 'CtrlObj', 'DeSCompInd', 'S3s', 'AADeSubj', 'm', 'S2p', 'pcasvers', 'ms_P3s', 'F1p',
               'AAPourObj', 'passive', 'G', 'I1s', 'I3s', 'C2p', 'active', 'p_P1s', 'fs_P3s', 's_P1p', 'mp_P1p', 'PS3', 'p', 'fs_P1p', 'W',
               'fp_P1s', 'C12s', 'AAObj', 'AASubj', 'Y2p', 'AAPourSubj', '3p', 'Y2s', 's_P2s', 'C1s', '3s', 'Ca', '1s', 'I3p', 'S3p',
               'fp_P3p', 'I1p', 'fp', 'J3p', 'pron', 'AADeObj', 's_P1s', 'time', 'fs_P2p', 'poss', 'S13s', 'mp_P2s', 'J1s', 'e', 'P1s',
               'P1p', 'être', 'mp_P3p', 'favoir', 'ms_P3p', 'Kms', 'pro_gen', 'Kmp', 'fp_P3s', 'pcasà', 's_P2p', 'ms', 'Il', 'hum', 'T1p',
               'p_P3p', 'Km', 'p_P2p', 'ms_P2p', 'avoir', 'Y1p', 'P3p', 's', 'pcassur', '2s', 'PJ12s', 'ms_P2s', 'PS2s', 'T1s', 'pcasdans',
               'S1s', 'fp_P2p', 'T3p', 'pcasde', 'pro_loc', 'F2p', 'mp_P3s', 'SCompInd', 'J1p', '3fp', 's_P3s', 'p_P3s', 'J2p', 'Kfp', 'imperative'}
morpho = """
        (être|avoir|)               # auxiliaire utilisé par le verbe (pour former actif/passif)
        (pcasaprès|pcasavec|pcascomme|pcascontre|pcasdans|pcasde|pcasdevant|pcasen|pcaspar|pcaspour|pcassur|pcasvers|pcasà|)
        (Il|Ca|)                     # Impersonnel
        (CtrlAObjA|CtrlAObjDe|CtrlObj|CtrlObjA|CtrlObjDe|CtrlPro|CtrlProA|CtrlProDe|CtrlSubj|CtrlSubjA|CtrlSubjDe|) #verbe à controle
        (AADeObj|AADeSubj|AAObj|AAPourObj|AAPourPro|AAPourSubj|AAPro|AAPro|AASubj|) # Verbe attributifs
        (DeSCompInd|DeSCompSubj|ASCompSubj|SCompInd|SCompSubj|) # Verbe avec complémenteurs
        (favoir|fêtre|) # auxiliaire être et avoir
        (active|passive|)           # diathèse
        ([PIJFSTKGYCW]*)            # temps_mode
        ([123]*)                    # personne
        ([mf]?)                     # genre
        ([sp]?)                     # nombre
        (?:_?P?([123]?)([sp]?))     # poss_pers, poss_nb
        """
# morpo = re.compile("([PIJFSTKGYCW]*)([123]*)([mf]?)([sp]?)(?:_?P?([123]?)([sp]?))")
temp = set([])
for x in morphologie:
    valeurs = re.search(morpho,x,re.VERBOSE).groups()
    temp0 = valeurs[8:]
    for x in temp0:
        temp |= set(x)
    temp |= set(valeurs[:8])

    #etiquettes = ["AuxVerb","pcas","impersonnel","controle","attribut","SComp","AuxEtrAvo","diathèse","temps_mode","personne","genre","nombre","poss_pers","poss_nb"]
    #attributs = dict(zip(etiquettes,valeurs))
    #print(attributs)
for x in sorted(list(temp)):
    print(x)