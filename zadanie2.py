import sys
import time
import unicodedata


def EditDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):

            if i == 0:
                dp[i][j] = j

            elif j == 0:
                dp[i][j] = i

            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            else:
                dp[i][j] = 1 + min(dp[i][j - 1],
                                   dp[i - 1][j],
                                   dp[i - 1][j - 1])

    return dp[m][n]


def lcSubstring(X, Y, m, n):
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    result = 0

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                result = max(result, dp[i][j])
            else:
                dp[i][j] = 0
    return result


def lcSubsequence(X, Y):
    m = len(X)
    n = len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def readDictionary(filename):
    # f = open(filename, "r")
    f = open(filename, "r", encoding='utf-8-sig')
    lines = f.read().splitlines()
    dictionary = list()
    for line in lines:
        dictionary.append(line)
    return dictionary


def readFile(filename):
    f = open(filename, "r", encoding='ansi')
    text = list()
    for line in f:
        for word in line.split():
            text.append(word.lower())
    f.close()
    return text


def compareText(textFixedByAlgo, textFixed):
    print(f"Algo fix: {len(textFixedByAlgo)} \nFixed text: {len(textFixed)}")
    correctWord = 0
    incorrectWord = 0
    for i in range(len(textFixedByAlgo)):
        try:
            if textFixedByAlgo[i].lower() == textFixed[i].lower():
                correctWord += 1
            else:
                incorrectWord += 1
        except IndexError:
            break
    print(
        f"Correct words: {correctWord}, incorrect words: {incorrectWord}, percentage: {(correctWord / len(textFixedByAlgo)) * 100}%\n")


class DistanceWord:
    def __init__(self, word=None, distance=None):
        self.word = word
        self.distance = distance


class SubsequenceWord:
    def __init__(self, word=None, number=None):
        self.word = word
        self.number = number

    def __str__(self):
        return str(self.word)


def editDistanceSolver(dictionary, text):
    tmp: DistanceWord() = list()
    minDistance: DistanceWord() = list()
    finalArray: DistanceWord() = list()
    index = 0
    for word in text:
        index += 1
        word = unicodedata.normalize('NFD', word).encode('ascii',
                                                         'ignore').decode(
            "utf-8")
        if word not in dictionary:
            for dic in dictionary:
                distanceWord = DistanceWord()
                distance = EditDistDP(word, dic, len(word), len(dic))
                distanceWord.distance = distance
                distanceWord.word = dic
                tmp.append(distanceWord)
            minDistance.append(min(tmp, key=lambda x: x.distance))
            finalArray.append(minDistance[0].word)
            print(
                f"{index}: {word} -> {minDistance[0].word}\t distance: {minDistance[0].distance}")
            minDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
            print(f"{index}: {word}")
    return finalArray


def substringSolver(dictionary, text):
    tmp: DistanceWord() = list()
    maxDistance: DistanceWord() = list()
    finalArray: DistanceWord() = list()
    index = 0
    for word in text:
        index += 1
        word = unicodedata.normalize('NFD', word).encode('ascii',
                                                         'ignore').decode(
            "utf-8")
        if word not in dictionary:
            for dic in dictionary:
                X = word
                Y = dic
                n = len(X)
                m = len(Y)
                dst = lcSubstring(X, Y, n, m)
                tmp.append(DistanceWord(Y, dst))
            maxDistance.append(max(tmp, key=lambda x: x.distance))
            finalArray.append(maxDistance[0].word)
            print(
                f"{index}: {word} -> {maxDistance[0].word}\t substring length: {maxDistance[0].distance}")
            maxDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
            print(f"{index}: {word}")
    return finalArray


def subsequenceSolver(dictionary, text):
    tmp: DistanceWord() = list()
    maxDistance: DistanceWord() = list()
    finalArray: DistanceWord() = list()
    index = 0
    for word in text:
        index += 1
        word = unicodedata.normalize('NFD', word).encode('ascii',
                                                         'ignore').decode(
            "utf-8")
        if word not in dictionary:
            for dic in dictionary:
                X = word
                Y = dic
                dst = lcSubsequence(X, Y)
                tmp.append(DistanceWord(Y, dst))
            maxDistance.append(max(tmp, key=lambda x: x.distance))
            finalArray.append(maxDistance[0].word)
            print(
                f"{index}: {word} -> {maxDistance[0].word}\t subsequence length: {maxDistance[0].distance}")
            maxDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
            print(f"{index}: {word}")
    return finalArray


if __name__ == '__main__':
    dictionary = readDictionary("slovnik.txt")

    if sys.argv[1] == 'compare' and len(sys.argv) == 4:
        message = readFile(sys.argv[2])
        textCorrectByAlgo = readFile(sys.argv[3])
        compareText(textCorrectByAlgo, message)

    if sys.argv[1] == 'dst' and len(sys.argv) == 4:
        text = readFile(sys.argv[2])
        f_edit = open(sys.argv[3], "w")
        start1 = time.time()
        finalArray = editDistanceSolver(dictionary, text)
        end1 = time.time()
        output = " ".join([str(x) for x in finalArray])
        f_edit.write(output)
        f_edit.close()
        print(f"Time to run: {end1 - start1}")

    if sys.argv[1] == 'substr' and len(sys.argv) == 4:
        text = readFile(sys.argv[2])
        f_substring = open(sys.argv[3], "w")
        start2 = time.time()
        finalArray = substringSolver(dictionary, text)
        end2 = time.time()
        output = " ".join([str(x) for x in finalArray])
        f_substring.write(output)
        f_substring.close()
        print(f"Time to run: {end2 - start2}")

    if sys.argv[1] == 'subseq' and len(sys.argv) == 4:
        text = readFile(sys.argv[2])
        f_subsequence = open(sys.argv[3], "w")
        start3 = time.time()
        finalArray = subsequenceSolver(dictionary, text)
        end3 = time.time()
        output = " ".join([str(x) for x in finalArray])
        f_subsequence.write(output)
        f_subsequence.close()
        print(f"Time to run: {end3 - start3}")
