'''
facilitateProcess: This file conatin function to upload student data to DB
'''
# _*_ coding: UTF-8 _*_


from lib.openCV.helperImageOperations import HelperImageOperations
from lib.ocr.helperJSONBuilder import HelperJSONBuilder
from lib.config.initConfig import InitConfig
from lib.db_helper.dbHelper import DBHelper
from lib.templates import *

class FacilitateProcess(object):
   
    def __init__(self):
        print "fn init: ProcessImageIntoMongoDB"
        #self.indentifiedTemplate = "template1"
        self.templateObject = {'template1': template1.Template1(), 'template2': template2.Template2()}
        self.dbHelper = DBHelper()
        self.helperImageOperations = HelperImageOperations()

    '''
    upload function: perform all steps to indentify template, crop, ocr, generate dict and store to DB 
    '''
    def upload(self, studentID):
        print "fn: Upload function called for %s" % studentID
        try:
            print "Step 1: To identify uploaded image resemble which template"
            result , templateName = self.helperImageOperations.getTemplateName(studentID)
            
            if result:
                print "Result: uploaded document matches %s" % templateName
            else:
                errorMsg = "Uploaded document for studentID %s is not supported template" % studentID
                raise ValueError(errorMsg) 

            print "Step 2: Crop image into identified contours"
            self.helperImageOperations.cropImagePerContours(studentID, templateName)     
        
            print "Step 3: Calling template function for %s to create DICT object" % templateName
            objTemplate = self.templateObject[templateName]
            resultJSON = objTemplate.getStudentDetail(studentID)
           
            print "Step 4: Store information into database"
            result = self.dbHelper.storeInDB(resultJSON)

            # if result:
            #     #implement code to send mail to the studentID
            # else:
            #     #send mail to user to contact admin as upload transcript fail 
             
        except Exception as ex:
            raise ex

# if __name__ == "__main__":
#     facilitateProcess = FacilitateProcess()
#     facilitateProcess.upload('1234')


        