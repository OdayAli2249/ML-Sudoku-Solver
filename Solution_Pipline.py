import cv2
import operator
import numpy as np
from Solve_Sudoku import Solve_Sudoku
from Image_Processor import Merge_Two_Images, Generate_Solution_Image
from HOG_OCR import HOG_OCR
from OCR import OCR
from Utils import Replace_Elements_With_Zero

# solver
def Solution_Pipline(im, classifier,LOD,OCRV):

    im = cv2.resize(im, (500, 500))
    imGra = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(imGra, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 12)
    imgt = cv2.bitwise_not(img,img)


    contor, hierarchy = cv2.findContours(imgt,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2:]

    contours = sorted(contor, key=cv2.contourArea, reverse=True)
    polygon = contours[0]
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in
                      polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in
                  polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in
                     polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in
                   polygon]), key=operator.itemgetter(1))


    Width, Height = 450, 450

    TransFrom = np.float32([[polygon[top_left][0][0], polygon[top_left][0][1]],
                        [polygon[top_right][0][0], polygon[top_right][0][1]],
                        [polygon[bottom_left][0][0], polygon[bottom_left][0][1]],
                        [polygon[bottom_right][0][0], polygon[bottom_right][0][1]]])
    TransTo = np.float32([[0, 0], [Height, 0], [0, Width], [Width, Height]])
    mat = cv2.getPerspectiveTransform(TransFrom, TransTo)
    imOut = cv2.warpPerspective(im, mat, (Width, Height))
    imOu = cv2.warpPerspective(imgt, mat, (Width, Height))            # input for is_Changed function

    Digits = []
    CC = 0
    for i in range(0,9):
        for j in range(0,9):
            Digits.append(imOut[i*50:(i+1)*50,j*50:(j+1)*50].copy())
            CC+=1
            
    # 1 - classify the digits in Digits array using NN
    # input : Digits - array contain 81 image of numbers or empty with size 9*9.
    # output : Digits - array contain 81 numbers or empty ( as -1 ) that represent the classified images.

    if(OCRV == 2):
       sol1 = HOG_OCR(Digits,classifier)
    else:
       sol1 = OCR(Digits, classifier)

    sol = []
    for i in range(0,9):
        sol.append(sol1[i*9:(i+1)*9])
    print('pre-OSR : ', sol)
    # 2 - find solution of step -1- output grid of digits using sudoku solver algorithm
    # input : Digits - array contain 81 numbers or empty ( as -1 ) that represent the classified images
    # output : Digits - array contain 81 numbers that represent the solution
    copySol = [row[:] for row in sol]
    Solve_Sudoku(copySol)
    print('post-OSR : ', copySol)
    print('copy : ', sol)

    current_solution = Generate_Solution_Image(np.asarray(Replace_Elements_With_Zero(copySol,sol)),LOD)
    # current_solution = Generate_Solution_Image(np.asarray(copySol),LOD)

    Width, Height = 450, 450  # should be current solution dimension
    Width2, Height2 = 500, 500  # should be video frame dimension
    TransFrom = np.float32([[0, 0], [Height, 0], [0, Width], [Width, Height]])
    TransTo = np.float32([[polygon[top_left][0][0], polygon[top_left][0][1]],
                          [polygon[top_right][0][0], polygon[top_right][0][1]],
                          [polygon[bottom_left][0][0], polygon[bottom_left][0][1]],
                          [polygon[bottom_right][0][0], polygon[bottom_right][0][1]]])
    mat = cv2.getPerspectiveTransform(TransFrom, TransTo)
    imOut = cv2.warpPerspective(current_solution, mat, (Width2, Height2))

    terget_image = Merge_Two_Images(imOut, im)
    
    return current_solution,terget_image



