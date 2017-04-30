'''
HelperImageOperations: Helper functions to perform processing on images like finding contours, crop images etc.
'''
import cv2
import os, sys, shutil
from ..config import initConfig

class HelperImageOperations(initConfig.InitConfig):
    def __init__(self):
        print "init fn : HelperImageOperations"
        
    '''
    Function to crop transcripts depending upon the contours 
    (This function will be later modified to support various templates) 
    ### - represent functionality still need to be implemented 
    '''
    def cropImagePerContours(self, studentID, imageTemplateName = "template1"):
        ###Check that the directory exists else exception 
        ###Delete if the sample folder already exists
        
        print "fn: cropImagePerContours Student ID: " + studentID
        srcImagePath = os.path.join(self.tempDir, studentID, self.transcriptName)
        self.findContoursAndSplit(srcImagePath, imageTemplateName = "template1", cropIntoContours = True, contourX = 15, contourY = 6)

    '''
    Function to find contours in an provide image(transcript) and cropping the image as per contours.
    '''
    def findContoursAndSplit(self, srcImagePath, imageTemplateName, cropIntoContours = True, contourX = 15, contourY = 6):

        selectedSequence = self.templateSequence[imageTemplateName]
        selectedTemplateValues = list(selectedSequence.values())
        print "fn: findContoursAndSplit Image Path: " + srcImagePath
        print "The sequence {%s} selected for {%s}" % (', '.join(selectedTemplateValues), imageTemplateName)
        srcImageDir = os.path.dirname(srcImagePath)
        srcImage = cv2.imread(srcImagePath)
        gray = cv2.cvtColor(srcImage,cv2.COLOR_BGR2GRAY) # grayscale
        _,thresh = cv2.threshold(gray,125,255,cv2.THRESH_BINARY_INV) # threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(contourX,contourY))#12,1#15,6 #4,2
        dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
        _, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
        
        if cropIntoContours:
            cropImageDir = os.path.join(srcImageDir, self.cropImageFolderName)
            if os.path.exists(cropImageDir):
                   print "Warning: Removing crop images folder"
                   shutil.rmtree(cropImageDir)
                   #os.rmdir(cropImageDir)
            os.mkdir(cropImageDir)
        index = 0
        for contour in reversed(contours):
            [x,y,w,h] = cv2.boundingRect(contour)
            #print x,y,w,h
            if cropIntoContours:
                roi = srcImage[y:y+h, x:x+w]
                #cropImageName = self.cropFileInitials + '_' + str(x) + '_' + str(y) +'.png'

                if index >= len(selectedTemplateValues):
                    print "Warning: The sequence specified by admin is exhausted " + str(index)
                    break
                cropImageName = selectedTemplateValues[index]
                cropImagePath = os.path.join(cropImageDir, cropImageName) 
                index += 1 
                cv2.imwrite(cropImagePath, roi)

            else:
                # draw rectangle around contour on original image
                cv2.rectangle(srcImage,(x,y),(x+w,y+h),(255,0,255),2)

                # write original image with added contours to disk  
                contourPath = os.path.join(srcImageDir, self.contourImageName)
                cv2.imwrite(contourPath, srcImage) 

# if __name__=="__main__":
#     helperImageOperations = HelperImageOperations()
#     helperImageOperations.cropImagePerContours('2345')