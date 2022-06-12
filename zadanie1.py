import numpy
import numpy as np
import pandas as pd


class Dictionary:
    def __init__(self, freq, word):
        self.freq = freq
        self.word = word
        self.left = None
        self.right = None


class BSTNode:
    def preorder(self, root, level, d):
        if root is None:
            return
        d.setdefault(level, []).append(root.word)
        self.preorder(root.left, level + 1, d)
        self.preorder(root.right, level + 1, d)

    def printTree(self, root):
        d = {}
        self.preorder(root, 1, d)
        for i in range(1, len(d) + 1):
            print(f'Level {i}:', d[i])

    def buildTree(self, keys, rootArray):
        root = keys[rootArray[0][len(keys) - 1]]
        S = []
        S.append((root, 0, len(keys) - 1))
        while len(S) != 0:
            (u, i, j) = S.pop()
            l = rootArray[i][j]
            if l < j:
                v = keys[rootArray[l + 1][j]]
                u.right = v
                S.append((v, l + 1, j))
            if i < l:
                v = keys[rootArray[i][l - 1]]
                u.left = v
                S.append((v, i, l - 1))
        return root

    def pocet_porovnani(self, root, key):
        compare_count = 0
        while root is not None:
            if key > root.word:
                compare_count += 1
                root = root.right
            elif key < root.word:
                root = root.left
                compare_count += 1
            elif key == root.word:
                return compare_count
        return "Slovo sa v strome nenachádza"


def readFile(filename):
    f = open(filename, "r")
    lines = f.read().splitlines()
    array = []
    for line in lines:
        splitLine = line.split(" ")
        dictionary = Dictionary(int(splitLine[0]), splitLine[1])
        array.append(dictionary)
    array = sorted(array, key=lambda x: x.word)
    return array


def count_pi(array):
    valuesSum = sum(item.freq for item in array)
    p_i = []
    for item in filter(lambda x: x.freq > 50000, array):
        p_i.append(item.freq / valuesSum)
    return p_i


def count_qi(array):
    q_i = []
    valuesSumAll = sum(item.freq for item in array)
    tmp = []
    if array[0].freq > 50000:
        q_i.append(0)
    position = 0
    while position != len(array):
        while position != len(array):
            if array[position].freq <= 50000:
                tmp.append(array[position])
            else:
                break
            position += 1
        if len(tmp) != 0:
            position -= 1
            valuesSum = sum(item.freq for item in tmp)
            q_i.append(valuesSum / valuesSumAll)
            tmp.clear()
        if array[position - 1].freq > 50000:
            q_i.append(0)
        position += 1
    return q_i


def optimalBST(P, Q, n):
    e = pd.DataFrame(np.diag(Q), index=range(1, n + 2))
    w = pd.DataFrame(np.diag(Q), index=range(1, n + 2))
    root = pd.DataFrame(np.zeros((n, n)), index=range(1, n + 1),
                        columns=range(1, n + 1))
    p = pd.Series(P, index=range(1, n + 1))
    q = pd.Series(Q)
    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e.at[i, j] = np.inf
            w.at[i, j] = w.at[i, j - 1] + p[j] + q[j]

            for r in range(i, j + 1):
                t = e.at[i, r - 1] + e.at[r + 1, j] + w.at[i, j]
                if t < e.at[i, j]:
                    e.at[i, j] = t
                    root.at[i, j] = r - 1
    return e, w, root


def sortKey(dictionary):
    p_i = []
    q_i = []
    for item in filter(lambda x: x.freq > 50000, dictionary):
        p_i.append(item)
    key = sorted(p_i, key=lambda x: x.word)
    for item in filter(lambda x: x.freq <= 50000, dictionary):
        q_i.append(item)
    dummyKey = sorted(q_i, key=lambda x: x.word)
    return key, dummyKey


if __name__ == '__main__':
    dictionary = readFile("dictionary.txt")
    key, dummy_key = sortKey(dictionary)
    pi = count_pi(dictionary)
    qi = count_qi(dictionary)
    n = len(pi)

    result = sum(item for item in pi) + sum(item for item in qi)

    e, w, root = optimalBST(pi, qi, len(pi))
    root = root.astype(numpy.int64)
    root = root.values.tolist()

    tree = BSTNode()
    root = tree.buildTree(key, root)
    tree.printTree(root)

    while True:
        val = input("Zadaj retazec: ")
        print(tree.pocet_porovnani(root, val))
