'''
facilitateProcess: This file conatin function to upload student data to DB
'''
# _*_ coding: UTF-8 _*_

from lib.openCV.helperImageOperations import HelperImageOperations
from lib.ocr.helperJSONBuilder import HelperJSONBuilder
from lib.config.initConfig import InitConfig
from lib.db_helper.dbHelper import DBHelper
from lib.mail.sendMail import SendMail
from lib.templates import *
import threading 

class FacilitateProcess(threading.Thread):
   
    def __init__(self, studentID):
        print "fn init: ProcessImageIntoMongoDB"
        threading.Thread.__init__(self)
        self.templateObject = {'template1': template1.Template1(), 'template2': template2.Template2()}
        self.dbHelper = DBHelper()
        self.helperImageOperations = HelperImageOperations()
        self.sendMail = SendMail()
        self.studentID = studentID

    def run(self):
        self.upload(self.studentID)

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

                print "Step 2: Crop image into identified contours"
                self.helperImageOperations.cropImagePerContours(studentID, templateName)     
            
                print "Step 3: Calling template function for %s to create DICT object" % templateName
                objTemplate = self.templateObject[templateName]
                resultJSON = objTemplate.getStudentDetail(studentID)
                
                if InitConfig.DEBUG:
                    print resultJSON
                #return False
                print "Step 4: Store information into database"
                result = self.dbHelper.storeInDB(resultJSON)
                
            else:
                errorMsg = "Warning: Uploaded document for studentID %s is not supported template" % studentID

            self.sendMail.loginToGmail()
            
            if result:
                print "Step 5: Send mail to the instructor"
                self.sendMail.sendMailToInstructor(studentID)
            else:
                print "Step 5: Send mail to user to contact admin as upload transcript fail"
                self.sendMail.sendMailToAdmin(studentID)

        except Exception as ex:
            raise Exception(ex)

#     def cropImage(self, studentID, crop):
#         self.helperImageOperations.cropImagePerContours(studentID, imageTemplateName = "template2", cropIntoContours = crop)
# #, contourX = 12, contourY = 1 )

# if __name__ == "__main__":
#     facilitateProcess = FacilitateProcess('stud1')
#     facilitateProcess.start()
#     #facilitateProcess.upload('1122')
#     facilitateProcess.upload('2345')

    #cropImagePerContours(self, studentID, imageTemplateName = "template1", cropIntoContours = True)


        