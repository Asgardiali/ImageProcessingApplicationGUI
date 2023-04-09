import cv2
import numpy as np

def getImgEqualizedHist(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    histValx = np.zeros(256)
    histValy = np.zeros(256)

    for i in range(0, imgGray.shape[0], 1):
        for j in range(0, imgGray.shape[1], 1):
            say = imgGray[i, j]
            histValy[say] = histValy[say] + 1

    for i in range(0, 256, 1):
        histValx[i] = i
        
    pdf = np.zeros(np.size(np.unique(img)))
    
    # Calculate of pixels PDF
    for i in range(0, np.size(np.unique(img)), 1):
        pdf[i] = histValy[i] / (img.shape[0] * img.shape[1])
    
    # Calculate of pixels CDF
    cdf = np.cumsum(pdf)
    
    histEqu = (np.size(np.unique(img))-1) * cdf
    
    for i in range(0, np.size(np.unique(img)), 1):
        histEqu[i] = round(histEqu[i])

    return histEqu
