# InsectNLTK

Note: This file contains code and data (pdfs) used in InsectNLTK test case. The pdf files included here are not all of the pds used in the article but reflect a sample of them. The full set of articles can be downloaded and obtained from relevant US government records referenced in the article. The python docs are included in the html_docs folder, which provides information about the modules and methods used. 

<b>Code</b>

The code is used for several different steps and analyses. First, there are a few external libraries needed to be installed in order to use InsectNLTK. These include:

NLTK 3.2+
Numpy 1.14+
Pymongo 3.6+
PyPDF2 1.26+
Pdftotext 2.1+
Matplotlib 2.1+
Gensim 3.3+
PyLDAvis 2.1+

<i>Scraping</i>

The scraping modules relate to extracting data from the pdf files downloaded that deal with the primary text analyzed. Data are scraped and metadata and data from MPB_Source_Doc.csv are used to organize the Mongo database used. 

csvExtract: This module reads the MPB_Source_Doc.csv file using the readDates() method. There is a run() method that launches this module but readDates() is called in pdfScrape.py.

pdfScrape:  methods read() and inputToDatabase() read pdf text and input to the database respectively.The method read() produces a text file "content.txt" placed in the content folder, which has the text data from the files, that is then used to populate the Mongo database for the pdf files anlaysed in inputToDatabase().

readScrapedPDF:  method readText() reads the content.txt file and sends the information to pdfScrape.inputToDatabase(). The run() method controls the methods in the scrape package. 

<i>Model</i>







