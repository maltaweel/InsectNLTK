'''
Module to count the number of documents for a given year and the total number of words for those documents.

Created on Aug 21, 2018

@author: 
'''
import os
import csv

##container for results
countResults={}

def loadData():
    '''
    Method will load MPB_Source_Doc.csv and input the year and count for given documents.
    '''
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    path=pn

    filename='MPB_Source_Doc_Mark.csv'
    name=os.path.join(path,filename)
    
    results={}
   
    
    with open(name,'rU') as csvfile:
            reader = csv.DictReader(csvfile)
                
            for row in reader:
                year = row['Year']
                count = int(row['Count'])
                
                    
                if year in results.keys() and year in countResults.keys():
                    yv=results[year]
                    yv+=1
                    results[year]=yv
                    
                    cR=countResults[year]
                    countResults[year]=count+cR
                
                else:
                    results[year]=1
                    countResults[year]=count
    
    return results

def printResults(results):
    '''
    Method to print the results that count the number of documents and word counts for a given year.
    results--the results that contain the number of documents and word counts.
    '''
    fieldnames = ['Year','Number','Count']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0] 
    filename=os.path.join(pn,'output','year_numbers.csv')  
    
    
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for y in results.keys():
        
            v=results[y]
            c=countResults[y]
            
            writer.writerow({'Year': str(y),'Number':str(v), 'Count':str(c)})   

def run():
    '''
    The method to run the analysis.
    '''
    results=loadData()
    printResults(results)   
    print('done') 
     
''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    run()  
 