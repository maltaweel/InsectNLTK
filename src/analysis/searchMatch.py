'''
Class used to load hdp and lda topics and terms.
These topics and terms are searched and a tf-idf analysis is conducted.
The results are based on years search and types of government documents (e.g., Federal).
See MPB_Source_Doc.csv 'Material type' column to see types of documents.

@author: 
'''
import re
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from db import mongoConnection
from scrape import csvExtract
import os
import csv
import zlib, base64
from gensim.models import Phrases
from gensim.models.phrases import Phrases
from gensim.models.phrases import Phraser
from db import filterBeetle 
from db import filterGovernment
from db.mongoConnection import mongo
import gridfs
from nlp import patternMatching
import numpy as np

class WordPatternAnalysis (patternMatching.PatternMatcher) :
    

    def retrieveContent(self, yearT, yearE, materialType,flt):
        '''
        Method will get content from Mongo database based on years searched and only sentences relevant to beetles.
        yearT-- the year to begin (inclusive) the search
        yearE-- the year up until to conduct the search (not inclusive) 
        materialType-- the type of material (e.g., Federal)
        flt-- filter list to filter search (e.g., by 'beetle', etc.)
        '''
        m=mongo()
        db=m.getDatabase()
        fs = gridfs.GridFS(db)
        self.tC=0
        cursor = self.getCursor()
#       cursor=filterGovernment.filterGovernmentType(flt, cursor)
        fb=filterBeetle.FilterBeetle()
        
        return_list=[]
        codeList=[]
        codeD={}
        ii=0
        
        #for loop looking at retrieved documents
        for document in cursor:
            
            code=document['Code']
            dateAccess=document['Database Name']
            
            c=code+'.pdf'
            if c in codeList:
                continue
            codeList.append(c)
            
            if code in codeD.keys():
                continue
            
            codeD[code]=code
            
            dbLink=''
            try:
                dbLink=document['Other Notes']
            except :
                dbLink=''
                
            
            title=document['Title']
            
            filt=''
            try:
                filt=document['Filters']
            except :
                filt=''
            
            year=''
            y=0
            try:
                year=document['Year']
                y=int(year)
                
                if(y>=yearE or y<yearT):
                    continue
                
            except:
                year=''
             
            month=''
            try:   
                month=document['Month'] 
            except:
                month=''
            
            day=''
            try:  
                day=document['Day']
            except:
                day=''
            
            material=''
            
            try:
                material=document["Material"]
            except:
                material=''
                
            govLevel1=document['Government Level 1']
            
            if materialType is not "":
                
                
                if materialType not in material:
                    continue
                
            
            govLevel2=document['Government Level 2']
            
            search=''
            try:
                search=document['Search Term']
            
            except:
                search=''
            content=''  
            try:
                txt=document['Content']
                content=fs.get(txt).read()
                
            except :
                content=''
           
            
            text=""
                    
            text=content.decode('utf-8')
            
            text=fb.filterBeetleSentences(text,flt)

            
            returns={"Code":code, "Date Accessed":dateAccess,"DB Link":dbLink,
                    "Title":title, "Filter":filt, "Year":year, "Month":month,"Day":day,"Material":material,
                    "Gov Level 1":govLevel1,"Gov Level 2":govLevel2, "Text":text, "Search":search} 
            
            return_list.append(returns) 
            
            print(c)
            
            self.tC+=1
            
        
            ii+=1
        
        return return_list

    
    def loadSearch(self):
        '''
        Load lda and hdp documents to search from 'topics' folder. This will take the csv files from the topics folder
        and load the hdp and lda analyses and compile those topics and terms to create a wider search for terms 
        from relevant documents.
        '''
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
    
        path=os.path.join(pn,"topics")
        topics={}
   
        for filename in os.listdir(path):
            name=os.path.join(path,filename)
            with open(name,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                
                print(csvfile)
                
                for row in reader:
                    topic=row['Topic']
                    terms=row['Term']
                    
                    lst=[]
                    if topic in topics.keys():
                        lst=topics[topic]
                    
                    if terms in lst:
                        continue
                    
                    lst.append(terms)
                    topics[topic]=lst
                     
        
        return topics
         
       
    def searchContent(self, return_list, topics):
        '''
        Method will conduct tf-idf analysis on relevant text from terms in topics found in the search.
        return_list-- the list containing the relevant text
        topics-- the topics containing terms to be search
        '''
        termMap={}
        docFreq={}
        self.textL=[]
        textTracker={}
        
        for returnL in return_list:
            
           
            text=returnL['Text']
            
            totalLength=len(text)
            
            self.textL.append(totalLength)
            
            for topic in topics.keys():
                lst=topics[topic]
                
                for l in lst:
                    
                    t=text.lower()
                    
                    if totalLength==0:
                        continue
                  
                    n=float(t.count(str(l.lower()))/float(totalLength))
                    
                
                    df=0
                   
                    if n>0:
                        if l not in textTracker:
                            textTracker[l]=1
                            docFreq[l]=text
                        else:
                            tt=docFreq[l]
                            
                            if text!=tt:  
                                docFreq[l]=text
                                textTracker[l]=textTracker[l]+1
                        
                    ll=[]              
                    if l in termMap.keys():
                        ll=termMap[l]
                    
                    ll.append(n)
                    
                    termMap[l]=ll
        
        for tm in termMap.keys():
            
            ll=termMap[tm]
            
            if tm not in docFreq:
                continue
            
            df=textTracker[tm]
            
            newList=[]
            for l in ll:
                n=l
#               print(str(self.tC)+" : "+str(n)+" : "+str(df))
                
                l=n*np.log(float(self.tC)/float((df+1)))
                newList.append(l)
            
            termMap[tm]=newList
                
                       
#            terms[returnL['Code']]=termMap       
                
        
        return termMap   
    
    
    def printOutput(self, topics, terms,year): 
        '''
        Output results to output folder where the file is called terms_topics_(year).csv.
        topics-- the topics to output
        terms-- the terms to output
        year-- the given year for the file name output
        '''
        fieldnames = ['Topic','Term','Value','Text Length']
     
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]   
        filename=os.path.join(pn,'termAnalysis','term_topics'+str(year)+'.csv')
        
          
        with open(filename, 'wb') as csvf:
                writer = csv.DictWriter(csvf, fieldnames=fieldnames)

                writer.writeheader()
        
               
                for kk in terms.keys():
                        
                    vv=terms[kk]
                    v=float(np.sum(vv))/len(vv)
                        
                       
                    for tN in topics.keys():
                            
                        ts=topics[tN]
                            
                        if kk in ts:
                            writer.writerow({'Topic': str(tN),'Term':str(kk), 'Value':str(v),'Text Length':
                                             str(np.sum(self.textL))})         
                
   
    def run(self):
        ''''
        Method to run analysis using documents between given years (i.e., 2010-2015, with 2010 to 2014 inclusive)
        '''      
        year=int(raw_input("What year to start search:"))
        end=int(raw_input("To what year: "))
        matType=raw_input("What type of document: ")
        fll=raw_input("What terms to filter:  ")
        fllt=fll.split(",")
        flt=[]
        for f in fllt:
            flt.append(f)
        topics=self.loadSearch()
        return_list=self.retrieveContent(year,end,matType,flt)
        terms=self.searchContent(return_list, topics)
        self.printOutput(topics, terms, year)

''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    wp=WordPatternAnalysis()
    wp.run()