'''
Class used to filter and search for MPB within texts and also filter texts by given years.

Created on May 11, 2018

@author:
'''

from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class FilterBeetle:
    
    def __init__(self):
        #default filter terms
        self.filt=['dendroctonus','beetle']

    def filterBeetleSentences(self,text,flt):
        '''
        Method to filter beetle sentences from texts based on the sentence that contains the filter term 
        and sentence before and after.
        text-- text to search
        flt-- terms used to filter in searching within text.
        '''
        #terms to search
        if len(flt)>0:
            self.filt=flt
        
        #tokenize sentences
        tokens = sent_tokenize(text)
        
            
        previousT=''
        result=[]
        nextToken=False
        
        for t in tokens:
        
            if nextToken is True:
                result.append(t)

                nextToken=False
                continue
                
            for f in self.filt:
                if f in t:
#                    print(t)
                    result.append(t)
                    nextToken=True
                        
                    if previousT not in result and previousT!= '':
#                        print(previousT)
                        result.append(previousT)
                    
            previousT=t
             
        
        tex='' 
        tex=tex.join(result)
            
         
           
        return tex
    

    def filterByYear(self, return_list,year):
        '''
        Method filters text results by year and returns in a given list
        return_list-- list to search for relevant text by given year
        year-- year to search for given text
        '''
        return_results=[]
        
        for txt in return_list:
            y=txt['Year']
            
            if y == year:
                return_results.append(txt)
            
        return return_results
            
