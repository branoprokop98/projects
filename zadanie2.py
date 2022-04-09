# A Space efficient Dynamic Programming
# based Python3 program to find minimum
# number operations to convert str1 to str2
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


def lcs(i, j, count):
    if i == 0 or j == 0:
        return count

    if X[i - 1] == Y[j - 1]:
        count = lcs(i - 1, j - 1, count + 1)

    count = max(count, max(lcs(i, j - 1, 0),
                           lcs(i - 1, j, 0)))

    return count


def lcsequence(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    elif X[m - 1] == Y[n - 1]:
        return 1 + lcsequence(X, Y, m - 1, n - 1)
    else:
        return max(lcsequence(X, Y, m, n - 1), lcsequence(X, Y, m - 1, n))


def readDictionary(filename):
    f = open(filename, "r")
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
    return text


def compareText(textFixedByAlgo, textFixed):
    print(f"Algo fix: {len(textFixedByAlgo)} \n Fixed text: {len(textFixed)}")


class DistanceWord:
    def __init__(self):
        self.word = ""
        self.distance = -1


class SubsequenceWord:
    def __init__(self, word, number):
        self.word = word
        self.number = number

    def __str__(self):
        return str(self.word)


if __name__ == '__main__':

    dictionary = readDictionary("slovnik.txt")
    text = readFile("VzorVstupu-Zadanie2.txt")
    textFix = readFile("VzorVstupu-Zadanie2oprava.txt")
    correctText = []

    tmpArray: DistanceWord() = list()

    for word in text:
        for dic in dictionary:
            distanceWord = DistanceWord()
            distance = EditDistDP(word, dic)
            distanceWord.distance = distance
            distanceWord.word = dic
            tmpArray.append(distanceWord)
        minimum = min(tmpArray, key=lambda x: x.distance)
        indices = []
        for index, element in enumerate(tmpArray):
            if minimum.distance == element.distance:  # check if this element is the minimum_value
                indices.append(element)  # add the index to the list if it is
        print("Substring")
        for inc in indices:
            X = word
            Y = inc.word

            n = len(X)
            m = len(Y)

            print(f'{inc.word}: {lcs(n, m, 0)}')
        print("Subsequence")
        tmp = []
        for inc in indices:
            X = word
            Y = inc.word

            n = len(X)
            m = len(Y)
            subsequence = lcsequence(X, Y, len(X), len(Y))
            tmp.append(SubsequenceWord(inc.word, subsequence))
            print(f'{inc.word}: {subsequence}')

        correctText.append(max(tmp, key=lambda x: x.number))
        indices.clear()
        tmpArray.clear()

    output = " ".join([str(x) for x in correctText])

    f = open("output.txt", "w")
    f.write(output)

    compareText(correctText, textFix)
