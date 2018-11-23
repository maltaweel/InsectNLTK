'''
Created on Jan 25, 2017

Class used to find relevant texts and return the data used for topic modelling analysis. The data derive from the
MongoDB that contains the texts.

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
import wordninja
from db.mongoConnection import mongo
import gridfs

  
class PatternMatcher :
    
    
    def __init__(self):
         self.phrases=None
         self.bigram=None
    
    def tokenizeSentence(self,content):
        '''
        Method used to tokenize content into sentences.
        content-- the content to tokenize to sentences
        '''
        sent_tokenize_list = sent_tokenize(content)
        
        for s in sent_tokenize_list:
            s
            frq=FreqDist(s)
            print(frq)
            
            
            
    def findWholeWord(self,w):
        '''
        Method to find a whole word.
        w-- the word to find
        '''
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search        
            
    '''   
    def wordnetWords(self,word):
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(word) 
        finds=[]
        
    
        for syn in wn.synsets(token):
            for l in syn.lemmas():
                if word==l.name().lower():
                    continue
                
                finds.append(l.name())
                
        return finds'''
    
    '''
    def frequencyFinder(self,text, keyValues):
        fdist={}
        text=text.lower()
        
        for k in keyValues:
            l=keyValues[k]
            
            for ll in l:
                ll=ll.lower()
                ll=ll.replace('_'," ")
                tt=len(text.split(ll))
                
                if(tt==1):
                    tt=0
                    
                fdist[ll]=tt
      '''      
    #    word_token=word_tokenize(text)
    #    filtered_words = filter(lambda token: token not in stopwords.words('english'), word_token)
        
        #tx=text.split("and")
        
        
        #finder = BigramCollocationFinder.from_words(filtered_words)
        #finder2 = TrigramCollocationFinder.from_words(filtered_words)
        
        #fdist = FreqDist(word_token) 
    
       # new_data = (' '.join(w) for w in finder.ngram_fd)
       # new_data2 = (' '.join(w) for w in finder2.ngram_fd)
        
       # fdist.update(new_data)
       # fdist.update(new_data2)
                
       # return fdist
    
    def getCursor(self):
        '''
        Method to get the Mongo cursor to find the data for texts analyzed.
        '''
        m=mongoConnection.mongo()
        col=m.getCollection()
        
        cursor = col.find(no_cursor_timeout=True)
        
        return cursor
    
   
    def retrieveContentFrequencyResults(self,keyValues):
        '''
        Get content frequency for terms.
        keyValues-- terms to look for.
        '''
        cursor = self.getCursor()
        
        frqResults={}
        
        ii=0
        #for loop looking at retrieved documents
        
        
        for document in cursor:
            
            fResults={}
            
            code=document['Code']
            
            year=document['Year']
            day_month=document['Day/Month'] 
            material=document["Material"]
            govLevel1=document['Government Level 1']
            govLevel2=document['Government Level 2']
                
            try:
                content=document['content']
            except :
                content=''
           
            
            text=""
            
            for x in content:
                i=zlib.decompress(base64.b64decode(x)).lower()
#                stop = set(stopwords.words('english'))
#                for iii in i.lower():
#                    if iii not in stop:
#                        text=text+iii
                text=text+i
               
           
            text=text.decode('utf-8')   
            
            print(text)
            fdResult=self.frequencyFinder(text,keyValues)
            
            fResults['Year']=year
            fResults['Day/Month']=day_month
            fResults['Material']=material
            fResults['Government Level 1']=govLevel1
            fResults['Government Level 2']=govLevel2
            fResults['Frequency']=fdResult

        #    ff={}
        #    for kk in keyValues:
        #            terms=keyValues.get(kk)
                
        #            for t in terms:
        #                t=t.strip().lower()
        #                t=t.replace('_'," ")
        #                n=text.count(t)
        #                ff[t]=n
        #    fResults['Frequency']=ff
            fResults['Code']=code
            
            frqResults[str(ii)]=fResults
        
            ii+=1
    
            return frqResults
    
    
    def retrieveContent(self,flt,government):
#        flt={'Academic journal article '}
        '''
        Get content in the database, which includes the column output from the MPB_Source_Doc.csv file and the 
        data in the MongoDB, including the full text. Filter is used to include desired text. 
        
        flt-- filter applied to text to include desired text.
        government-- option to apply a given government type or not
        '''
        m=mongo()
        db=m.getDatabase()
        fs = gridfs.GridFS(db)
        
        cursor = self.getCursor()
        
        if len(government)>0:
            cursor=filterGovernment.filterGovernmentType(government, cursor)
            
        fb=filterBeetle.FilterBeetle()
        
        return_list=[]
        codeList=[]
        codeD={}
        ii=0
        #for loop looking at retrieved documents
        
        for document in cursor:
            ii+=1
            
            
            if ii>10:
                continue
            
            code=document['Code']
            dateAccess=document['Database Name']
            
            c=code+'.pdf'
           
            codeList.append(c)
            
            if code in codeD.keys():
                continue
            
            codeD[code]=code
            
            dbLink=''
            try:
                dbLink=document['Other Notes']
            except :
                dbLink=''
                
#            if ii==10:
#                break
            
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
            
#            print(str(ii)+ ' : '+year+" : "+text)
            
            returns={"Code":code, "Date Accessed":dateAccess,"DB Link":dbLink,
                    "Title":title, "Filter":filt, "Year":year, "Month":month,"Day":day,"Material":material,
                    "Gov Level 1":govLevel1,"Gov Level 2":govLevel2, "Text":text, "Search":search} 
            
            return_list.append(returns) 
            
            print(c)

        
        return return_list

    '''   
    def termsToMatch(self):
        
        cs=csvExtract.CSVExtract()
        
        keyValues=cs.readCSV()
        
        
        for k in keyValues:
            terms=keyValues.get(k)
            
            tms=[]
            for t in terms:
                f=self.wordnetWords(t)
                tms.extend(f)
            
            terms.extend(tms)
            keyValues[k]=terms
            
        return keyValues
    '''
    
    def termMatchingToPdfs(self):
        '''
        Method to output frequency counts of terms from pdf files.
        
        '''        
        keyValues=self.termsToMatch()
        freqResults=self.retrieveContentFrequencyResults(keyValues)
        
        filename=self.filenameToOutput()
        
        alreadyTerms={}
        with open(filename, 'wb') as csvfile:
            fieldnames = ['Code','Day/Month','Year','Category','Term', 'Material',"Government Level 1","Government Level 2",'Counts']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            
        
            for k in freqResults:
                fResults=freqResults[k]
            
                fTerms=fResults['Frequency']
                year=fResults['Year'].encode('utf-8').strip()
                code=fResults['Code'].encode('utf-8').strip()
                day_month=fResults['Day/Month']
                material=fResults['Material'].encode('utf-8').strip()
                govLevel1=fResults['Government Level 1'].encode('utf-8').strip()
                govLevel2=fResults['Government Level 2'].encode('utf-8').strip()
                for kk in keyValues:
                    terms=keyValues.get(kk)
                
                    for t in terms:
                        t=t.strip().lower()
                        t=t.replace('_'," ")
                        
                        print(kk+" : "+t)
                        res1=fTerms[t]
                        
                        
                        if alreadyTerms.has_key(str(code)+str(day_month)+str(year)+str(kk)+str(t)+str(res1)):
                            continue
                        writer.writerow({'Code':code,'Day/Month': day_month,'Year':year,'Category':kk,'Term':t,'Material': material,
                                         'Government Level 1':govLevel1, 'Government Level 2':govLevel2,'Counts': fTerms[t]})
                        alreadyTerms[str(code)+str(day_month)+str(year)+str(kk)+str(t)+str(fTerms[t])]=0
            

    def filenameToOutput(self):
        '''
        The file name to output the results
        filename-- the filename for the output of term frequencies.
        '''  
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        filename=os.path.join(pn,'output','termFrequencies.csv')
        
        return filename
    

#p=PatternMatcher()
#p.retrieveContent()