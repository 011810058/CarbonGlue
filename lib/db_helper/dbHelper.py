# _*_ coding: UTF-8 _*_

from pymongo import MongoClient
from ..config.initConfig import InitConfig

class DBHelper():
    """ Performs MongoDB related functions """

    def __init__(self):
        print "init function"

    def getCollection(self, colName):
        """ Return the PyMongo collection object based on given collection name """
        client = MongoClient()
        db = client[InitConfig.databaseTitle]
        coll = db[colName]
        return coll

    def storeInDB(self,jsonFormatString):
        """ This method takes a string in json formate and stores it 
        as json object in MongoDB """
        print type(jsonFormatString)
        coll = self.getCollection('student2345')

        DOC_ID = coll.insert_one(jsonFormatString).inserted_id
        print DOC_ID

    
        
    def findInDB(self):
        """ Find matching document in collection based on given keys values """
        
        coll = self.getCollection('student2345')

        query = {"studentID":"1234", "$and":[{"Semester1.Subjects": \
                {"$elemMatch":{"code":"CMPE202", "GP":{"$gte":5}, \
                "GR":{"$in": ["A","A+", "A-", "B", "B+", "B-"]}}}},\
                {"Semester1.Subjects":{"$elemMatch":{"code":"CMPE273", "GP":{"$gte":5}, \
                "GR":{"$in": ["A","A+", "A-", "B", "B+", "B-"]}}}}]}
        print coll.find(query).count()
            
