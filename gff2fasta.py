# TODO
# deal with introns

import re
import string
import sys
from collections import defaultdict

chromosomes = {};
reverseChromosomes = {};
features = [];
	
maxPromoterLength = 500;
maxTerminatorLength = 200;

# Feature class, represents all possible featurse imported in the GFF file
class Feature:
	def __init__(self, chromosome, source, feature, start, end, score, strand, frame, notes):

		# sets first few attributes
		self.chromosome = chromosome;
		self.source = source;
		self.feature = feature;
		self.start = int(start);
		self.end = int(end);
		self.score = score;
		self.strand = strand;
		self.frame = frame;
		self.notes = notes;

		# accounts for information provided in notes
		theNotes = notes.split(";");
		reID = re.compile("^ID=");
		reGene = re.compile("^gene=");
		reAlias = re.compile("^Alias=");
		reNote = re.compile("^Note=");
		reOrf = re.compile("^orf_classification=");


		for note in theNotes:
			if reID.match(note):
				self.id = note.split("^ID=")[-1];
			elif reGene.match(note):
				self.gene = note.split("^gene=")[-1];
			elif reAlias.match(note):
				self.alias = note.split("^Alias=")[-1];
			elif reNote.match(note):
				self.note = note.split("^Note=")[-1];
			elif reOrf.match(note):
				self.verification = note.split("^orf_classification=")[-1];

		return None;



	# allows for keeping track of the promoter coordinates through the feature object
	def setPromoter(self, start, end):
		self.promoterStart = start;
		self.promoterEnd = end;
		return self;



	# allows for keeping track of the terminator coordinates through the feature object
	def setTerminator(self, start, end):
		self.terminatorStart = start;
		self.terminatorEnd = end;
		return self;



# main method which imports and parses the GFF file and extracts the features and chromosomes
def parse():

	f = open('saccharomyces_cerevisiae.gff', 'r');

	count = 0;
	phase = 0;


	currentChromosomeId = "";
	currentChromosomeSeq = "";

	for line in f:
		line = line.rstrip('\n');
		
		if line == "###":
			phase = 2

		if line == "#":
			phase = 1;

		if phase == 1:
			words = line.split()
			if words[0][0] != '#':
				feature = Feature(words[0], words[1], words[2], words[3], words[4], words[5], words[6], words[7], words[8]);
				features.append(feature);
				#condense
				print "a";

		if phase == 2:
			if line != "##FASTA":
				if line[0] == ">":
					if currentChromosomeId != "":
						chromosomes[currentChromosomeId] = currentChromosomeSeq;
						reverseChromosomes[currentChromosomeId] = getReverseCompliment(currentChromosomeSeq);
					currentChromosomeId = line[1:];
					currentChromosomeSeq = "";
				else:
					currentChromosomeSeq = currentChromosomeSeq + line;

	if phase == 2:
		chromosomes[currentChromosomeId] = currentChromosomeSeq;
		reverseChromosomes[currentChromosomeId] = getReverseCompliment(currentChromosomeSeq);

	f.close();

	return None;



# gets the GCC content as a percentage of the whole sequence
def getGCContent(sequence):
	return len(re.findall("G|g|C|c", sequence))/len(sequence);



# calculates the melting temperature of a sequence
def getMeltingTemperature(sequence):
	gcContent = getGCContent(sequence);
	tm = 0;

	if len(sequence) <= 14:
		tm = 4 * len(sequence) * gcContent + 2 * len(sequence) * (1-gcContent);
	else:
		tm = 64.9 + 41 * (gcContent * len(sequence) - 16.4) / len(sequence);
	
	return tm;


# returns the reverse compliment of a sequence. requires the string library to be imported.
def getReverseCompliment(sequence):
	return sequence[::-1].translate(string.maketrans("AaTtCcGg", "TtAaGgCc"));



# gets an open reading frame's sequence from its chromosome
def getOrfSequence(feature):
	if feature.strand == "+":
		return chromosomes[feauture.chromosome][feature.start-1:feature.end-1];
	else:
		return reverseChromosomes[feauture.chromosome][feature.start-1:feature.end-1];


def saveFasta():
	print len(chromosomes); 
	with open('yeast.fa','w') as f:
		for name in chromosomes:
			f.write(">")
			f.write(name)
			f.write("\n")
			f.write(chromosomes[name])
			f.write("\n\n")
		print len(features);
		for feature in features:
			f.write(">")
			f.write(feature.feature+"|"+feature.notes)
			chromosomeID = feature.chromosome
			print chromosomeID
			chromosome = chromosomes[chromosomeID]
			a = feature.start if feature.start < feature.end else feature.end
			b = feature.end if feature.start < feature.end else feature.start

			f.write("\n")
			f.write(chromosome[a:b])
			f.write("\n")
			f.write("\n")
		

#actually calling the jim jams
parse();
saveFasta();

