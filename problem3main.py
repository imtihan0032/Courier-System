import numpy as np
import matplotlib.pyplot as plt
import problem1
import problem2
import problem4
import wave
import webbrowser

allcomp = {"citylink" : "City-Link Express",
                        "dhl" : "DHL",
                        "poslaju" : "Pos Laju",
                        "jnt" : "J&T Express",
                        "gdex" : "GDEX",}

def dictToListOfLists(dictionary: dict):
    listoflists = list(dictionary.items())
    return ([list(i) for i in listoflists])


def listofListstoDict(listoflists: list):
    listoflists = [tuple(i) for i in listoflists]
    return (dict(listoflists))

def totalscores(distance_dict, sentiment_dict):
    totalscore = {'citylink': 0, 'dhl': 0, 'poslaju': 0, 'jnt': 0, 'gdex': 0}
    couriers = dictToListOfLists(distance_dict)
    for i in range(len(totalscore)):
        name = couriers[i][0]
        totalscore[name] = distance_dict[name]*0.5 + sentiment_dict[name]*0.5
    return totalscore

MIN_MERGE = 32

def calculate_min_run(num):
    run = 0
    while (num >= MIN_MERGE):
        run |= num & 1
        num >>= 1
    return num + run


def timSort(dict):

    num = len(dict)
    minimum_run = calculate_min_run(num)


    for start in range(0, num, minimum_run):
        end = min(start + minimum_run - 1, num -1)
        insertion_sort_dict(dict, start, end)


    size = minimum_run
    while size < num:
        for left in range(0, num, 2 * size):
            middle = min(num-1, left + size - 1)
            right = min((left + 2 * size -1),(num - 1))

            if middle < right:
                merge(dict, left, middle, right)

        size = 2 * size
    return dict

