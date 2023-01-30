import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

class TriesNode():
    def __init__(self, letter):
        self.letter = letter
        self.children = []
        self.lastLeaf = False

    def addChild(self, TrieNode):
        self.children.append(TrieNode)

class Tries():
    def __init__(self):
        self.root = TriesNode(None)

    def insert(self, key):
        currentLetter = self.root
        length = len(key)

        for i in range(length):
            found = False
            for j in range(len(currentLetter.children)):
                if (currentLetter.children[j].letter == key[i]):
                    nextLetter = currentLetter.children[j]
                    found = True
                    break

            if not found:
                nextLetter = TriesNode(key[i])
                currentLetter.addChild(nextLetter)
            currentLetter = nextLetter

        currentLetter.lastLeaf = True

    def search(self, text):
        currentLetter = self.root

        for i in range(len(text)):
            num=i
            for j in range(len(currentLetter.children)):
                if (text[i] == currentLetter.children[j].letter):
                    currentLetter = currentLetter.children[j]
                    break
                if (j == len(currentLetter.children)-1):
                    return False
            if currentLetter.lastLeaf == True and (num == len(text)-1):
                return True

        return False





def dictToListOfLists(dictionary: dict):
    listoflists = list(dictionary.items())
    return ([list(i) for i in listoflists])


def listofListstoDict(listoflists: list):
    listoflists = [tuple(i) for i in listoflists]
    return (dict(listoflists))


def print_hi(name):

    print(f'Hi, {name}')


class article():
    arraywords = []
    arraypos = []
    arrayneg = []
    arrayneutral = []
    arraystop = []
    positivetrie = Tries()
    negativetrie = Tries()
    stoptrie = Tries()
    company = None;
    allcomp = {}
    freqpos = {}
    freqneg = {}
    freqneutral = {}
    freqwords = {}



    def __init__(self, companyname):
        self.arraywords = []
        self.arraypos = []
        self.arrayneg = []
        self.arrayneutral = []
        self.arraystop = []
        self.positivetrie = Tries()
        self.negativetrie = Tries()
        self.stoptrie = Tries()
        self.readposnegstop()
        self.company = companyname
        self.freqwords = {}
        self.freqpos = {}
        self.freqneg = {}
        self.freqneutral = {}
        self.allcomp = {"citylink" : "City-Link Express",
                        "dhl" : "DHL",
                        "poslaju" : "Pos Laju",
                        "jnt" : "J&T Express",
                        "gdex" : "GDEX",}
        self.score = 0

    def readposnegstop(self):

        positive = open("positiveWords.txt", "r")
        fulltxt = positive.read()
        positive.close()
        fulltxt = fulltxt.lower()
        words = fulltxt.split(',  ')

        for word in words:
            self.positivetrie.insert(word)

        negative = open("negativeWords.txt", "r")
        fulltxt = negative.read()
        negative.close()
        fulltxt = fulltxt.lower()
        words = fulltxt.split(',    ')

        for word in words:
            self.negativetrie.insert(word)

        stop = open("stopword.txt", "r")
        fulltxt = stop.read()
        stop.close()
        fulltxt = fulltxt.lower()
        words = fulltxt.split('\n')

        for word in words:
            self.stoptrie.insert(word)


    def readtext(self, filenames):
        lines = [[],[],[]]
        words = []

        print("Company:", self.allcomp[self.company])

        i=0
        for filename in filenames:
            currwords = []
            currpos = []
            currneg = []
            currentpos = 0
            currentneg = 0
            currentword = 0


            file = open(filename, "r", encoding='latin-1')
            fulltxt = file.read()
            file.close()
            fulltxt = fulltxt.lower()
            characters = "!(+[])â€?@\"#”“’-,\'%.*&\\:|"
            for c in characters:
                fulltxt = fulltxt.replace(c, "")
            fulltxt = fulltxt.rstrip('\n')
            fulltxt = fulltxt.rstrip('\n\n')
            fulltxt = fulltxt.replace('\t', " ")

            words = fulltxt.split(' ')



            for word in words:
                word = word.replace("\n\n", "")
                word = word.replace("\x80\x99", "")
                if not self.stoptrie.search(word):
                    currentword += 1
                    currwords.append(word)
                    self.arraywords.append(word)

            for word in currwords:
                if (self.positivetrie.search(word)):
                    self.arraypos.append(word)
                    currentpos += 1
                elif (self.negativetrie.search(word)):
                    self.arrayneg.append(word)
                    currentneg += 1
                else:
                    self.arrayneutral.append(word)

            print("Statistics for Article", i+1)
            print("Number of words in article " + filename + ":", currentword)
            print("Number of positive words in article " + filename + ":", currentpos)
            print("Number of negative words in article " + filename + ":", currentneg)
            print()

            i+=1


        print("Collective Statistics for", self.allcomp[self.company] )
        print("Number of words in given articles (Excluding Stop words):",self.arraywords.__len__())
        print("Number of positive words in given articles:",self.arraypos.__len__())
        print("Number of negative words in given articles:",self.arrayneg.__len__())
        print("Number of neutral words in given articles:",self.arrayneutral.__len__())
        print("Final score based on articles:", self.calcscore())


    def wordfreq(self):
        self.freqwords = Counter(self.arraywords)
        self.freqwords = dict(self.freqwords)

        self.freqpos = Counter(self.arraypos)
        self.freqpos = dict(self.freqpos)

        self.freqneg = Counter(self.arrayneg)
        self.freqneg = dict(self.freqneg)

        self.freqneutral = Counter(self.arrayneutral)
        self.freqneutral = dict(self.freqneutral)
        print()


    def plothisto6(self):
        freqwords = self.freqwords
        freqwords = {k:v for k,v in sorted(freqwords.items(), key = lambda v: v[1], reverse = True)}

        freqwords = dictToListOfLists(freqwords)



        left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


        height = [freqwords[0][1], freqwords[1][1], freqwords[2][1], freqwords[3][1], freqwords[4][1], freqwords[5][1], freqwords[6][1], freqwords[7][1], freqwords[8][1], freqwords[9][1]]


        tick_label = [freqwords[0][0], freqwords[1][0], freqwords[2][0], freqwords[3][0], freqwords[4][0], freqwords[5][0], freqwords[6][0], freqwords[7][0], freqwords[8][0], freqwords[9][0]]


        plt.bar(left, height, tick_label=tick_label,
                width=0.5, color=['red'])


        plt.xlabel('Words')

        plt.ylabel('Occurences')

        plt.title("Bar chart for " + self.allcomp[self.company] + "")

        plt.show()



    def calcscore(self):
        pos = self.arraypos.__len__()
        neg = self.arrayneg.__len__()
        tot = self.arraypos.__len__() + self.arrayneg.__len__()

        self.score = round((((pos - 0.5*neg) / tot) * 5), 3)

        return self.score


