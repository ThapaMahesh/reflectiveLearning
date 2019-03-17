import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import re

class PreProcess:
    text = ""
    norks = False
    allWordList = []
    stopWordList = []
    def __init__(self, text, norsk):
        self.text = text
        self.norsk = norsk

    def getWordList(self, text, stop, splitHyphen=False):
        wordList = self.text.split()
        punctuationList = """!"#$%*+,.:;<=>?@^_`{|}~"""
        punctuationMap = str.maketrans('', '', punctuationList)
        stripped = [w.translate(punctuationMap) for w in wordList]

        # replace ()/ with spliting the word and add to the main list
        # strip '"- from start or end of the word.
        newList = []
        parenRegex = r"\(?.*?\)?"
        bothAposRegex = r"(\"?.*?\"?)|(\'?.*?\'?)"
        for eachWord in stripped:
            eachNoBrackList = re.compile('[\[\]\(\)—/]').split(eachWord)
            for listword in eachNoBrackList:
                eachNoQuoteWord = listword.strip("\'|\"|\”|\“|\’")
                eachNoQuoteWord = eachNoQuoteWord.replace("\’", "\'")
                eachNoHyphenWord = eachNoQuoteWord.strip("\-|\–")
                if splitHyphen and "-" in eachNoHyphenWord:
                    hyphenList = [word if word.isupper() else word.lower() for word in eachNoHyphenWord.split('-')]
                    newList = newList + hyphenList
                elif eachNoHyphenWord != "":
                    newList.append(eachNoHyphenWord if eachNoHyphenWord.isupper() else eachNoHyphenWord.lower())

        wordTag = nltk.pos_tag(newList)
        self.allWordList = newList

        if self.norsk:
            usefulWords = [word for word in newList if word.lower() not in stopwords.words("norwegian")]
        else:
            usefulWords = [word for word in newList if word.lower() not in stopwords.words("english")]
        self.stopWordList = usefulWords
        if stop:
            return usefulWords
        else:
            return newList

    def wordFrequency(self):
        # wordList = self.getWordList(True)
        # lemmaWordList = self.lemmatizeSentence(wordList)
        frequencyList = FreqDist(self.stopWordList).most_common(100)
        # frequencyList = {}
        # for word in lemmaWordList:
        #     if word in frequencyList.keys():
        #         frequencyList[word] += 1
        #     else:
        #         frequencyList[word] = 1
        return frequencyList

    def sentiment(self):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(self.text)

    def getNumericData(self):
        sentences = sent_tokenize(self.text)
        wordList = self.getWordList(self.text, False)
        # onlyWord = [word[0] for word in wordList]
        uniquWords = set(wordList)
        noOfSentences = len(sentences)
        noOfWords = len(wordList)
        noOfUniqueWords = len(uniquWords)
        noOfCharacters = 0
        longSentence = 0
        # for word in wordList:
        noOfCharacters = len(self.text.strip(" "))

        for sentence in sentences:
            if len(sentence.split()) > 20:
                longSentence += 1

        avgLetters = (noOfCharacters/noOfWords)*100
        avgSentences = (noOfSentences/noOfWords)*100
        lexicalDiversity = (noOfUniqueWords/noOfWords)*100

        return {
            "noOfWords": noOfWords,
            "noOfSentences": noOfSentences,
            "noOfCharacters": noOfCharacters,
            "avgLetters": avgLetters,
            "avgSentences": avgSentences,
            "noOfUniqueWords": noOfUniqueWords,
            "lexicalDiversity": lexicalDiversity,
            "longSentence": longSentence
        }


    def complexity(self):
        stats = self.getNumericData()
        ari = 4.71*(stats["noOfCharacters"]/stats["noOfWords"]) + 0.5*(stats["noOfWords"]/stats["noOfSentences"]) - 21.43
        gradeAri = self.ariGrade(ari)
        cli = 0.0588*stats["avgLetters"] - 0.296*stats["avgSentences"] - 15.8
        gradeCli = self.cliGrade(cli)
        return {
            "ARI": ari,
            "gradeAri": gradeAri,
            "CLI": cli,
            "gradeCli": gradeCli,
            "stats": stats
        }


    def ariGrade(self, ari):
        roundValue = round(ari)
        if roundValue == 1:
            return "Kindergarten"
        elif roundValue == 2:
            return "1st-2nd"
        elif roundValue >= 14:
            return "Graduate"
        elif roundValue >= 13:
            return "College Student"
        else:
            return str(roundValue) + "th"


    def cliGrade(self, cli):
        cliValue = round(cli)
        if cliValue == 1:
            return "1st"
        elif cliValue == 2:
            return "2nd"
        elif cliValue > 16:
            return "Graduate"
        elif cliValue >= 13:
            return "College Student"
        else:
            return str(cliValue) + "th"