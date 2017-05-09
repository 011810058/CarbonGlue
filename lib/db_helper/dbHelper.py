# _*_ coding: UTF-8 _*_

from pymongo import MongoClient
from ..config import initConfig


class DBHelper(initConfig.InitConfig):
    """ Performs MongoDB related functions """

    def __init__(self):
        self.mongoClient = MongoClient()

    def getCollection(self, collection_name):
        """ Return the PyMongo collection object based on given collection name """
        db = self.mongoClient[self.databaseName]
        coll = db[collection_name]
        return coll

    def storeInDB(self, json_formate_string, collection_name = None):
        """ This method takes a string in json formate and stores it as json object in MongoDB """
        try:
            success = True
            if isinstance(json_formate_string, dict) is False:
                success = False
            if collection_name is None:
                collection_name = self.collection_name

            selectedCollection = self.getCollection(collection_name)
            key = {self.studentID : json_formate_string.pop(self.studentID,None)}
            update_query = {self.set_string : json_formate_string}
            documentID = selectedCollection.update_one(key,update_query, upsert=True).upserted_id
            if documentID is None:  
                raise "Exception MongoDB: Insert record failed..!!"

            return success
            
        except Exception as ex:
            raise ex
        
    def findInDB(self, query):
        """ Find matching document in collection based on given keys values """ 
        coll = self.getCollection(self.collection_name)
        return coll.find_one(query)
            
