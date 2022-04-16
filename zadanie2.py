# A Space efficient Dynamic Programming
# based Python3 program to find minimum
# number operations to convert str1 to str2
import time


def EditDistDP(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    # Create a DP array to memoize result
    # of previous computations
    DP = [[0 for i in range(len1 + 1)]
          for j in range(2)]

    # Base condition when second String
    # is empty then we remove all characters
    for i in range(0, len1 + 1):
        DP[0][i] = i

    # Start filling the DP
    # This loop run for every
    # character in second String
    for i in range(1, len2 + 1):

        # This loop compares the char from
        # second String with first String
        # characters
        for j in range(0, len1 + 1):

            # If first String is empty then
            # we have to perform add character
            # operation to get second String
            if j == 0:
                DP[i % 2][j] = i

            # If character from both String
            # is same then we do not perform any
            # operation . here i % 2 is for bound
            # the row number.
            elif str1[j - 1] == str2[i - 1]:
                DP[i % 2][j] = DP[(i - 1) % 2][j - 1]

            # If character from both String is
            # not same then we take the minimum
            # from three specified operation
            else:
                DP[i % 2][j] = (1 + min(DP[(i - 1) % 2][j],
                                        min(DP[i % 2][j - 1],
                                            DP[(i - 1) % 2][j - 1])))

    # After complete fill the DP array
    # if the len2 is even then we end
    # up in the 0th row else we end up
    # in the 1th row so we take len2 % 2
    # to get row
    return DP[len2 % 2][len1]


def lcSubstring(s, t, n, m):
    # Create DP table
    dp = [[0 for i in range(m + 1)] for j in range(2)]
    res = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i % 2][j] = dp[(i - 1) % 2][j - 1] + 1
                if dp[i % 2][j] > res:
                    res = dp[i % 2][j]
            else:
                dp[i % 2][j] = 0
    return res


def lcSubsequence(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[0] * (n + 1) for _ in range(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]


def readDictionary(filename):
    # f = open(filename, "r")
    f = open(filename, "r", encoding='utf-8-sig')
    lines = f.read().splitlines()
    dictionary = list()
    for line in lines:
        dictionary.append(line)
    return dictionary


def readFile(filename):
    f = open(filename, "r")
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
    print(f"Correct words: {correctWord}, incorrect words: {incorrectWord}\n")


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
    index = 1
    for word in text:
        print(index)
        index += 1
        if word not in dictionary:
            for dic in dictionary:
                distanceWord = DistanceWord()
                distance = EditDistDP(word, dic)
                distanceWord.distance = distance
                distanceWord.word = dic
                tmp.append(distanceWord)
            minDistance.append(min(tmp, key=lambda x: x.distance))
            finalArray.append(minDistance[0].word)
            minDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
    return finalArray


def substringSolver(dictionary, text):
    tmp: DistanceWord() = list()
    maxDistance: DistanceWord() = list()
    finalArray: DistanceWord() = list()
    index = 1
    for word in text:
        print(index)
        index += 1
        if word not in dictionary:
            for dic in dictionary:
                X = word
                Y = dic
                n = len(X)
                m = len(Y)
                dst = lcSubstring(X, Y, n, m)
                tmp.append(DistanceWord(X, dst))
            maxDistance.append(max(tmp, key=lambda x: x.distance))
            finalArray.append(maxDistance[0].word)
            maxDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
    return finalArray


def subsequenceSolver(dictionary, text):
    tmp: DistanceWord() = list()
    maxDistance: DistanceWord() = list()
    finalArray: DistanceWord() = list()
    index = 1
    for word in text:
        print(index)
        index += 1
        if word not in dictionary:
            for dic in dictionary:
                X = word
                Y = dic
                dst = lcSubsequence(X, Y)
                tmp.append(DistanceWord(X, dst))
            maxDistance.append(max(tmp, key=lambda x: x.distance))
            finalArray.append(maxDistance[0].word)
            maxDistance.clear()
            tmp.clear()
        else:
            finalArray.append(word)
    return finalArray


if __name__ == '__main__':
    dictionary = readDictionary("slovnik.txt")
    text = readFile("VzorVstupu-Zadanie2.txt")

    f_edit = open("outputEdit2.txt", "w")
    f_substring = open("outputSubstring2.txt", "w")
    f_subsequence = open("outputSubsequence2.txt", "w")

    start1 = time.time()
    finalArray = editDistanceSolver(dictionary, text)
    end1 = time.time()
    output = " ".join([str(x) for x in finalArray])
    f_edit.write(output)
    f_edit.close()

    start2 = time.time()
    finalArray = substringSolver(dictionary, text)
    end2 = time.time()
    output = " ".join([str(x) for x in finalArray])
    f_substring.write(output)
    f_substring.close()

    start3 = time.time()
    finalArray = subsequenceSolver(dictionary, text)
    end3 = time.time()
    output = " ".join([str(x) for x in finalArray])
    f_subsequence.write(output)
    f_subsequence.close()

    print("Edit distance\n")
    textFix = readFile("message.txt")
    textCorrectByAlgo = readFile("outputEdit2.txt")
    print(f"Time to run: {end1 - start1}")
    compareText(textCorrectByAlgo, textFix)

    print("Subsequence\n")
    textFix = readFile("message.txt")
    textCorrectByAlgo = readFile("outputSubsequence2.txt")
    print(f"Time to run: {end2 - start2}")
    compareText(textCorrectByAlgo, textFix)

    print("Substring\n")
    textFix = readFile("message.txt")
    textCorrectByAlgo = readFile("outputSubstring2.txt")
    print(f"Time to run: {end3 - start3}")
    compareText(textCorrectByAlgo, textFix)

    # correctText = []
    # tmp: SubsequenceWord() = list()
    #
    # tmpArray: DistanceWord() = list()
    #
    #
    # for word in text:
    #     for dic in dictionary:
    #         # print("Substring")
    #         X = word
    #         Y = dic
    #
    #         n = len(X)
    #         m = len(Y)
    #
    #         # print(f'{dic}: {lcSubstring(X, Y, n, m)}')
    #         # print("Subsequence")
    #
    #         X = word
    #         Y = dic
    #
    #         subsequence = lcSubsequence(X, Y)
    #         tmp.append(SubsequenceWord(dic, subsequence))
    #         # print(f'{dic}: {subsequence}')
    #
    #     correctText.append(max(tmp, key=lambda x: x.number))
    #     print(word)
    #     tmp.clear()
