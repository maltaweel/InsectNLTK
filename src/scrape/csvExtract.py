'''
Class used to extract CSV data from MPB+Source_Doc.csv and match with pdf files that will be used to extract 
text.

Created on Jan 12, 2017

@author: 
'''
import os
import csv
from db.mongoConnection import mongo

class CSVExtract:
    
    def readCSV(self):
        
        '''
        Method to open csv file and read column and row data.
        '''
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0] 
        path=os.path.join(pn,"content")
        
        keyValues={}
        for filename in os.listdir(path):
            filename=os.path.join(path,filename)
            with open(filename,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cat=row['Category']
                    keyword=row['Keyword']
                    
                    if cat in keyValues:
                        l=keyValues[cat]
                        l.append(keyword)
                    
                    else:
                        l=[]
                        l.append(keyword)
                        keyValues[cat]=l
            
        return keyValues
    
    def readCSVpath(self,path1):
        
        '''
        Method used to read csv data from a given path input where the column and row data are read from the csv 
        file.
        path1-- the path to get the file read
        '''
        path=os.path.join(path1,"content")
        
        keyValues={}
        for filename in os.listdir(path):
            filename=path+'/'+filename
            with open(filename,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cat=row['Category']
                    keyword=row['Keyword']
                    
                    if cat in keyValues:
                        l=keyValues[cat]
                        l.append(keyword)
                    
                    else:
                        l=[]
                        l.append(keyword)
                        keyValues[cat]=l
            
        return keyValues

    def readDates(self):
        '''
        Method used to read MPB_Source_Docs.csv and extracting specific column data that are populated into MongoDB
        where the data are then matched to specific pdf files that contain the relevant text on mountain pine beetles.
        '''
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        filename=os.path.join(pn,'MPB_Source_Doc.csv')
        
        results={}
        with open(filename,'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    
                    code=row['Code #'].encode("utf-8")
                    title=row['Title']
                    html=row['HTML address'].encode("utf-8")
                    url=row['URL: doc address'].encode("utf-8")
                    dateAccessed=row['Date accessed'].encode("utf-8")
                    accessedBy=row['Accessed by'].encode("utf-8")
                    source=row['Source'].encode("utf-8")
                    day_month=row['Day/Month']
                    year=row['Year'].encode("utf-8")
                    material=row['Material type'].encode("utf-8")
                    govLevel1=row['Government Level 1'].encode("utf-8")
                    govLevel2=row['Government Level 2']
                    citation=row['Citation']
                    dbName=row['Database name'].encode("utf-8")
                    dbLink=row['Database link']
                    searchT=row['Search terms used']
                    filters=row['Filters applied']
                    other=row['Other Notes'].encode("utf-8")
                    
                    lsResults={'Code':code,'Title':title,'Html address':html,'URL':url,'Date Accessed':dateAccessed,'Accessed By':accessedBy,
                               'Source':source, 'Day/Month':day_month,'Year':year, 'Material':material,"Government Level 1":govLevel1,"Government Level 2":
                               govLevel2,'Citation':citation,'Database Name':dbName,'Database Link':dbLink,"Search Terms Used":searchT,
                               'Filters Applied':filters,'Other Notes':other}
                               
                    results[str(code)]=lsResults
                    
                    print(lsResults)
                    
                    
                    
                        
            
        return results

  
def run():
    '''
    The method to run the class.
    '''
    csvE=CSVExtract()
    csvE.readDates() 
     
''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    run() 
