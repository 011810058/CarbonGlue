'''
	This class provides an API for which implements the functionality of
	sending the mail to the instructor about the status of the student about
	a particular prerequisite
'''

import smtplib
from ..config import initConfig

class SendMail(initConfig.InitConfig):
            def __init__(self):
                self.server = smtplib.SMTP(self.googleServer, self.googlePort)

            def loginToGmail(self):
                self.server.starttls()
                self.server.login(self.email,self.password)

            def sendMailToInstructor(self,studentId):
                SUBJECT = "Student Status"
                TEXT = "Student: "+studentId+" has uploaded his Transcripts"
                message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                self.server.sendmail(self.email,self.instructorEmail,message)
                self.server.quit()

            def sendMailToAdmin(self,studentId):
                print "sending the mail to the admin"
                SUBJECT = "Student Status"
                TEXT = "Student: " + studentId + " was unable to upload his Transcripts"
                message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                self.server.sendmail(self.email, self.adminEmail, message)
                self.server.quit()


