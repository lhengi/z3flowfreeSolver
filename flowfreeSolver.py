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
    
NO
    [
    [1,0,2],
    [0,0,0],
    [2,0,1]
    ]
"""
arr = [
    [1,0,0,3,0],
    [2,0,0,0,0],
    [0,0,0,1,0],
    [0,3,0,0,2],
    [0,0,0,0,0]]

def construct3Dbool(arr,colorList):
    # create a 3d matrix of boolean vars
    n = len(arr)
    numColors = len(colorList)
    m = []

    for i in range(0,numColors):
        eachColorM = []
        for j in range(0,n):
            eachColorM.append(BoolVector("m"+str(i)+"_"+str(j),n))
        m.append(eachColorM)
    return m

def constructDistinctRule(arr,colorList,m):
    #
    n = len(arr)
    numColors = len(colorList)
    colorClause = []

    print(len(m),"  ",len(m[0]),"  ",len(m[0][0]))
    for k in range(0,numColors-1): # each color
        for i in range(0,n): # each row
            for j in range(0,n): # each colum
                for k2 in range(k+1,numColors): # each color
                    #print("K : ", k, " i: ", i, " j: ", j)
                    #print("K2: ", k2, " i: ", i, " j: ", j)
                    colorClause.append( Or(Not(m[k][i][j]), m[k2][i][j])) # color in this cell implies no other color in other cells


    return colorClause
    


def constructcolorCellRule(k,matrix,currentColorMatrix):
    # currentColorMatrix should only contains 0 and 1, where 1 is start and end
    n = len(matrix)
    clauses = []

    for i in range(0,n):
        for j in range(0,n):
            if currentColorMatrix[i][j] == 1:

                clauses.append( Or( matrix[k][i + 1][j], matrix[k][i - 1][j] , matrix[k][i][j + 1], matrix[k][i][j - 1] ) )

                clauses.append(Implies(matrix[k][i + 1][j], Not(matrix[k][i - 1][j])))
                clauses.append(Implies(matrix[k][i + 1][j], Not(matrix[k][i][j + 1])))
                clauses.append(Implies(matrix[k][i + 1][j], Not(matrix[k][i][j - 1])))

                clauses.append(Implies(matrix[k][i - 1][j], Not(matrix[k][i][j + 1])))
                clauses.append(Implies(matrix[k][i - 1][j], Not(matrix[k][i][j - 1])))

                clauses.append(Implies(matrix[k][i][j + 1], Not(matrix[k][i][j - 1])))
            else:

                """
                     a 
                    b c
                     d
                     
                    a or b or c or d
                    a -> (b or c or d)
                    (a -> b) -> -c
                    (a -> b) -> -d
                    (a -> c) -> -b
                    (a -> c) -> -d
                    (a -> d) -> -b
                    (a -> d) -> -c
                    
                    b -> (a or c or d)
                    (b -> c) -> -a
                    (b -> c) -> -d
                    (b -> d) -> -a
                    (b -> d) -> -c
                    
                    c -> (a or b or d)
                    (c -> d) -> -a
                    (c -> d) -> -b
                """

                clauses.append( Or( matrix[k][i + 1][j], matrix[k][i - 1][j], matrix[k][i][j + 1], matrix[k][i][j - 1] ))

                clauses.append( Implies(matrix[k][i + 1][j], Or(matrix[k][i - 1][j], matrix[k][i][j + 1], matrix[k][i][j - 1])) )
                clauses.append( Implies( Implies(matrix[k][i + 1][j], matrix[k][i - 1][j]),Not(matrix[k][i][j + 1]) ) )

                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i - 1][j]), Not(matrix[k][i][j - 1])))
                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i - 1][j]), Not(matrix[k][i][j + 1])))
                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i][j + 1]), Not(matrix[k][i - 1][j])))
                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i][j + 1]), Not(matrix[k][i][j - 1])))
                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i][j - 1]), Not(matrix[k][i - 1][j])))
                clauses.append(Implies(Implies(matrix[k][i + 1][j], matrix[k][i][j - 1]), Not(matrix[k][i][j + 1])))

                clauses.append( Implies(matrix[k][i - 1][j], Or(matrix[k][i + 1][j], matrix[k][i][j + 1], matrix[k][i][j - 1])))
                clauses.append(Implies(Implies(matrix[k][i - 1][j], matrix[k][i][j + 1]), Not(matrix[k][i + 1][j])))
                clauses.append(Implies(Implies(matrix[k][i - 1][j], matrix[k][i][j + 1]), Not(matrix[k][i][j - 1])))
                clauses.append(Implies(Implies(matrix[k][i - 1][j], matrix[k][i][j - 1]), Not(matrix[k][i + 1][j])))
                clauses.append(Implies(Implies(matrix[k][i - 1][j], matrix[k][i][j - 1]), Not(matrix[k][i][j + 1])))

                clauses.append( Implies(matrix[k][i][j + 1], Or(matrix[k][i + 1][j], matrix[k][i - 1][j], matrix[k][i][j - 1])))
                clauses.append(Implies(Implies(matrix[k][i][j + 1], matrix[k][i][j - 1]), Not(matrix[k][i + 1][j])))
                clauses.append(Implies(Implies(matrix[k][i][j + 1], matrix[k][i][j - 1]), Not(matrix[k][i - 1][j])))
    return clauses


def transformInput(arr,colorList):

    processedArr = []
    for k in colorList:
        colorM = []
        for i in range(0,len(arr)):
            colorRow = []
            for j in range(0,len(arr[0])):
                colorRow.append(1 if arr[i][j] == k else 0)
            colorM.append(colorRow)
        processedArr.append(colorM)

    return processedArr
def getColorList(arr):
    numColor = {0}
    for i in range(0, len(arr)):
        numColor = numColor.union(set(arr[i]))

    colorList = list(numColor)
    colorList.sort()
    colorList.pop(0)  # take out color 0
    print(colorList)
    return colorList

def constructFormula(arr):
    colorList = getColorList(arr)
    processedArr = transformInput(arr,colorList)

    for i in processedArr:
        print(i)
    m = construct3Dbool(arr,colorList)
    distinctRule = constructDistinctRule(arr,colorList,m)
    colorCellRule = []

    for k in range(0,len(colorList)):
        colorCellRule.append(constructcolorCellRule(k,m,processedArr[k]))

    s = Solver()

    for rule in distinctRule:
        s.add(rule)
    for rule in colorCellRule:
        s.add(rule)

    return s

def getSolution(arr):

    s = constructFormula(arr)

    if s.check().r > 0:
        print("YES")
    else:
        print("NO")


getSolution(arr)