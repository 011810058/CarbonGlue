import re
import pytesseract
from PIL import Image

from ..config import initConfig

class HelperJSONBuilder(initConfig.InitConfig):

    def __init__(self): #, _studentID
        print "init fn: HelperJSONBuilder"
        # add gradespan and subjectCodeSpan variable 
        #self.studentID = _studentID
        self.gradeTuple = ('UA', 'UG', 'UE', 'GR', 'GP')
        self.gradeDataTypeDict = {'UA': 'float', 'UG': 'float', 'UE': 'float', 'GR': 'string', 'GP': 'float'}

    def performOCR(self, imagePath):
        srcImage = Image.open(imagePath)#"./images/test0_198.jpg"
        srcText = pytesseract.image_to_string(srcImage, config = "-psm 6") #parameter can be removed 
        return srcText

    def generateSubjectByGradeList(self, imagePath):
        subjectByGrade = []
        srcText = self.performOCR(imagePath)
        srcTextByLine = self.formatOCRTextAndHeader(srcText)
        for lineText in srcTextByLine:
            gradeRecord = self.extractSubjectWithGrades(lineText)
            #print gradeRecord
            subjectByGrade.append(gradeRecord)
        return subjectByGrade
        
    def extractSubjectWithGrades(self, gradePerSubject, subjectCodeSpan = 2, gradeSpan = 5):
        #Function to extract Subject Code, Subject Name and Grades 
        actualValues = {}
        subjectCode = ''
        subjectName = ''
        extractValues = gradePerSubject.split()
        extractValueCount = len(extractValues)
        #print "extractValueCount " + str(extractValueCount)
        for index, fieldValue in list(enumerate(extractValues)):
            if(index < subjectCodeSpan):
                subjectCode += fieldValue
                continue

            if(index >= subjectCodeSpan and extractValueCount-index > gradeSpan):
                subjectName += fieldValue #add spaces to subject name later 
                continue

            if(extractValueCount-index == gradeSpan):#exception handling add later
                actualValues["code"] = subjectCode
                actualValues["name"] = subjectName

            if(extractValueCount-index <= gradeSpan):
                grade = self.gradeTuple[gradeSpan-(extractValueCount-index)]
                gradeDataType = self.gradeDataTypeDict[grade]
                if (gradeDataType == 'float'): 
                    fieldValue = float(fieldValue) 

                actualValues[grade] = fieldValue
                #.decode('utf-8')

        return actualValues

    def removeNumCharDotSpace(self, formatText):
        #Function to remove spacing between number and (.)
        print "To be implemented later"
            # for text in srcText:
            # text = text.replace(' ','$')
            # i = re.finditer('$\d+$.$\d',text)
            # indices = [(m.start(0), m.end(0)) for m in i]
            
            # for start,end in indices:
            #      print text[start : end].replace(' ','')
            # print text
        

    def formatOCRTextAndHeader(self, formatText, removeHeader = True):
        #self.removeNumCharDotSpace(formatText)
        formatTextByLine = formatText.splitlines()
        formatTextByLine = [line.strip(' ') for line in formatTextByLine]
        formatTextByLine = filter(None, formatTextByLine)
        if removeHeader:
            del formatTextByLine[0]
        return formatTextByLine
    
    #def run(self):
    
    def getSemester(self, imagePath, includeMajor = True):
        srcText = self.performOCR(imagePath)
        srcText = self.formatOCRTextAndHeader(srcText, removeHeader = False)
        current = 0
        major = {}
        semester = {}
        while current < len(srcText):
            if current == 0:
                semester = {"Semester" : srcText[current]}
            if includeMajor and current > 1 :
                major = {"Major" : re.sub('MAJOR:\s','', srcText[current])}
            current += 1
        return semester, major

# if __name__ == "__main__":
#     #helperJSONBuilder.generateSubjectByGradeList("./images/test0_872.jpg")