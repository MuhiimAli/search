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
        self.link_regex = '''\[\[[^\[]+?\]\]'''
        self.word_corpus = set()
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.parse()
        self.file_io = file_io
        
    def parse(self):
        for page in self.all_pages:#looping through all the pages
            text: str = page.find('text').text #getting the text of each page (as a str)
            page_tokens = re.findall(self.tokenization_regex,text)
            print(page_tokens[0])
            links = re.findall(self.link_regex, text)
            for word in page_tokens: #looping through a list of words
                if word in links:#if the word is link
                    sliced_links= handle_Links(links)
                    sliced_links_token = re.findall(self.tokenization_regex, sliced_links)
                    for word in sliced_links_token:
                        if word not in STOP_WORDS:
                            stemmed =nltk_test.stem(word)
                            self.word_corpus.add(stemmed)
                else:
                    if word not in STOP_WORDS:
                        stem =nltk_test.stem(word)
                        self.word_corpus.add(stem)
        print(self.word_corpus)
    # def ids_to_titles(self):
    #     ids_to_titles = {}
    #     for page in self.all_pages:
    #         title = str = page.find('title').text
    #         id: int = int(page.find('id').text)
    #         ids_to_titles[id] = title
    #         self.file_io.write_title_file(self.title_file, ids_to_titles)
    # def 
def handle_Links(links : list):
    for text in links:
        if "|" in text:
            sliced = text[2:-2]
            no_bar = sliced.split("|")
            return no_bar[1]
        else:
            sliced = text[2:-2]
            return sliced
           # link_list.append(sliced)
    #return link_list

  


vl = Indexer('our_wiki_files/test_tf_idf.xml')

