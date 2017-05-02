'''
InitConfig: This file contains all the configuration variables 
'''
import os, sys

class InitConfig(object):
    # Upload image will be processed and saved into .png format with same name
    transcriptName = 'template1.png'
    tempDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "temp")
    templatesDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "templates")
    templateInitials = "template"
    cropImageFolderName = "sample"
    cropFileInitials = "sample"
    contourImageName = "contoured.png"
    #Move this template sequence to json file and load json object 
    templateSequence = {'template1':{'0': 'dummy.png', '1' : 'Semester.png', '2' : 'Subject.png'},
                        'template2':{
                            '0' : 'dummy.png',
                            '1': 'Semester_1.png',
                            '2': 'Subject_1.png',
                            '3': 'Semester_2.png',
                            '4': 'Subject_2.png',
                        }}
    

       
