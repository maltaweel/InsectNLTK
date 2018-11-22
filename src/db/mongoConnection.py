'''
Class to connect to MongoDB.

Created on Jan 19, 2017

@author: 
'''
from pymongo import MongoClient


class mongo:

    def getCollection(self):
        
        '''
        Start the client using Mongo and get collection, which is assumed to be
        called insectNLTK from db insectNLTK
        '''
        self.client = MongoClient()
        db = self.client.insectNLTK
        coll=db['insectNLTK']
         
        return coll
    
    def getDatabase(self):
        '''
        Method returns the database (insectNLTK)
        '''
        self.client=MongoClient()
        db=self.client.insectNLTK;
        
        return db

#m=mongo()
#m.getCollection()