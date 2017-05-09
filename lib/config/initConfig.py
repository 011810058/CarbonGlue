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
    templateSequence = {'template1':{
                            '0' : 'Semester.png', 
                            '1' : 'Subject.png'
                            },
                        'template2':{
                            '0' : 'dummy.png',
                            '1': 'Semester_1.png',
                            '2': 'Subject_1.png',
                            '3': 'Semester_2.png',
                            '4': 'Subject_2.png',
                        }}

    databaseName = 'db_carbon_glue' #Name of database which will be created
    collection_name = 'col_student_records'
    supportedImageExtensions = '*.*' #*.jpg
    email = "prerequisite273project@gmail.com" # the mail which our app will use for sending the mail
    instructorEmail = "abhi3003thapar@gmail.com" # the mail of the instructor
    adminEmail = "abhi3003thapar@gmail.com"
    password = "test@273"
    googleServer = 'smtp.gmail.com'
    googlePort = 587

    DEBUG = False
    ADMIN = False

    studentID = "studentID"
    set_string = "$set"
    get_string = "GET"
    post_string = "POST"
    semester = "Semester"
    subjects = "Subjects"
    code = "code"
    grade_point = "GP"
    secret_key = "abhishek-jasmeet-parag-vinayak"
    