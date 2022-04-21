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
            links = re.findall(self.link_regex, text)
            for term in page_tokens: #looping through a list of words
                if term in links:#if the word is link
                    sliced_links= handle_Links(term)
                    sliced_links_token = re.findall(self.tokenization_regex, sliced_links)#tokenizes link texts
                    for word in sliced_links_token:
                        remove_stop_words_and_stem(self, word)
                else: #if the word is not a link
                   remove_stop_words_and_stem(self, term)
        print(self.word_corpus)




    # def ids_to_titles(self):
    #     ids_to_titles = {}
    #     for page in self.all_pages:
    #         title = str = page.find('title').text
    #         id: int = int(page.find('id').text)
    #         ids_to_titles[id] = title
    #         self.file_io.write_title_file(self.title_file, ids_to_titles)
    # def 
def handle_Links(term : str):
    if "|" in term:
        sliced = term[2:-2]
        no_bar = sliced.split("|")
        return no_bar[1]
    else:
        sliced = term[2:-2]
        return sliced
def remove_stop_words_and_stem(self, term: str):
    if term not in STOP_WORDS:
        processed_word =nltk_test.stem(term)
        self.word_corpus.add(processed_word)



vl = Indexer('our_wiki_files/test_parsing.xml')

