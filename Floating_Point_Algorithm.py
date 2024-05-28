import numpy as np

def push(stack , item):
    stack.append(item)
    return stack

def pop(stack):
    new_stack = stack[1:]
    return new_stack, stack[0]
def empty(stack):
    if (len(stack) == 0):
        return True
    return False

def Boundaries(x, y, dimension):
    if (y < dimension[0] and -1 < y and x < dimension[1] and -1 < x):
        return True
    else: return False

def Float(i, j, Matrix, Visited, dimension, BW):

    Area = []
    Stack = [[j,i]]
    Visited[i,j] = 1
    x = 0
    y = 0
    #print('\nstart ..')
    while(not empty(Stack)):

        Stack,Cell = pop(Stack)

        x = Cell[0] + 1
        y = Cell[1]
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-1 ..')
            Area.append([x,y])
            push(Stack, [x,y])
            Visited[y, x] = 1
        x = Cell[0]
        y = Cell[1] + 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-2 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0] + 1
        y = Cell[1] + 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-3 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0] - 1
        y = Cell[1]
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-4 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0]
        y = Cell[1] - 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-5 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0] - 1
        y = Cell[1] - 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-6 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0] - 1
        y = Cell[1] + 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-7 ..')
            Area.append([x,y])
            push(Stack, [x, y])
            Visited[y, x] = 1
        x = Cell[0] + 1
        y = Cell[1] - 1
        if (Boundaries(x, y, dimension) and Visited[y,x] == 0 and Matrix[y,x] == BW):
            #print('\nc-8 ..')
            Area.append([x, y])
            push(Stack, [x, y])
            Visited[y, x] = 1


    return Area


def Floating_Point_Algorithm(Matrix, dimension, BW) :

    Visited = np.zeros((dimension[0],dimension[1]))
    Areas = []
    for i in range(15, 35):
        for j in range(12, 38):
            if(Visited[i][j] == 0 and Matrix[i][j] == BW):
                Area = Float(i, j, Matrix, Visited, dimension, BW)
                if (len(Area) != 0):
                   Areas.append(Area)
    return Areas