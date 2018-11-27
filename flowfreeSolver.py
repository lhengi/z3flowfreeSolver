from z3 import Solver, Bool, Bools, Or, And, Not, Implies, If, BoolVector
import numpy as np

"""
YES
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 3, 0],
    [2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 3, 0, 0, 2],
    [0, 0, 0, 0, 0, 0]

NO
    [
    [1,0,0,3,0],
    [2,0,0,0,0],
    [0,0,0,1,0],
    [0,3,0,0,2],
    [0,0,0,0,0]]

YES
[
[1,0,2],
[0,0,0],
[1,0,2]
]

NO
    [
    [1,0,2],
    [0,0,0],
    [2,0,1]
    ]

YES
    [
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,9,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0],
    [0,0,0,0,7,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,5,0,0,0,0,0,0,2,0,0,0,0,0,2,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [8,0,0,0,0,0,0,0,0,0,0,0,3,0,0,8,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
    [0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
"""
arr = [
    [10, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 9, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
]

def constructMy3Dbool(arr, colorList):
    n = len(arr)

    numColors = len(colorList)
    m = []

    for i in range(0, numColors):
        eachColorM = []
        for j in range(0, n):
            eachColorM.append(BoolVector("m" + str(i) + "_" + str(j), n))
        m.append(eachColorM)

    return m


def getColorList(arr):
    numColor = {0}
    for i in range(0, len(arr)):
        numColor = numColor.union(set(arr[i]))

    colorList = list(numColor)

    colorList.sort()
    return colorList


def addDistinctRule(myBools, x, colorList):
    n = len(myBools[0])
    numColors = len(colorList)

    for k in range(0, numColors):  # each color
        for i in range(0, n):  # each row
            for j in range(0, n):  # each column
                for k2 in range(0, numColors):  # each color
                    if k != k2 and k2 > k:
                        x.add(Or(Not(myBools[k][i][j]),
                                 Not(myBools[k2][i][j])))  # color in this cell implies no other color in other cells
    return x


def addColorRule(k, myBools, arr, x):
    n = len(myBools[0])
    for i in range(0, n):
        for j in range(0, n):
            a = False;
            b = False;
            c = False;
            d = False;

            if (i < n - 1):
                a = myBools[k][i + 1][j]
            if (i > 0):
                b = myBools[k][i - 1][j]
            if (j < n - 1):
                c = myBools[k][i][j + 1]
            if (j > 0):
                d = myBools[k][i][j - 1]

            if arr[i][j] == k and k != 0:

                x.add(myBools[k][i][j])

                x.add(Or(a, b, c, d))  # a or b or c or d

                x.add(Implies(a, Not(b)))  # a -> -b
                x.add(Implies(a, Not(c)))  # a -> -c
                x.add(Implies(a, Not(d)))  # a -> -d

                x.add(Implies(b, Not(c)))  # b -> -c
                x.add(Implies(b, Not(d)))  # b -> -d

                x.add(Implies(c, Not(d)))  # c -> -d
            else:

                x.add(Or(Not(myBools[k][i][j]), Or(a, b, c, d)))  # a or b or c or d

                x.add(Or(Not(myBools[k][i][j]), Implies(a, Or(b, c, d))))
                x.add(Or(Not(myBools[k][i][j]), Or(Not(a), Not(b), Not(c))))
                x.add(Or(Not(myBools[k][i][j]), Or(Not(a), Not(b), Not(d))))
                x.add(Or(Not(myBools[k][i][j]), Or(Not(a), Not(c), Not(d))))

                x.add(Or(Not(myBools[k][i][j]), Implies(b, Or(a, c, d))))
                x.add(Or(Not(myBools[k][i][j]), Or(Not(b), Not(c), Not(d))))

                x.add(Or(Not(myBools[k][i][j]), Implies(c, Or(a, b, d))))
                x.add(Or(Not(myBools[k][i][j]), Implies(d, Or(a, b, c))))
    return x


def getSolution(arr):
    x = Solver()
    colorList = getColorList(arr)
    myBools = constructMy3Dbool(arr, colorList)

    x = addDistinctRule(myBools, x, colorList)

    for k in range(0, len(colorList)):
        x = addColorRule(k, myBools, arr, x)

    # print(x)

    if x.check().r > 0:
        print("YES")
        print()
        # print(x.model())

        myArray = np.zeros((len(myBools[0]), len(myBools[0])), dtype=np.int)
        for k in range(0, len(colorList)):  # each color
            for i in range(0, len(myBools[0])):  # each row
                for j in range(0, len(myBools[0])):  # each column
                    if x.model().get_interp(myBools[k][i][j]):
                        myArray[i][j] = k

        print(myArray)

    else:
        print("NO")


getSolution(arr)
