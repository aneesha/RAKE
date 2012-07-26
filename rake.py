# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010). 
# Automatic keyword extraction from indi-vidual documents. 
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re

# Utility function to load stop words from a file and return as a list of words
# @param stopWordFile Path and file name of a file containing stop words.
# @return list A list of stop words.
def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        for word in line.split( ): #in case more than one per line
            stopWords.append(word)
    return stopWords

# Utility function to return a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def separatewords(text,minWordReturnSize):
	splitter=re.compile('[^a-zA-Z0-9_\\+\\-]')
	return [singleWord.lower() for singleWord in splitter.split(text) if len(singleWord)>minWordReturnSize]

# Utility function to return a list of sentences.
# @param text The text that must be split in to sentences.
def splitSentences(text):
	sentenceDelimiters = re.compile('[.!?,;]')
	sentenceList = sentenceDelimiters.split(text)
	return sentenceList

def buildStopwordRegExPattern(pathtostopwordsfile):
	stopwordlist = loadStopWords(stoppath)
	stopwordregexlist = []
	for wrd in stopwordlist:
		wrdregex = '\\b' + wrd + '\\b'
		stopwordregexlist.append(wrdregex)
	stopwordpattern = re.compile('|'.join(stopwordregexlist), re.IGNORECASE)
	return stopwordpattern

def generateCandidateKeywords(stopwordpattern):
	phraseList = []
	for s in sentenceList:
		tmp = re.sub(stopwordpattern, '|', s.strip())
		phrases = tmp.split("|")
		for phrase in phrases:
			phraseList.append(phrase);
	return phraseList

def calculateWordScores(phraseList):
	wordfreq = {}
	worddegree = {}
	for phrase in phraseList:
		wordlist = separatewords(phrase,0) 
		wordlistlength = len(wordlist)
		wordlistdegree = wordlistlength - 1
		for singleWord in wordlist:
			word = singleWord.lower().strip()
			if (word!=""):
				wordfreq.setdefault(word,0)
				wordfreq[word] += 1
				worddegree.setdefault(word,0)
				worddegree[word] += wordlistdegree
	for item in wordfreq:
		worddegree[item] = worddegree[item]+wordfreq[item] 	

	# Calculate Word scores = deg(w)/frew(w)
	wordscore = {}
	for item in wordfreq:
		wordscore.setdefault(item,0)
		wordscore[item] = worddegree[item]/(wordfreq[item] * 1.0)
	return wordscore
	
def generateCandidateKeywordScores(phraseList, wordscore):
	keywordcandidates = {}
	for phrase in phraseList:
		keywordcandidates.setdefault(phrase,0)
		wordlist = separatewords(phrase,0) 
		candidatescore = 0
		for singleWord in wordlist:
			word = singleWord.lower().strip()
			if (word!=""):
				candidatescore += wordscore[word]
		keywordcandidates[phrase] = candidatescore
	return keywordcandidates

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

# Split text into sentences
sentenceList = splitSentences(text)
stoppath = "englishstop.txt" 
stopwordpattern = buildStopwordRegExPattern(stoppath)

# generate candidate keywords
phraseList = generateCandidateKeywords(stopwordpattern)

# calculate individual word scores
wordscores = calculateWordScores(phraseList)

# generate candidate keyword scores
keywordcandidates = generateCandidateKeywordScores(phraseList, wordscores)

print keywordcandidates
