'''
InitConfig: This file contains all the configuration variables 
'''
import os, sys, json

class InitConfig(object):
    try:
        DEBUG = True
        ADMIN = False
        tempDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "temp")
        templatesDir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "templates")
        
        with open("config/config.json") as json_file:
            configVal = json.load(json_file)

        with open("config/templateConfig.json") as json_file:
            templateSequence = json.load(json_file)

        transcriptName = configVal["transcriptName"] 

        templateInitials = configVal["templateInitials"] 
        cropImageFolderName = configVal["cropImageFolderName"] 
        cropFileInitials = configVal["cropFileInitials"] 
        contourImageName = configVal["contourImageName"] 
        supportedImageExtensions = configVal["supportedImageExtensions"] 
     
        email = configVal["email"] # the mail which our app will use for sending the mail
        instructorEmail = configVal["instructorEmail"] # the mail of the instructor
        adminEmail = configVal["adminEmail"]
        password = configVal["password"]
        googleServer = configVal["googleServer"]
        googlePort = configVal["googlePort"]
        carbonGlue_mail = configVal["carbonGlue_mail"]
        carbonGlue_pass = configVal["carbonGlue_pass"]

        databaseName = configVal["databaseName"] #Name of database which will be created
        collection_name = configVal["collection_name"]
        studentID = configVal["studentID"]
        set_string = configVal["set_string"]
        semester = configVal["semester"]
        subjects = configVal["subjects"]
        code = configVal["code"]
        grade_point = configVal["grade_point"]
        secret_key = configVal["secret_key"]

    except Exception as ex:
        print ex.message
        sys.exit("Verify: Configuration files missing!!")

    