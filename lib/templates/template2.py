'''
Templete2 :  File extend from HelperJSONBuilder to perform opertaions related to template 2
'''
import os

from ..ocr.helperJSONBuilder import HelperJSONBuilder

class Template2(HelperJSONBuilder):
    def __init__(self):
        self.imageTemplateName =  (os.path.splitext(os.path.basename(__file__))[0]).lower()
        super(Template2, self).__init__()

    '''
    Function : Create a dictonary object that can be directly saved into MongoDB
    '''
    def getStudentDetail(self, studentID):
        print "fn: getStudentDetail %s" % studentID
        try:
            selectedSequence = self.templateSequence[self.imageTemplateName]
            studentRecord = {'studentID': studentID}
            
            cropImagePath = os.path.join(self.tempDir, studentID, self.cropImageFolderName)
            
            for file_name in os.listdir(cropImagePath):
                cropImageFileName = os.path.join(cropImagePath, file_name)
                
                if file_name == selectedSequence['1']:
                    semester_1, major = self.getSemester(cropImageFileName)
                    studentRecord.update(major)

                elif (file_name == selectedSequence['2']): 
                    subjectByGrade = self.generateSubjectByGradeList(cropImageFileName)
                    studentRecord['Semester1']= semester_1
                    studentRecord['Semester1']['Subjects'] = subjectByGrade

                elif (file_name == selectedSequence['3']):
                    semester_2, major = self.getSemester(cropImageFileName)
                    #studentRecord.update(major)
                
                elif (file_name == selectedSequence['4']):
                    subjectByGrade = self.generateSubjectByGradeList(cropImageFileName)
                    studentRecord['Semester2']= semester_2
                    studentRecord['Semester2']['Subjects'] = subjectByGrade
                    
            return studentRecord
        except Exception as ex:
            print "fn: getStudentDetail " + ex.message
            raise ex

# if __name__ == "__main__":
#     template = Template1()
#     print template.getStudentDetail('2345')
    # helperJSONBuilder.generateSubjectByGradeList("./images/test0_872.jpg")
