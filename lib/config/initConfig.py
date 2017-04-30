'''
InitConfig: This file contains all the configuration variables 
'''
import os, sys

class InitConfig(object):
    # Upload image will be processed and saved into .png format with same name
    transcriptName = 'template1.jpg'
    tempDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "temp")
    templatesDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "templates")
    cropImageFolderName = "sample"
    cropFileInitials = "sample"
    contourImageName = "contoured.png"
    template1_Order = {'Img1' : 'Semester.png', 'Img2' : 'Subject.png'}
    #Move this template sequence to json file and load json object 
    templateSequence = {'template1':{'1' : 'Semester.png', '2' : 'Subject.png'}}
    

       