def plothisto8(citylink, dhl, poslaju, jnt, gdex):

    barWidth = 0.25

    POS = [citylink.arraypos.__len__(), dhl.arraypos.__len__(), poslaju.arraypos.__len__(), jnt.arraypos.__len__(), gdex.arraypos.__len__()]
    NEG = [citylink.arrayneg.__len__(), dhl.arrayneg.__len__(), poslaju.arrayneg.__len__(), jnt.arrayneg.__len__(), gdex.arrayneg.__len__()]

    br1 = np.arange(len(POS))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, POS, color='g', width=barWidth,
            edgecolor='grey', label='Positive')
    plt.bar(br2, NEG, color='r', width=barWidth,
            edgecolor='grey', label='Negative')

    for index, data in enumerate(POS):
        plt.text(x=index, y=data + 1, s=f"{data}", fontdict=dict(fontsize=10), ha='center')
    for index, data in enumerate(NEG):
        plt.text(x=index + 0.25, y=data + 1, s=f"{data}", fontdict=dict(fontsize=10), ha='center')

    plt.xlabel('Courier Company', fontweight='bold', fontsize=15)
    plt.ylabel('Number of Words', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(POS))],
               ['City-Link', 'DHL', 'Pos Laju', 'J&T Express', 'GDEX'])

    plt.legend()
    plt.show()
    return


def plothisto6wc(citylink, dhl, poslaju, jnt, gdex):

    barWidth = 0.25

    POS = [citylink.arraywords.__len__(), dhl.arraywords.__len__(), poslaju.arraywords.__len__(), jnt.arraywords.__len__(), gdex.arraywords.__len__()]

    br1 = np.arange(len(POS))

    plt.bar(br1, POS, color='g', width=barWidth,
            edgecolor='grey', label='')

    for index, data in enumerate(POS):
        plt.text(x=index, y=data + 10, s=f"{data}", fontdict=dict(fontsize=10), ha='center')
    plt.xlabel('Courier Company', fontweight='bold', fontsize=15)
    plt.ylabel('Number of Words', fontweight='bold', fontsize=15)
    plt.xticks(br1,
               ['City-Link', 'DHL', 'Pos Laju', 'J&T Express', 'GDEX'])

    plt.show()
    return


def sentimentscore(citylink, dhl, poslaju, jnt, gdex):
    score = {citylink.company : citylink.score,
             dhl.company : dhl.score,
             poslaju.company : poslaju.score,
             jnt.company : jnt.score,
             gdex.company : gdex.score}

    return score

