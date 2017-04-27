'''
HelperImageOperations: Helper functions to perform processing on images like finding contours, crop images etc.
'''
import cv2
import os, shutil

class HelperImageOperations:
    def __init__(self):
        print "init fn : HelperImageOperations"
        ### Will declare all this function into config file
        # Upload image will be processed and saved into .png format with same name
        self.transcriptName = 'template1.png' 
        self.tempDir = "/Users/Rkaur/CarbonGlue/temp" #Root directory path with temp os.path.join
        self.cropImageFolderName = "sample"
        self.cropFileInitials = "sample"
        self.contourImageName = "contoured.png"
    
    '''
    Function to crop transcripts depending upon the contours 
    (This function will be later modified to support various templates) 
    ### - represent functionality still need to be implemented 
    '''
    def cropImagePerContours(self, studentID):
        ###Check that the directory exists else exception 
        ###Delete if the sample folder already exists
        
        print "fn: cropImagePerContours Student ID: " + studentID
        srcImagePath = os.path.join(self.tempDir, studentID, self.transcriptName)
        self.findContoursAndSplit(srcImagePath, cropIntoContours = True, contourX = 15, contourY = 6)

    '''
    Function to find contours in an provide image(transcript) and cropping the image as per contours.
    '''
    def findContoursAndSplit(self, srcImagePath, cropIntoContours = True, contourX = 15, contourY = 6):

        print "fn: findContoursAndSplit Image Path: " + srcImagePath
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
        
        for contour in contours:
            [x,y,w,h] = cv2.boundingRect(contour)
            #print x,y,w,h
            if cropIntoContours:
                roi = srcImage[y:y+h, x:x+w]

                cropImageName = self.cropFileInitials + '_' + str(x) + '_' + str(y) +'.png'
                cropImagePath = os.path.join(cropImageDir, cropImageName) 
            
                #print cropImagePath
                cv2.imwrite(cropImagePath, roi)
            else:
                # draw rectangle around contour on original image
                cv2.rectangle(srcImage,(x,y),(x+w,y+h),(255,0,255),2)

                # write original image with added contours to disk  
                contourPath = os.path.join(srcImageDir, self.contourImageName)
                cv2.imwrite(contourPath, srcImage) 

if __name__=="__main__":
    helperImageOperations = HelperImageOperations()
    helperImageOperations.cropImagePerContours('1234')