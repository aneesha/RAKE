# -*- coding: utf-8 -*-
# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010). 
# Automatic keyword extraction from indi-vidual documents. 
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re
import operator

debug = False
test = True


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\-\\"\\(\\)\\\'\u2019\u2013]')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = '\\b' + word + '\\b'
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path):
        self.stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stoppath)

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords


if test:
    text = """
    Have you ever wondered why selfish, arrogant, and entitled individuals are so charming? These narcissistic people have parasitic effects on society. When in charge of companies they commit fraud, demoralize employees, and devalue stock. When in charge of countries they increase poverty, violence, and death rates.

And yet, there is no shortage of examples to illustrate the cultural appeal of narcissistic antiheroes, whether fictional (Walter White of Breaking Bad; Batman, and James Bond), all-too real (Silvio Berlusconi, Steve Jobs, Kanye West, and too many professional athletes to name), or a mix of both, such as the so-called Wolf of Wall Street. We are attracted to them despite their self-absorption — or perhaps, even because of it.
Why?
After decades of scientific research, psychologists have begun to deconstruct the seductive power of narcissists, explaining the precise mechanisms underlying their charm and ability to get ahead in all domains of life. Here are the key findings:
1. Narcissists are masterful impression managers: Thanks largely to their intense self-obsession and self-adulation, narcissists excel at managing initial impressions. They care a lot about their appearance and dress to impress, which signals status and makes them attractive. As Kaiser and Craig note in a recent review (“Destructive leadership in and of organizations”), “it is the obsessive focus on the self that links the narcissistic personality with charisma.” Furthermore, narcissists’ desire to make a great initial impression enables them to disguise their arrogance as confidence, which they often achieve through humor and by being entertaining or eccentric. Unsurprisingly, narcissists perform well on interviews and they are excellent social networkers – you can even spot them by their social media activity (e.g., more Twitter followers, Facebook friends, or a higher Klout score).
2. Narcissists manipulate credit and blame in their favor: Through a mix of shameless self-promotion and a guilt-free, Machiavellian agenda, narcissists are quick to take credit for others’ achievements and blame colleagues and subordinates for their own failures. As Ben Dattner notes, narcissistic managers “lead with the main purpose of receiving personal credit or glory. When things go wrong or they make mistakes, they deny or distort information and ‘rewrite history’ in order to avoid getting blamed.” What makes narcissists so effective at this is their complete conviction that they are actually special. In Dattner’s words: “they believe that they deserve credit for simply being who they are, regardless of their actual contributions or achievements.” Such delusions of grandeur allow narcissists to be more effective manipulators than individuals who are politically savvy but inhibited by their inability to distort reality or morality in their favor. It is always easier to fool others when you have already fooled yourself; it is always harder to feel guilty when you think you are innocent.
3. Narcissists fit conventional stereotypes of leadership: Because of their ability to accumulate power and influence, narcissists enjoy a prominent spot in laypeople’s views about leadership. However, the idea that leaders must be overconfident, charismatic, or selfish in order to be effective is in stark contrast with reality. Yes, these characteristics help them emerge as leaders, but they are also the cause of their dishonest and incompetent behaviors once they get to the top. Whether in sports, business, education or politics, effective leadership requires building high-performing teams and, when it comes to that, the critical ingredients for success are competence rather than confidence, altruism rather than egotism, and integrity rather than charisma. In other words, the real essence of good leadership is the exact opposite of what the Hollywood version of leadership implies. Until we understand this, we will unfortunately continue to invite narcissists to the top while overlooking more competent and healthier alternatives. In Eastern and collectivistic cultures narcissism rates are lower because society condemns it – we should follow that model in the West.
Importantly, there are different degrees of narcissism and, though we tend to use the term categorically, it is more appropriate to refer to people as either more or less narcissistic. In fact, some people may display relatively benign levels of narcissism, while others may resemble true psychopaths.
Interestingly, a small degree of narcissism may not be detrimental for leadership, at least in corporate America. In a recent meta-analytic study, managers with moderate narcissism scores did tend to outperform not only managers with high, but also low, rates of narcissism. This finding reminds us of some of the bright side characteristics associated with narcissistic leadership, such as effective communication skills, strategic vision, and ambition. No wonder we find narcissistic people appealing, despite themselves. However, if such competencies can also be found in non-narcissistic individuals – and they can – the derailment risks will decrease.
It is useful to recall one of the unique characteristics of narcissistic individuals, which is their inability to prolong their seductive powers for too long. Much like crack cocaine, the charm of narcissists produces an intense but short-lived high; and, unlike crack cocaine, it is far from addictive, except for narcissists themselves. As a seminal study in this area showed, the charisma of narcissists wears off after a mere 2.5 hours. Their initial flamboyance, charm and confidence soon morphs into deluded self-admiration, defensive arrogance, and moral disengagement. It is this rapid expiry date of narcissistic charms, which keeps narcissists always on the hunt for new fans — or victims.
So, when dealing with charismatic individuals, a good rule of thumb is to delay making decisions — whether to hire that person, promote them, or take them on as clients — until you work out who they really are. Not all charismatic people are narcissistic, but many narcissists are charismatic, and the more charismatic they are, the more time it takes to spot them.
    """

    # Split text into sentences
    sentenceList = split_sentences(text)
    #stoppath = "FoxStoplist.txt" #Fox stoplist contains "numbers", so it will not find "natural numbers" like in Table 1.1
    stoppath = "SmartStoplist.txt"  #SMART stoplist misses some of the lower-scoring keywords in Figure 1.5, which means that the top 1/3 cuts off one of the 4.0 score words in Table 1.1
    stopwordpattern = build_stop_word_regex(stoppath)

    # generate candidate keywords
    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

    # calculate individual word scores
    wordscores = calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    if debug: print keywordcandidates

    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    if debug: print sortedKeywords

    totalKeywords = len(sortedKeywords)
    if debug: print totalKeywords
    print sortedKeywords[0:(totalKeywords / 3)]

    print "-------------------------------"
    rake = Rake("SmartStoplist.txt")
    keywords = rake.run(text)
    print keywords
