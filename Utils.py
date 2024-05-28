def Decode(y):
    L = list(y)
    MAX = 0
    INDEX = -1
    for i in range(0,len(L)):
        if(L[i] > MAX):
            MAX = L[i]
            INDEX = i
    return INDEX + 1


def Replace_Elements_With_Zero(array1, array2):

    if len(array1) != len(array2) or any(len(row1) != len(row2) for row1, row2 in zip(array1, array2)):
        raise ValueError("Both arrays must have the same dimensions")

    result = []
    
    for row1, row2 in zip(array1, array2):
        new_row = []
        for elem1, elem2 in zip(row1, row2):
            if elem2 != 0:
                new_row.append(0)
            else:
                new_row.append(elem1)
        result.append(new_row)
    
    return result