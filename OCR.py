import cv2
import numpy as np
from Utils import Decode 
from Floating_Point_Algorithm import Floating_Point_Algorithm

# OCR v1: using preprocessed image
def OCR(Digits,model):
    output = []

    for i in range(0, len(Digits)):

        im1 = cv2.cvtColor(Digits[i], cv2.COLOR_BGR2GRAY)
        im = cv2.adaptiveThreshold(im1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 33, 10)
        cv2.imshow('sss',im)
        result = []
        # step 1
        imarr = np.asarray(im)
        areas = Floating_Point_Algorithm(imarr, imarr.shape, 0)
        filtered_areas2 = []
        # step 2 filtering
        areas.sort(key=len)
        filtered_areas = areas[-2:].copy()
        for area in filtered_areas:
            if len(area) > 40:
                filtered_areas2.append(area)
        # step 3
        l = len(filtered_areas2)

        max_X = 0
        min_X = 50
        max_Y = 0
        min_Y = 50

        if (l == 0):
            output.append(0)
            result = 0
        elif (l == 1):
            max_X = 0
            min_X = 50
            max_Y = 0
            min_Y = 50
            for point in filtered_areas2[0]:
                if (point[0] > max_X):
                    max_X = point[0]
                if (point[0] <= min_X):
                    min_X = point[0]
                if (point[1] > max_Y):
                    max_Y = point[1]
                if (point[1] <= min_Y):
                    min_Y = point[1]
            Y_dist = max_Y - min_Y
            X_dist = max_X - min_X
            if (Y_dist > 35 or X_dist > 35):
                output.append(0)
                result = 0
            else:
                result = filtered_areas2[0]
        else:
            max1 = 0
            max_X1 = 0
            min_X1 = 50
            max_Y1 = 0
            min_Y1 = 50
            for point in filtered_areas2[0]:
                if (point[0] > max_X1):
                    max_X1 = point[0]
                if (point[0] <= min_X1):
                    min_X1 = point[0]
                if (point[1] > max_Y1):
                    max_Y1 = point[1]
                if (point[1] <= min_Y1):
                    min_Y1 = point[1]
            Y_dist1 = max_Y1 - min_Y1
            X_dist1 = max_X1 - min_X1
            if (Y_dist1 > X_dist1):
                max1 = Y_dist1
            else:
                max1 = Y_dist1

            max2 = 0
            max_X2 = 0
            min_X2 = 50
            max_Y2 = 0
            min_Y2 = 50
            for point in filtered_areas2[1]:
                if (point[0] > max_X2):
                    max_X2 = point[0]
                if (point[0] <= min_X2):
                    min_X2 = point[0]
                if (point[1] > max_Y2):
                    max_Y2 = point[1]
                if (point[1] <= min_Y2):
                    min_Y2 = point[1]
            Y_dist2 = max_Y2 - min_Y2
            X_dist2 = max_X2 - min_X2

            if (Y_dist2 > X_dist2):
                max2 = Y_dist2
            else:
                max2 = Y_dist2

            if (max2 > max1):
                result = filtered_areas2[0]

                max_X = max_X1
                min_X = min_X1
                max_Y = max_Y1
                min_Y = min_Y1
            else:
                result = filtered_areas2[1]

                max_X = max_X2
                min_X = min_X2
                max_Y = max_Y2
                min_Y = min_Y2
        # step 4 perspective
        newIM = np.zeros((50, 50))
        if (result != 0):
            for cell in result:
                newIM[cell[1]][cell[0]] = 255

            TransFrom = np.float32([[min_X, min_Y], [max_X, min_Y], [min_X, max_Y], [max_X, max_Y]])
            TransTo = np.float32([[0, 0], [0, 10], [20, 0], [20, 10]])
            mat = cv2.getPerspectiveTransform(TransFrom, TransTo)
            imOut = cv2.warpPerspective(newIM, mat, (20, 10))

            ret, imOut = cv2.threshold(imOut, 100, 255, cv2.THRESH_BINARY)

            prediction = model.predict(np.array([imOut]))[0]
            output.append(Decode(prediction))
    return output