def insertion_sort_dict(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while (j > left and arr[j][1] > arr[j - 1][1]):
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1


def merge(arr, left, middle, right):
    len1 = middle - left + 1
    len2 = right - middle
    left = []
    right = []

    for i in range(0, len1):
        left.append(arr[left + i])
    for i in range(0, len2):
        right.append(arr[middle + 1 + i])

    i, j, k = 0, 0, left

    while i < len1 and j < len2:

        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1


    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1

    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1


if __name__ == '__main__':

    print("Initialising.....")
    print("=================================================================================Courier System================================================================================")
    print()

    print("=================================================================================Distance Analysis================================================================================")
    print()

    '''#Customer 1
    customer1hlat = "3.3615395462207878"
    customer1hlong = "101.56318183511695"
    customer1dlat = "3.1000170516638885"
    customer1dlong = "101.53071480907951"'''

    '''# Customer 2
    customer1hlat = "3.048398375759954"
    customer1hlong = "101.58546611160301"
    customer1dlat = "3.227994355250716"
    customer1dlong = "101.42730357605375"'''



    # Customer 3
    customer1hlat = "3.141855957281073"
    customer1hlong = "101.76158583424586"
    customer1dlat = "2.9188704151716256"
    customer1dlong = "101.65251821655471"



    customer1home = problem1.geolocator.reverse((customer1hlat + " , " + customer1hlong))
    customer1dest = problem1.geolocator.reverse((customer1dlat + " , " + customer1dlong))


    print("The home address is: " + customer1home.address)
    print("The destination address is: " + customer1dest.address)
    c = problem1.Customer()
    # c.sethomedest("Jalan 17/2, Section 17, Petaling Jaya, Petaling, Selangor, 47350, Malaysia", "Bangsar South, Pantai Dalam, Kuala Lumpur, 59200, Malaysia")
    c.sethomedest((customer1home.address), (customer1dest.address))
    c.finddirectdistance()
    c.printalldistances()
    c.setpointsfordelivery()
    c.printmap()
    c.initgraph()
    print()
    c.getrankfinal()

    webbrowser.open('maphubs.html')
    webbrowser.open('mapdeliverypath.html')

    inp = input("Press any key to continue...")

    print("=================================================================================Article Analysis================================================================================")
    print()

    citylinkfiles = ["citylink.txt", "citylink2.txt", "citylink3.txt"]
    citylink = problem2.article("citylink")
    citylink.readtext(citylinkfiles)
    citylink.wordfreq()
    citylink.plothisto6()
    print("===================================================================================================================================================================================")
    # print(citylink.score)

    dhlfiles = ["dhl1.txt", "dhl2.txt", "dhl3.txt"]
    dhl = problem2.article("dhl")
    dhl.readtext(dhlfiles)
    dhl.wordfreq()
    dhl.plothisto6()
    print("===================================================================================================================================================================================")
    # print(dhl.score)

    poslajufiles = ["poslaju1.txt", "poslaju2.txt", "poslaju3.txt"]
    poslaju = problem2.article("poslaju")
    poslaju.readtext(poslajufiles)
    poslaju.wordfreq()
    poslaju.plothisto6()
    print("===================================================================================================================================================================================")
    # print(poslaju.score)

    jntfiles = ["jnt1.txt", "jnt2.txt", "jnt3.txt"]
    jnt = problem2.article("jnt")
    jnt.readtext(jntfiles)
    jnt.wordfreq()
    jnt.plothisto6()
    print("===================================================================================================================================================================================")
    # print(jnt.score)

    gdexfiles = ["gdex1.txt", "gdex2.txt", "gdex3.txt"]
    gdex = problem2.article("gdex")
    gdex.readtext(gdexfiles)
    gdex.wordfreq()
    gdex.plothisto6()
    print("===================================================================================================================================================================================")
    # print(gdex.score)

    problem2.plothisto6wc(citylink, dhl, poslaju, jnt, gdex)
    problem2.plothisto8(citylink, dhl, poslaju, jnt, gdex)


    inp = input("Press any key to continue...")

    print("=================================================================================Final Analysis================================================================================")
    print()




    scoredistance = c.getrankfinal()
    scoresentiment = problem2.sentimentscore(citylink, dhl, poslaju, jnt, gdex)

    sort_distance = timSort(dictToListOfLists(scoredistance))
    sort_sentiment = timSort(dictToListOfLists(scoresentiment))

    final = totalscores(scoredistance, scoresentiment)
    final = timSort(dictToListOfLists(final))

    totallist = [round(scoredistance[final[0][0]] + scoresentiment[final[0][0]], 3),
                 round(scoredistance[final[1][0]] + scoresentiment[final[1][0]], 3),
                 round(scoredistance[final[2][0]] + scoresentiment[final[2][0]], 3),
                 round(scoredistance[final[3][0]] + scoresentiment[final[3][0]], 3),
                 round(scoredistance[final[4][0]] + scoresentiment[final[4][0]], 3)]

    print("Best Courier based on Distance:", allcomp[sort_distance[0][0]], "  Score: ", scoredistance[sort_distance[0][0]])
    print("Best Courier based on Sentiment:", allcomp[sort_sentiment[0][0]], "  Score: ", scoresentiment[sort_sentiment[0][0]])
    print("Best Courier based on both Distance & Sentiment:", allcomp[final[0][0]], "  Score: ", totallist[0])


    # print(final)

    N = 5

    Distance = (
    scoredistance[final[0][0]], scoredistance[final[1][0]], scoredistance[final[2][0]], scoredistance[final[3][0]],
    scoredistance[final[4][0]])
    Sentiment = (
    scoresentiment[final[0][0]], scoresentiment[final[1][0]], scoresentiment[final[2][0]], scoresentiment[final[3][0]],
    scoresentiment[final[4][0]])
    ind = np.arange(N)
    width = 0.35

    fig = plt.subplots(figsize=(10, 7))
    p1 = plt.bar(ind, Distance, width)
    p2 = plt.bar(ind, Sentiment, width, bottom=Distance)

    for index, data in enumerate(totallist):
        plt.text(x=index, y=data + 0.25, s=f"{data}", fontdict=dict(fontsize=10), ha='center')

    plt.ylabel('Score')
    plt.title('List of Couriers')
    plt.xticks(ind, (
    allcomp[final[0][0]], allcomp[final[1][0]], allcomp[final[2][0]], allcomp[final[3][0]], allcomp[final[4][0]],))
    plt.yticks(np.arange(0, 11, 1))
    plt.legend((p1[0], p2[0]), ('Distance Score', 'Sentiment Score'))

    plt.show()

    print()
    print("=================================================================================DTW Analysis================================================================================")
    print()

    jnt = wave.open("sample.wav", "r")
    jntsoundwave = jnt.readframes(-1)

    random = wave.open("random word.wav", "r")
    randomwave = random.readframes(-1)

    jnt_slow = wave.open("sample05.wav", "r")
    jntsoundwaveslow = jnt_slow.readframes(-1)

    jnt_fast = wave.open("sample15.wav", "r")
    jntsoundwavefast = jnt_fast.readframes(-1)

    jnt_fast2 = wave.open("sample20.wav", "r")
    jntsoundwavefast2 = jnt_fast2.readframes(-1)


    print("Resultant DTW matrix between sample and changed word")
    print(problem4.dtw(jntsoundwave[:1000], randomwave[:1000]))
    print()
    print("Resultant DTW matrix between sample and slowed word")
    print(problem4.dtw(jntsoundwave[:1000], jntsoundwaveslow[:1000]))
    print()
    print("Resultant DTW matrix between same words")
    print(problem4.dtw(jntsoundwave[:1000], jntsoundwave[:1000]))
    print()
    print("Resultant DTW matrix between sample and 1.5 word")
    print(problem4.dtw(jntsoundwave[:1000], jntsoundwavefast[:1000]))
    print()
    print("Resultant DTW matrix between sample and 2.0 word")
    print(problem4.dtw(jntsoundwave[:1000], jntsoundwavefast2[:1000]))
    print()
