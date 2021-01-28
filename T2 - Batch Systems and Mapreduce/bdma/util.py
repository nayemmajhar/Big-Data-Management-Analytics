import numpy as np

def makeTuple(matrix, name):
    tuples = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            tuples.append((name, i, j, matrix[i][j]))
    return tuples  #indices start at 0!


    #Transforms a list of tuples of form ((row, column), value)) into a matrix
def makeMatrix(tuple_list, rows, cols):
    mx = np.empty([rows, cols])
    for tuple in tuple_list:
        row = tuple[0][0]
        column = tuple[0][1]
        val = tuple[1]
        mx[row][column] = val
    return np.array(mx)

