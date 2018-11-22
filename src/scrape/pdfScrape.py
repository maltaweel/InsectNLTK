'''
Class used to scrape pdf data for relevant text and populate file to be used for MongoDB that contains the relevant
data for anlaysis. Generally the methods here are called from readScrapedPDF.py.

Created on Jan 12, 2017

@author: 
'''
import os
import PyPDF2
import base64
import zlib
import io
import pdftotext
import sys
from db import mongoConnection
from csvExtract import CSVExtract
from matplotlib.testing.jpl_units import day
import gridfs
import csv

class PDFScrape:
    
    def read(self):
        '''
        Method used to read a pdf file and extract its content.
        '''
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        

        #The data file path is now created where the data folder is referenced
        path=os.path.join(pn,'pdfs')

        
        contents={}
        for filename in os.listdir(path):
            f=filename
            filename=os.path.join(path,filename)
            
            pdf=''
#           pdf_file = open(filename, 'rb')
            with open(filename, "rb") as ff:
                print(ff)
                pdf = pdftotext.PDF(ff)
            
            content=[]
            for pd in pdf:
                content.append(pd)

            contents[f.split(".pdf")[0]]=content
 
        return contents
    
    
    def printOut(self,contents):
        '''
        Method used to print out text from pdfs to a text file which will then be read. This is so that it is easier for
        the data entry into the database and to certify all relevant data are extract from the pdfs.
        contents-- the pdf file contents to extract text from.
        '''
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        file1=os.path.join(pn,'content','contents.txt')
        print(file1)
        with open(file1, 'wb') as tfile:
            
            kys=contents.keys()
            
            for f in kys:
                content=contents[f]
                
                str1 = ":::Code "+f+"_:::_"+''.join(content)
                str1=str1.encode("utf-8")
                tfile.write(str1)
    
    '''
    def readId(self,i_d):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        filename=pn+'/pdfs/'+i_d+".pdf"
        try:
            print(filename)
            pdf_file = open(filename, 'rb')
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()
            content=[]
            for i in range(number_of_pages):
                page = read_pdf.getPage(i)
                page_content = page.extractText()
                print(page_content)
                page_content=page_content.encode('utf-8')
                content.append(page_content.encode('zlib_codec').encode('base64_codec'))
            
        
            pdf_file.close()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return ''
        
        return content
    '''
    def inputToDatabase(self,contents):
        '''
        Method to intput information from pdf files into MongoDB. The method takes the csv metadata that was placed in 
        the database earlier and then matches to the pdf files data.
        
        contents-- the contnets to input into the database
        '''
        mongo=mongoConnection.mongo()
        collection=mongo.getCollection()
        db=mongo.getDatabase()
        fs = gridfs.GridFS(db)
        
        
        csvE=CSVExtract()
        results=csvE.readDates()
        
        
        ky=contents.keys()
        for k in ky:
            ct=contents.get(k)
            print(k)
            dates=results[k.strip()]
          
                    
            code=dates['Code']
            title=dates['Title']
            year=dates['Year']
                
            day_month=dates['Day/Month']
            
            day=''
            month=''
            if day_month != '':
                
                if len(day_month.split("/"))>1:
                    day=day_month.split('/')[1]
                    month=day_month.split("/")[0]
                
                else:
                    month=day_month
                    
            material=dates['Material']
            databaseName=dates['Database Name']
            searchTerm=dates['Search Terms Used']
            filters=dates['Filters Applied']
            otherNotes=dates['Other Notes']

            govLevel1=dates['Government Level 1']
            govLevel2=dates['Government Level 2']
            
            print(year+" : "+govLevel1+" : "+code) 
            
            str1=ct
            
            a = fs.put(str1) 
            post = {
                "Content":a,
                "Code":code,
                "Title":title,
                "Year": year,
                "Month":month,
                "Day":day,
                "Material":material,
                "Government Level 1":govLevel1,
                "Government Level 2":govLevel2,
                "Database Name":databaseName,
                "Search Term":searchTerm,
                "Filters":filters,
                "Other Notes":otherNotes
                }
            
            collection.insert_one(post)
    '''
    def updateDBWithPDFs(self):
        mongo=mongoConnection.mongo()
        collection=mongo.getCollection()
        
        cursor = collection.find({})
    
        for document in cursor:
            i_d=document['Code']
            content=self.readId(i_d)
            
            if(content!=''):
                document['content']=content
                collection.update_one({"_id": document["_id"]}, {"$set": {"content": content}})
            print(i_d)
            
        cursor.close()  
    '''
def run():
    '''
    The method to run the class.
    '''
    pdf=PDFScrape()
    contents=pdf.read()
    pdf.printOut(contents)
#   pdf.inputToDatabase(contents)

     
''''
The main to launch this class for merging lda and hdp terms and topics
'''
if __name__ == '__main__':
    run()           

