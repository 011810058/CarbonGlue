# _*_ coding: UTF-8 _*_

from pymongo import MongoClient
from ..config import initConfig


class DBHelper(initConfig.InitConfig):
    """ Performs MongoDB related functions """

    def __init__(self):
        print "fn init: DBHelper"
        self.mongoClient = MongoClient()

    def getCollection(self, collectionName):
        """ Return the PyMongo collection object based on given collection name """
        print "fn getCollection: %s" % collectionName
        db = self.mongoClient[self.databaseName]
        coll = db[collectionName]
        return coll

    def storeInDB(self, jsonFormatString, collectionName = None):
        """ This method takes a string in json formate and stores it 
        as json object in MongoDB """
        try:
            success = True
            if type(jsonFormatString) is not dict:
                print "Invalid string type provided"
                success = False
               
            if collectionName is None:
                collectionName = self.collectionName

            selectedCollection = self.getCollection(collectionName)
            key = {"studentID" : jsonFormatString.pop("studentID",None)}
            update_query = {"$set" : jsonFormatString}
            documentID = selectedCollection.update_one(key,update_query, upsert=True).upserted_id
            if documentID is None:  
                raise "Exception MongoDB: Insert record failed..!!"

            return success
            
        except Exception as ex:
            print ex.message
            raise ex
        
    def findInDB(self, query):
        """ Find matching document in collection based on given keys values """
        
        coll = self.getCollection(self.collectionName)

        # query = {"studentID":"1234", "$and":[{"Semester1.Subjects": \
        #         {"$elemMatch":{"code":"CMPE202", "GP":{"$gte":5}, \
        #         "GR":{"$in": ["A","A+", "A-", "B", "B+", "B-"]}}}},\
        #         {"Semester1.Subjects":{"$elemMatch":{"code":"CMPE273", "GP":{"$gte":5}, \
        #         "GR":{"$in": ["A","A+", "A-", "B", "B+", "B-"]}}}}]}
        # return coll.find(query).count()
        return coll.find_one(query)
            
