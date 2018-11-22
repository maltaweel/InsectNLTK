'''
Module used to look for a specific term (input data from user) within the data file(s) in termAnalysis. The result is
an aggregation for terms' tf-idf scores for given year intervals.

Created on Aug 21, 2018

@author: 
'''

import os
import csv

#container for the text lengths
length={}

#dictionary containing the year and positioning of that year used for outputting the data
position={'1880':"0",'1960':'1','1965':'2','1970':'3','1975':'4','1980':'5','1985':"6",'1990':'7','1995':'8','2000':'9','2005':'10',
          '2010':'11','2015':'12'}

def loadData():
    
    '''
    Method to load data to analyze the tf-idf value and text length. This method aggregates terms so that a total 
    tf-idf for terms for each year interval is created.
    '''
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    path=os.path.join(pn,'termAnalysis')
    topics={}
    
   
    for filename in os.listdir(path):
        name=os.path.join(path,filename)
        
        with open(name,'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            
           
            
            smallValue={}  
            textL=0
            for row in reader:
#                topic=row['Topic']
                term=row['Term']
                value=row['Value']
                textL=row['Text Length']
            
            
               
                print(term)
                
                smallValue[term]=value
                
            length[filename]=textL    
            topics[filename]=smallValue         
            
    return topics
    
def findTermAndPrint(term,topics,years):
    '''
    Method printing the given in output for term used to assess topics and based on years there are data.
    term-- the term searched in the loaded data.
    topics--the topics the term is associated with
    years-- possible years where there are data
    '''
    fieldnames = ['Year','Position','Term','Value','Word Length']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]   
    filename=os.path.join(pn,'output','found_term_'+term+'.csv')
    
    years=sorted(years)
    
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
        

        for topic in topics.keys():
            lenG=length[topic]
            values=topics[topic]
        
            yearToAdd=0
            thisYear=0
            for yy in years:
                if yy in topic:
                    yearToAdd=int(yy)+4
                    thisYear=int(yy)
            
            stringE=''
            stringE=str(yearToAdd)
            stringE=stringE[3-4]
           
            stringT=str(thisYear)+"-"+stringE
            
            if thisYear==1880:
                stringT="<1960"
            
            if thisYear==2015:
                stringT="2015<=" 
            
            value=0
            if term in values.keys():
                value=values[term]
    
            if thisYear==0:
                continue 
            
            writer.writerow({'Year': str(stringT),'Position':str(position[str(thisYear)]),'Term':str(term),'Value':str(value),
                                 'Word Length':str(lenG)})
        
def run():
    '''
    Method used to run the term search in the given data files that have tf-idf scores and topic/term data.
    '''   
    years=['1880','1960','1965','1970','1975','1980','1985','1990','1995','2000','2005','2010','2015']
    term=raw_input('Enter term searched: ')
    topics=loadData()
    findTermAndPrint(term, topics,years)    
    
''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    run()
