import Bio.Blast.Applications
import subprocess
import Bio.Blast.NCBIXML
import os
import os.path

blastCmd = r'/usr/local/ncbi/blast/bin/'
stdDbName = 'dbyeast'
customDbName = 'my'
customDbFastaFileName = "my.fa"

def saveTempFile(seq):
	fileName = "tempInputFile.fa"
	with open(fileName,"w") as f:
		f.write(seq)
		f.write('\n')
	return fileName 

def checkXML(fileName,reStr):
	blast = Bio.Blast.NCBIXML.parse(open(fileName,'rU'))
	num = 0
	for record in blast:
		num += len(record.alignments)
		for ali in record.alignments:
			reStr.append(ali.hit_def)
			for hsp in ali.hsps:
				reStr.append("   [%s/%s]  [%s-%s]"%(hsp.identities,hsp.align_length,hsp.sbjct_start,hsp.sbjct_end))
				reStr.append(hsp.query)
				reStr.append(hsp.match)
				reStr.append(hsp.sbjct)
				reStr.append(' ')

	return num

def rebuildDatabase():
	subprocess.call(blastCmd+"makeblastdb -in "+customDbFastaFileName+" -dbtype 'nucl' -out "+customDbName, shell=True);

def addToCustomDatabase(seqName, seq5,seq3):
	with open(customDbFastaFileName,'a') as f:
		f.write(">"+seqName+"-5"+"\n")
		f.write(seq5)
		f.write("\n\n")
		f.write(">"+seqName+"-3"+"\n")
		f.write(seq3)
		f.write("\n\n")
	rebuildDatabase()

def check53(seq5,seq3):
	
	reStr = []

	check(seq5,"m_code_5.xml",stdDbName)
	check(seq3,"m_code_3.xml",stdDbName)

	#checkXML
	hitTime = checkXML("m_code_5.xml",reStr)
	hitTime+= checkXML("m_code_3.xml",reStr)
	if hitTime > 0:
		reStr.append("there are %d hit(s) in the original database"%hitTime)
		return (False, reStr);
	else:
		reStr.append("not found in the original database.")
		
		check(seq5,"m_code_5.xml",customDbName)
		check(seq3,"m_code_3.xml",customDbName)

		hitTime = checkXML("m_code_5.xml",reStr)
		hitTime+= checkXML("m_code_3.xml",reStr)
		if hitTime > 0:
			reStr.append("there are %d hit(s) in the custom database"%hitTime)
			return (False,reStr)
		else:
			reStr.append("not found in the custom databse.")
			return (True,reStr)

def addNew(seqName,seq5,seq3):
	addToCustomDatabase(seqName,seq5,seq3)


def check(seq,xmlFileName,dbName):
	srcFileName = saveTempFile(seq)
	cline = Bio.Blast.Applications.NcbiblastnCommandline(cmd=blastCmd+"blastn", out=xmlFileName, outfmt=5, query=srcFileName, db=dbName)
	cline()

def getAllCustomDbNames(full = False):
	names = []
	cwd = os.getcwd();
	f = open(cwd+"/"+customDbFastaFileName,'r')
	while True:
		line = f.readline()
		if not line:
			break
		if len(line)>1 and line[0] == '>':
			names.append(line[1:])
			if full:
				l = f.readline()
				names[-1]+=" : "+l
	f.close()
	return names[1:]


def testC():
	seq5 = raw_input("seq 5': ")
	seq3 = raw_input("seq 3': ")
	result = check53(seq5,seq3)
	if result:
		yn = raw_input("add this sequence to custom database?(y/n):")
		if yn == 'y':
			seqName = raw_input("sequence name: ")
			addNew(seq5,seq3,seqName)

rebuildDatabase()
#testC()

def checkTRNA(id):
	names = getAllCustomDbNames()
	id5 = id+"-5"
	id3 = id+"-3"
	seq5 = ""
	seq3 = ""
	status = "not found"
	for i in range(0,len(names),3):
		if names[i].find(id5)>0:
			seq5 = names[i+1]  
			status = "found"
		elif names[i].find(id3)>0:
			seq3 = names[i+1]
			status = "found"
	return {"Status":status, "Seq5":seq5, "Seq3":seq3}

def matchTRNA(id,seq5,seq3):
	result = check53(seq5,seq3)[0]
	return {"Result":str(result)}

def appendTRNA(id,seq5,seq3):
	addToCustomDatabase(id,seq5,seq3);
	return {"Result":"OK"}

