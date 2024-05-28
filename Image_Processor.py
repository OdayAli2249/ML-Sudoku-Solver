import cv2

# Merge Two Images
def Merge_Two_Images(im, im2):
    '''
    for i in range(0,500):
        for j in range(0, 500):
            if(im[i,j] != 0):
                im2[i,j] = [im[i,j], 0, 0]

    '''
    roi = im2.copy()
    mask = im
    mask_inv = cv2.bitwise_not(mask)
    image1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    image2_fg = cv2.cvtColor(cv2.bitwise_and(im, im, mask=mask), cv2.COLOR_GRAY2BGR)
    im2= cv2.add(image1_bg, image2_fg)

    return im2

# Generate Solution Image
def Generate_Solution_Image(matrix,list_of_digits):
    frame = cv2.imread('Resources/digits/empty.jpg',0)
    for i in range(0,9):
        for j in range(0,9):
            #print(matrix[i,j])
            #frame[i*50:(i+1)*50,j*50:(j+1)*50] = cv2.imread('Resources/digits/d' + str(matrix[i,j]) +'.jpg',0)
            frame[i * 50:(i + 1) * 50, j * 50:(j + 1) * 50] = list_of_digits[matrix[i,j]]
    ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    return frame