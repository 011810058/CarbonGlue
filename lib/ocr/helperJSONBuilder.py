import pytesseract
from PIL import Image

class HelperJSONBuilder:
    def __init__(self):
        print "init function"
        # add gradespan and subjectCodeSpan variable 
        self.gradeTuple = ('UA', 'UG', 'UE', 'GR', 'GP')

    def performOCR(self, imagePath):
        srcImage = Image.open(imagePath)#"./images/test0_198.jpg"
        srcText = pytesseract.image_to_string(srcImage) #config = "-psm 6" parameter can be removed 
        return srcText

    def generateSubjectByGradeList(self, imagePath):
        subjectByGrade = []
        srcText = self.performOCR(imagePath)
        srcTextByLine = self.formatOCRTextAndHeader(srcText)
        for lineText in srcTextByLine:
            gradeRecord = self.extractSubjectWithGrades(lineText)
            print gradeRecord
            subjectByGrade.append(gradeRecord)
        return subjectByGrade
    
    # def getSemester(self, imagePath):
    #     srcText = self.performOCR(imagePath)
    #     srcText = self.formatOCRTextAndHeader(srcText, removeHeader = False)
    #     print srcText 
        
    def extractSubjectWithGrades(self, gradePerSubject, subjectCodeSpan = 2, gradeSpan = 5):
        #Function to extract Subject Code, Subject Name and Grades 
        actualValues = {}
        subjectCode = ''
        subjectName = ''
        extractValues = gradePerSubject.split()
        extractValueCount = len(extractValues)
        print "extractValueCount " + str(extractValueCount)
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
                actualValues[self.gradeTuple[gradeSpan-(extractValueCount-index)]] = fieldValue 
                #.decode('utf-8')

        return actualValues

    def removeNumCharDotSpace(self, formatText):
        #Function to remove spacing between number and (.)
        print "To be implemented later"

    def formatOCRTextAndHeader(self, formatText, removeHeader = True):
        #self.removeNumCharDotSpace(formatText)
        formatTextByLine = formatText.splitlines()
        formatTextByLine = [line.strip(' ') for line in formatTextByLine]
        formatTextByLine = filter(None, formatTextByLine)
        if removeHeader:
            del formatTextByLine[0]
        return formatTextByLine
    #def run(self):

if __name__ == "__main__":
    helperJSONBuilder = HelperJSONBuilder()
    helperJSONBuilder.getSemester("./images/test0_0.jpg")
    #helperJSONBuilder.generateSubjectByGradeList("./images/test0_198.jpg")
    #helperJSONBuilder.generateSubjectByGradeList("./images/test0_872.jpg")