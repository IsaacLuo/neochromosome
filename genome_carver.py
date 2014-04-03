# TODO
# deal with introns

import re
import string
import sys
from collections import defaultdict

chromosomes = {};
reverseChromosomes = {};

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
        for note in theNotes:
            if note.match("^ID="):
                self.id = note.split("^ID=")[-1];
            elif note.match("^gene="):
                self.gene = note.split("^ID=")[-1];
            elif note.match("^Alias="):
                self.alias = note.split("^ID=")[-1];
            elif note.match("^Note="):
                self.note = note.split("^ID=")[-1];
            elif note.match("^orf_classification="):
                self.verification = note.split("^ID=")[-1];

        return self;



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

    features = [];

    currentChromosomeId = "";
    currentChromosomeSeq = "";

    for line in f:
    	line = line.rstrip('\n');
        
        if line == "###":
            phase = 2;

        if phase == 1:
            words = line.split();
            if words[0][0] != '#':
                feature = Feature(words[0], words[1], words[2], words[3], words[4], words[5], words[6], words[7]);
                features.append(feature);
                #condense

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

    return;



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



def getPromoterSequence(feature):
    tempStart = feature.start - maxPromoterLength;

    for f in features where f.chromosome == feature.chromosome and f.strand == feature.strand:
	#for f in (ff for ff in features if ff.chromosome == feature.chromosome and ff.strand == feature.strand):
        if f.start < feature.start and f.start > tempStart and f.end > feature.start:
            return "";
        elif f.start < feature.start and f.end > tempStart and f.end < feature.start:
            tempStart = f.end + 1;

    if feature.strand == "+":
        return chromosomes[feature.chromosome][tempStart-1:feature.start-2];
    else:
        return reverseChromosomes[feature.chromosome][tempStart-1:feature.start-2];



def getTerminatorSequence(feature):
    tempEnd = feature.end + maxTerminatorLength;

    for f in features where f.chromosome == feature.chromosome and f.strand == feature.strand:
        if feature.end > f.start and feature.end < f.end:
            return "";
        elif feature.end < f.start and tempEnd > f.start:
            tempEnd = f.start - 1;

    if feature.strand == "+":
        return chromosomes[feature.chromosome][tempStart-1:feature.start-2];
    else:
        return reverseChromosomes[feature.chromosome][tempStart-1:feature.start-2];



#get command line arguments for promoter/terminator lengths
if str(sys.argv)[0]:
    maxPromoterLength = int(str(sys.argv)[0]);

if str(sys.argv)[1]:
    maxTerminatorLength = int(str(sys.argv)[1]);

#actually calling the jim jams
parse();
