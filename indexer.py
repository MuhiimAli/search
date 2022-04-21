import xml.etree.ElementTree as et
import file_io
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
import re
class Indexer:
    def __init__(self, xml_file):
        #what are the fields
        """
        :param xml_file: the name of the input file that the indexer will read in and parse
        :param title_file: maps document IDs to document titles
        :param doc_file: stores the rankings computed by PageRank
        :param worsds_file: stores the relevance of documents to words
        """
        self.xml_file = xml_file
        # self.title_file = title_file
        # self.docs_file = docs_file
        # self.words_file = words_file
        self.tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        self.word_corpus = set()
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.parse()
        self.file_io = file_io
        
    def parse(self):
        for page in self.all_pages:
            text: str = page.find('text').text #this gets the text of each page (as a str)
            page_tokens = re.findall(self.tokenization_regex,text)
            print(page_tokens)
            for word in page_tokens:
                #think about link edge cases
                print(word)
                if word in STOP_WORDS:
                    #print(word)
                    page_tokens.remove(word)#removing unimportant words
                else:
                    #print(word)
                    stem =nltk_test.stem(word)
                    self.word_corpus.add(stem)
            #print(stem)
            

    # def ids_to_titles(self):
    #     ids_to_titles = {}
    #     for page in self.all_pages:
    #         title = str = page.find('title').text
    #         id: int = int(page.find('id').text)
    #         ids_to_titles[id] = title
    #         self.file_io.write_title_file(self.title_file, ids_to_titles)
    # def 

  

vl = Indexer('wikis/test1_tf_idf.xml')
vl.parse()