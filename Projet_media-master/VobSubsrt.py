Projet_media
============

import os
from subprocess import Popen, PIPE
import shlex
import re
import fileinput


mkvpath='<Chemin vers le dossier à lire>'

for mkv in os.listdir(mkvpath):
	mkvSansext=mkv.split('.')[0]
	commandeMKVmerge = shlex.split('mkvmerge -I %s' %(mkv))
	appelMKVmerge = Popen(commandeMKVmerge, stdout=PIPE, universal_newlines=True)
	lectureMKVmerge = appelMKVmerge.stdout.readlines()
	listePistes=[]
	
	for ligne in lectureMKVmerge:
		#ligne=ligne.decode('utf-8')
		if not 'video' in ligne and not 'audio' in ligne:
			recherche=re.search('Track ID ([0-9]{1}): (.*) (\(.*\)) .*language:([a-z]{3})',ligne)
			if recherche:
				numTrack=recherche.group(1)
				pisteNom=recherche.group(2)
				pisteGenre=recherche.group(3)
				pisteLangue=recherche.group(4)
				l=numTrack+pisteNom+pisteLangue
				listePistes.append([numTrack,pisteGenre,pisteLangue])
	appelMKVmerge.stdout.close()
	
	for x in listePistes:
		langue=x[2]
		if x[1]=='(VobSub)':
			commande='%s:%s_%s' %(x[0],mkvSansext,x[2])
			commandeMKVextract=shlex.split('mkvextract tracks %s %s' %(mkv,commande))
			appelMKVextract=Popen(commandeMKVextract,stdout=PIPE)
			stopExtract=appelMKVextract.communicate()
			
		for idx_sub in os.listdir(mkvpath):
			if idx_sub.endswith('.idx'):
				idx=idx_sub
				idxSansext=idx_sub.split('.')[0]
			elif idx_sub.endswith('.sub'):
				sub=idx_sub
				subSansext=idx_sub.split('.')[0]
		commandeSub2tiff=shlex.split('subp2tiff --sid=0 -n %s %s' %(idxSansext,subSansext))
		appelSub2tiff=Popen(commandeSub2tiff, stdout=PIPE)
		stopSub2tiff=appelSub2tiff.communicate()
		commandeSupidxsub=shlex.split('rm %s %s' %(idx,sub))
		appelSupidxsub=Popen(commandeSupidxsub, stdout=PIPE)
		stopRMidxsub=appelSupidxsub.communicate()

		
		for tif in os.listdir(mkvpath):
			if tif.endswith('.tif'):
				tifsansExtention=tif.split('.')[0]
#				p=shlex.split('tesseract %s %s -l fra' %(tifsansExtention,tifsansExtention))
				if langue == 'fre':
					langue=re.sub('fre','fra',langue)
				Commandetif2txt=shlex.split('tesseract %s %s -l %s -psm 6' %(tif,tifsansExtention,langue))
				Appeltif2txt=Popen(Commandetif2txt,stdout=PIPE)
				stoptif2txt=Appeltif2txt.communicate()
				commandeSuptif=shlex.split('rm %s' %(tif))
				appelSuptif=Popen(commandeSuptif,stdout=PIPE)
				stopRMtif=appelSuptif.communicate()
		
		for xml in os.listdir(mkvpath):
			if xml.endswith('.xml'):
				for line in fileinput.input(xml, inplace = 1):
					print (line.replace(".tif", ""))
				commandeSubptools=shlex.split('subptools -s -w -t srt -i %s -o %s_%s.srt' %(xml,mkvSansext,langue))
				appelSubptools=Popen(commandeSubptools,stdout=PIPE)
				stopSubptools=appelSubptools.communicate()
				commandeSupxml=shlex.split('rm %s' % (xml))
				appelSupxml=Popen(commandeSupxml,stdout=PIPE)
				stopRMxml=appelSupxml.communicate()
		for txt in os.listdir(mkvpath):
			if txt.endswith('.txt'):
				commandeSuptxt=shlex.split('rm %s' % (txt))
				appelSuptxt=Popen(commandeSuptxt,stdout=PIPE)
				stopRMtxt=appelSuptxt.communicate()
