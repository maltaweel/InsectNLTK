'''
This module is generally used to control the pdf scraping of files and then inputting data to the database. It uses the pdfScrape 
module where it also then reads the relevant text input file that represents the scraped data.

Created on Jul 14, 2018

@author: mark
'''
import os
from pdfScrape import PDFScrape

def readText():
        '''
        Method reads contents.txt, which is the file assumed to contain the relevant text data from the pdf files.
        '''
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
 
        contents={}
        filename=os.path.join(pn,'content','contents.txt')
        
        with open(filename, "rb") as ff:
                text=ff.read()
                splits=text.split(":::Code")
                
                number=0
                for i in range(0,len(splits)):
                    tn=splits[i]
                    
                    if "_:::_" in tn: 
                        
                        tnt=tn.split("_:::_")
                        number=tnt[0]
                        number=number.replace(".PDF","")
                        number=number.replace(".pdf","")
                        
                        contents[number]=tnt[1]
                        
                
        return contents

def run():
    '''
    The method to run the module. This will scrape the pdfs and then input the data to the database in Mongo.
    '''
    pdfs=PDFScrape()  
    contents=pdfs.read()
    pdfs.printOut(contents)
    contents=readText()
    pdfs.inputToDatabase(contents)

     
''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    run()      


