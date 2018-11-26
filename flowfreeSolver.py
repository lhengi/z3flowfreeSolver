from z3 import Solver, Bool, Bools, Or, And, Not, Implies, If, BoolVector

# test
"""
YES
   [[0,0,0,0,0,0],
    [1,0,0,0,3,0],
    [2,0,0,0,0,0],
    [0,0,0,0,1,0],
    [0,0,3,0,0,2]]
    
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
"""
arr = [
[1,0,2],
[0,0,0],
[1,0,2]
]


def construct3Dbool(arr,colorList):
    # create a 3d matrix of boolean vars
    n = len(arr)
    numColors = len(colorList)
    m = []

    for i in range(0,numColors):
        eachColorM = []
        for j in range(0,n+2):
            eachColorM.append(BoolVector("m"+str(i)+"_"+str(j),n+2))
        m.append(eachColorM)


    return m

def transformInput(arr,colorList):

    # add 0 edges and set the to false to later, so we don't need to handle edge cases
    processedArr = []
    for k in colorList:
        colorM = []
        colorM.append([0]*(len(arr)+2))
        for i in range(0,len(arr)):
            colorRow = [0]
            for j in range(0,len(arr[0])):
                colorRow.append(1 if arr[i][j] == k else 0)
            colorRow.append(0)
            colorM.append(colorRow)
        colorM.append([0] * (len(arr) + 2))
        processedArr.append(colorM)

    return processedArr
def getColorList(arr):
    numColor = {0}
    for i in range(0, len(arr)):
        numColor = numColor.union(set(arr[i]))

    colorList = list(numColor)
    colorList.sort()
    colorList.pop(0)  # take out color 0
    return colorList

def constructDistinctRule(colorList,m):
    #
    n = len(m[0])
    numColors = len(colorList)
    colorClause = []

    print(len(m),"  ",len(m[0]),"  ",len(m[0][0]))
    for k in range(0,numColors): # each color
        for i in range(0,n ): # each row
            for j in range(0,n): # each colum
                if i == 0 or j == 0 or i == n - 1 or j == n -1:
                    colorClause.append(Not(m[k][i][j]))
                    continue
                for k2 in range(0,numColors): # each color
                    #print("K : ", k, " i: ", i, " j: ", j)
                    #print("K2: ", k2, " i: ", i, " j: ", j)
                    if k == k2:
                        continue
                    colorClause.append( Or(Not(m[k][i][j]), m[k2][i][j])) # color in this cell implies no other color in other cells


    return colorClause
    



def constructcolorCellRule(k,matrix,currentColorMatrix):
    # currentColorMatrix should only contains 0 and 1, where 1 is start and end
    n = len(matrix[0])
    clauses = []

    for i in range(1,n-1):
        for j in range(1,n-1):
            a = matrix[k][i + 1][j]
            b = matrix[k][i - 1][j]
            c = matrix[k][i][j + 1]
            d = matrix[k][i][j - 1]
            if currentColorMatrix[i][j] == 1:

                # start and end node should have exactly one neighbors with same color

                clauses.append( Or( a, b , c, d ) )         # a or b or c or d

                clauses.append(Implies(a, Not(b)))          # a -> -b
                clauses.append(Implies(a, Not(c)))          # a -> -c
                clauses.append(Implies(a, Not(d)))          # a -> -d

                clauses.append(Implies(b, Not(c)))          # b -> -c
                clauses.append(Implies(b, Not(d)))          # b -> -d

                clauses.append(Implies(c, Not(d)))          # c -> -d
            else:

                """
                None start or end node should have exactly two neighbors with same color
                     a 
                    b c
                     d
                     
                    
                    
                    
                    
                    # c -> (a or b or d)
                    # c & d -> -a       -c or -d or -a
                    # c & d -> -b       -c or -d or -b
                """

                # need to consider edge cases

                clauses.append(Or(a, b, c, d))  # a or b or c or d

                # a or b or c or d
                # a -> (b or c or d)
                # a & b -> -c       -a or -b or -c
                # a & b -> -d       -a or -b or -d
                # a & c -> -b       -a or -c or -b
                # a & c -> -d       -a or -c or -d
                # a & d -> -b       -a or -d or -b
                # a & d -> -c       -a or -d or -c
                clauses.append(Implies(a, Or(b, c, d)))
                clauses.append(Or(Not(a), Not(b), Not(c)))
                clauses.append(Or(Not(a), Not(b), Not(d)))
                clauses.append(Or(Not(a), Not(c), Not(d)))

                # b -> (a or c or d)
                # b & c -> -a       -b or -c or -a
                # b & c -> -d       -b or -c or -d
                # b & d -> -a       -b or -d or -a
                # b & d -> -c       -b or -d or -c
                clauses.append(Implies(b, Or(a, c, d)))
                clauses.append(Or(Not(b), Not(c), Not(d)))

                # c -> (a or b or d)
                # c & d -> -a       -c or -d or -a
                # c & d -> -b       -c or -d or -b
                clauses.append(Implies(c, Or(a, b, d)))
                clauses.append(Implies(d, Or(a, b, c)))
    return clauses



def constructFormula(arr):
    colorList = getColorList(arr)
    processedArr = transformInput(arr,colorList)

    for i in processedArr:
        print(i)
    m = construct3Dbool(arr,colorList)
    distinctRule = constructDistinctRule(colorList,m)
    colorCellRule = []

    for k in range(0,len(colorList)):
        colorCellRule.append(constructcolorCellRule(k,m,processedArr[k]))

    s = Solver()

    for rule in distinctRule:
        s.add(rule) # should be fine
    for rule in colorCellRule:
        s.add(rule)

    print(s)

    return s

def getSolution(arr):

    s = constructFormula(arr)

    if s.check().r > 0:
        print("YES")
    else:
        print("NO")


getSolution(arr)