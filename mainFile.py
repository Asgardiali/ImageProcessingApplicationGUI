from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
import image
import fileOpen
from matplotlib import pyplot as plt


class Ui_MainWindow(object):
    
   
    def setupUi(self, MainWindow):
         
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 550)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("Image Processing ToolBox")
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(70, 20, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.author = QtWidgets.QLabel(self.centralwidget)
        self.author.setGeometry(QtCore.QRect(340, 520, 111, 21))
        self.author.setObjectName("author")

        self.openImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.openImageButton.setGeometry(QtCore.QRect(70, 80, 321, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.openImageButton.setFont(font)
        self.openImageButton.setObjectName("openImageButton")

        self.openDesiredImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.openDesiredImageButton.setGeometry(QtCore.QRect(70, 170, 321, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.openDesiredImageButton.setFont(font)
        self.openDesiredImageButton.setObjectName("openDesiredImageButton")

        self.imageHistogramButton = QtWidgets.QPushButton(self.centralwidget)
        self.imageHistogramButton.setGeometry(QtCore.QRect(70, 260, 321, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.imageHistogramButton.setFont(font)
        self.imageHistogramButton.setObjectName("imageHistogramButton")

        self.imageEqualizationButton = QtWidgets.QPushButton(self.centralwidget)
        self.imageEqualizationButton.setGeometry(QtCore.QRect(70, 350, 321, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.imageEqualizationButton.setFont(font)
        self.imageEqualizationButton.setObjectName("imageEqualizationButton")

        self.imageSpecificationButton = QtWidgets.QPushButton(self.centralwidget)
        self.imageSpecificationButton.setGeometry(QtCore.QRect(70, 440, 321, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.imageSpecificationButton.setFont(font)
        self.imageSpecificationButton.setObjectName("imageSpecificationButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.openImageButton.clicked.connect(self.clickedOpenImage)
        self.openDesiredImageButton.clicked.connect(self.clikedOpenDesiredImage)
        self.imageHistogramButton.clicked.connect(self.clikedImageHistogram)
        self.imageEqualizationButton.clicked.connect(self.clickedImageEqualization)
        self.imageSpecificationButton.clicked.connect(self.clickedImageSpecification)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.title.setText(_translate("MainWindow", "Image Processing ToolBox"))
        self.author.setText(_translate("MainWindow", "Designed by Asgardiali"))
        self.openImageButton.setText(_translate("MainWindow", "Open Image File"))
        self.openDesiredImageButton.setText(_translate("MainWindow", "Open Desired Image"))
        self.imageHistogramButton.setText(_translate("MainWindow", "Image Histogram"))
        self.imageEqualizationButton.setText(_translate("MainWindow", "Image Equalization"))
        self.imageSpecificationButton.setText(_translate("MainWindow", "Image Specification"))

    def clickedOpenImage(self):
        
        fo = fileOpen.App()
        global imgPathOrg
        imgPathOrg = fo.openFileNameDialog()
        img = cv2.imread(imgPathOrg)
        cv2.imshow("Orginal Image", img)
        return imgPathOrg

    def clikedOpenDesiredImage(self):
        
        fo = fileOpen.App()
        global imgPathDesired
        imgPathDesired = fo.openFileNameDialog()
        img = cv2.imread(imgPathDesired)
        cv2.imshow("Desired Image", img)
        return imgPathDesired

    def clikedImageHistogram(self):
        
        img = cv2.imread(imgPathOrg)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        histValx = np.zeros(256)
        histValy = np.zeros(256)
    
        for i in range(0, imgGray.shape[0], 1):
            for j in range(0, imgGray.shape[1], 1):
                say = imgGray[i, j]
                histValy[say] = histValy[say] + 1
    
        for i in range(0, 256, 1):
            histValx[i] = i
            
        plt.title("Histogram Of Orginal Image")
        plt.xlabel("Intensity Values")
        plt.ylabel("Number Of Pixel")
        plt.bar(histValx, histValy)
        plt.show()

    def clickedImageEqualization(self):
        
        imgOrg = cv2.imread(imgPathOrg)
        imgGray = cv2.cvtColor(imgOrg, cv2.COLOR_BGR2GRAY)
    
        histValx = np.zeros(256)
        histValy = np.zeros(256)
    
        for i in range(0, imgGray.shape[0], 1):
            for j in range(0, imgGray.shape[1], 1):
                say = imgGray[i, j]
                histValy[say] = histValy[say] + 1
    
        for i in range(0, 256, 1):
            histValx[i] = i
            
        pdf = np.zeros(np.size(np.unique(imgGray)))
        
        # Calculate of pixels PDF
        for i in range(0, np.size(np.unique(imgGray)), 1):
            pdf[i] = histValy[i] / (imgGray.shape[0] * imgGray.shape[1])
        
        # Calculate of pixels CDF
        cdf = np.cumsum(pdf)
        
        histEqu = (np.size(np.unique(imgGray))-1) * cdf
        
        for i in range(0, np.size(np.unique(imgGray)), 1):
            histEqu[i] = round(histEqu[i])
        
        # Histogram equalization process
        for k in range(0, np.size(np.unique(imgGray)), 1):
            for i in range(0, imgGray.shape[0], 1):
                for j in range(0, imgGray.shape[1], 1):
                    if imgGray[i, j] == k:
                        imgGray[i, j] = histEqu[k]
    
        plt.title("Histogram Equalization Of Image")
        plt.xlabel("Intensity Values")
        plt.ylabel("Number Of Pixel")
        plt.hist(imgGray.ravel(), 256, [0, 256])
        plt.show()
    
        cv2.imshow("Histogram Equalization Of Image", imgGray)
        #cv2.waitKey(0)
        
    def clickedImageSpecification(self):
        
        imgOrg = cv2.imread(imgPathOrg)
        imgDesired = cv2.imread(imgPathDesired)
        
        
        imgHistSpec = np.zeros(256)
        
        imgHistEquOrg = image.getImgEqualizedHist(imgOrg)
        imgHistEquDesired = image.getImgEqualizedHist(imgDesired)    
        
        for i in range(0,imgHistEquOrg.shape[0],1):
            for j in range(0,imgHistEquDesired.shape[0],1):
                if(imgHistEquOrg[i]<=imgHistEquDesired[j]):
                    imgHistSpec[i] = j
                    break    
    
        for i in range(0, imgOrg.shape[0], 1):
            for j in range(0, imgOrg.shape[1], 1):
                k = imgOrg[i, j]
                imgOrg[i, j] = imgHistSpec[k]
                
        plt.title("Histogram Specification Of Image")
        plt.xlabel("Intensity Values")
        plt.ylabel("Number Of Pixel")
        plt.hist(imgOrg.ravel(), 256, [0, 256])
        plt.show()
        
        cv2.imshow("Image Specification",imgOrg)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
