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

For given code, use the src folder, which contains the relevant packages described below.

<i>scrape</i>

The scraping modules relate to extracting data from the pdf files downloaded that deal with the primary text analyzed. Data are scraped and metadata and data from MPB_Source_Doc.csv are used to organize the Mongo database used. 

csvExtract: This module reads the MPB_Source_Doc.csv file using the readDates() method. There is a run() method that launches this module but readDates() is called in pdfScrape.py.

pdfScrape:  methods read() and inputToDatabase() read pdf text and input to the database respectively.The method read() produces a text file "content.txt" placed in the content folder, which has the text data from the files, that is then used to populate the Mongo database for the pdf files anlaysed in inputToDatabase().

readScrapedPDF:  method readText() reads the content.txt file and sends the information to pdfScrape.inputToDatabase(). The run() method controls the methods in the scrape package. 

<i>nlp</i>

The main LDA and HDP topic modeling methods are launched from here. The utilise Gensim's implementation of these methods. The module model.py controls the launching and application of LDA and HDP. The patternMatching.py module is used to guide filtering and organising of text to analyse.

model:  The run() method controls the utilising of methods in model.py and patternMatching.py. The run() method, once launched, will ask for the number of topics (used for LDA), any filters (e.g., 'beetle') for terms to search within texts. The default assumes 'dendroctonus','beetle'. Otherwise, users could also put no terms, which means there is no term to filter. Filtering means that sentences before, after, and containing the term will be included in the analysis. If no filter is chosen, then all text is analyzed. Filter terms are separated by a comma. This is also true for government material, where the type of government-related text are chose and indicated. No input means no input is applied, while one or more filters for government type could be applied (i.e., Congressional document, Legal news, GAO document, Federal agency document, Legal news, The White House document).

Texts are processed in the preProcsText() and process_texts() methods. These tokenize and remove stop words, etc. in preparation for the LDA and HDP analyses. Once the analysed corpus is created, then the LDA and HDP are used based on a given topic number used from the input. The end result will be output in the results folder called analysis_results for the hdp and lda models that looks at the term and topic values and evaluationTotal, which looks at the coherence score used to test the number of topics applied. The method also prints LDA_Visualization html files that are visualizations that can be adjusted to see what the LDA output looks like. 

patternMatching:  The only method used here is retrieveContent(), which also applies a filter to retrieve text desired. The basic point of this method is to get the desired text for analysis. The method is called within model.run().

<i>db</i>

filterBeetle:  module uses filterBeetleSentences() that filters are returns relevant sentences for the analysis. This is called by patternMatching.retrieveContent(). Sentences before, after, and within the desired (filtered) terms are returned.

filterGovernment:  module uses filterGovernmentType(), which is a method called by patternMatching.retrieveContent() and finds relevant government text to analyze. 

mongoConnection:  module gets relevant database from Mongo (assumed to be insectNLTK) and collection (also called insectNLTK).

<i>analysis</i>


countYears: module uses a run() method to launch loadData(), which counts the number of documents for given years and number of words for those years. The results are printed in output as year_numbers.csv.

searchMatch:  module is used to merge LDP and HDP results in loadSearch(), which are assumed to be placed in topics. Then the retrieveContent() method will do the tf-idf on terms found in topics. The output of this is in the termAnalysis folder. The analysis asks what year to start (inclusive) to what year to end (exclusive). The type of document is then asked, where the input expected are one of the type of documents (Congressional document, Legal news, GAO document, Federal agency document, Legal news, The White House document). Filter terms are similar to be before as discussed in model, where it is expected more than one term will be separated by a comma (e.g., beetle, bark, etc.).

termAnalysis:  module used to look at termAnalysis results based on years based on year intervals (inclusive start year and exclusive end year). A specific term is searched for the interval where the tf-idf score is returned. The module is launched in the run() method. 



















