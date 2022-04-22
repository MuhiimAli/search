import xml.etree.ElementTree as et
import file_io
import nltk
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
import re
class Indexer:
    def __init__(self, xml_file : str, title_file : str):
        #what are the fields
        """
        :param xml_file: the name of the input file that the indexer will read in and parse
        :param title_file: maps document IDs to document titles
        :param doc_file: stores the rankings computed by PageRank
        :param worsds_file: stores the relevance of documents to words
        """
        self.xml_file = xml_file
        self.title_file = title_file
        # self.docs_file = docs_file
        # self.words_file = words_file
        self.tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        self.link_regex = '''\[\[[^\[]+?\]\]'''
        self.word_corpus = set()
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.file_io = file_io
        self.parse()
        self.ids_to_titles()
        
    docs_to_words_to_counts = {}  
    def parse(self):
        count = 0
        for page in self.all_pages:#looping through all the pages
            text: str = page.find('text').text #getting the text of each page (as a str)
            id: int = int(page.find('id').text)
            page_tokens = re.findall(self.tokenization_regex,text)
            links = re.findall(self.link_regex, text)
            for term in page_tokens: #looping through a list of words
                if term in links:#if the word is link
                    sliced_links= self.handle_Links(term)
                    sliced_links_token = re.findall(self.tokenization_regex, sliced_links)#tokenizes link texts
                    for word in sliced_links_token:
                        word_stem = self.remove_stop_words_and_stem(word)
                else: #if the word is not a link
                    word_stem= self.remove_stop_words_and_stem(term)
                if word_stem != None:
                        if word_stem not in self.docs_to_words_to_counts:
                            self.docs_to_words_to_counts[word_stem] = {}
                        if id not in self.docs_to_words_to_counts[word_stem]:
                            self.docs_to_words_to_counts[word_stem][id] = 0
                        self.docs_to_words_to_counts[word_stem][id]+=1
        print(self.docs_to_words_to_counts)
        """ treat linked text as words as well so that we can stem the linked test/remove stop/update maps """

    def handle_Links(self, term : str):
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
            return processed_word
            #print(processed_word)
            # if processed_word != None:

            # return processed_word
           # 

    def ids_to_titles(self):
        ids_to_titles_dict = {}
        for page in self.all_pages:
            title = str = (page.find('title').text).strip()
            id: int = int(page.find('id').text)
            ids_to_titles_dict[id] = title
            self.file_io.write_title_file(self.title_file, ids_to_titles_dict)
        print(ids_to_titles_dict)
    def term_frequency():
        pass
        
    



var = Indexer('our_wiki_files/dict_words_id_counts','indexer_output_files/titles')

