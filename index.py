import math
import xml.etree.ElementTree as et
import file_io
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
import re
import sys

class Index:
    def __init__(self, xml_file : str, title_file : str, words_file: str):
        """
        :param xml_file: the name of the input file that the indexer will read in and parse
        :param title_file: maps document IDs to document titles
        :param doc_file: stores the rankings computed by PageRank
        :param worsds_file: stores the relevance of documents to words
        """
        self.xml_file = xml_file
        self.title_file = title_file
        # self.docs_file = docs_file
        self.words_file = words_file
        self.tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        self.link_regex = '''\[\[[^\[]+?\]\]'''
        self.word_corpus = set()
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.file_io = file_io
        self.populate_ids_to_titles()
        self.populate_title_to_page_id()
        self.parse()
        self.ids_with_no_link()
        self.populate_id_to_set_of_ids()
        self.compute_n_i()
        self.compute_idf()
        self.populate_id_to_most_freq_count()
        self.compute_term_frequency()
        self.compute_term_relevance()
        self.write_words_file()
        
    word_to_id_to_count = {} 
    all_page_titles_set = set()
    all_page_ids = set()
    def parse(self):
        for page in self.all_pages:#looping through all the pages
            page_text: str = (page.find('text').text).lower() #getting the text of each page (as a str)
            page_title: str = (page.find('title').text).lower() #getting the title of each page.
            id: int = int(page.find('id').text)
            self.all_page_ids.add(id) #keeps track of all the page ids
            page_tokens = re.findall(self.tokenization_regex,page_title +' '+ page_text)
            links = re.findall(self.link_regex, page_text)
            self.all_page_titles_set.add(page_title) #keeps track of all the page titles
            for term in page_tokens: #looping through a list of words
                if term in links:#if the word is link
                    self.ids_with_links_set.add(id) #keeps track of all the ids with links
                    sliced_page_links = self.handle_Links(term,True)
                    self.populate_id_to_set_of_titles(id, sliced_page_links)
                    sliced_text_links= self.handle_Links(term, False)
                    sliced_links_token = re.findall(self.tokenization_regex, sliced_text_links)#tokenizes link texts
                    for word in sliced_links_token:
                        word_stem = self.remove_stop_words_and_stem(word)
                        self.populate_word_to_ids_to_counts(word_stem, id)
                else: #if the word is not a link
                    word_stem= self.remove_stop_words_and_stem(term)
                    self.populate_word_to_ids_to_counts(word_stem, id)
                

        # print(self.word_corpus)
        # print(self.word_to_id_to_count)
    ids_with_links_set = set()
    def ids_with_no_link(self):
        for ids in self.all_page_ids: #looping through all the page_titles
            if ids not in self.ids_with_links_set: #looping through all the processed links
                copy_titles= self.all_page_titles_set.copy()
                copy_titles.remove(self.ids_to_titles[ids])
                self.page_id_to_set_of_titles[ids] = copy_titles

    page_id_to_set_of_titles = {}
    def populate_id_to_set_of_titles(self, id :int, sliced_page_links : str):
        if id not in self.page_id_to_set_of_titles:
            self.page_id_to_set_of_titles[id] =set()
        #if self.ids_to_titles[id] in self.all_page_titles_set:
        self.page_id_to_set_of_titles[id].add(sliced_page_links)
    id_to_set_of_ids = {}
    def populate_id_to_set_of_ids(self):
        for id in self.page_id_to_set_of_titles.keys():
            if id not in self.id_to_set_of_ids:
                self.id_to_set_of_ids[id] = set()
            for title in self.page_id_to_set_of_titles[id]:
                #ignores if the page_links to itself or to a page that is not in the corpus
               if title in self.all_page_titles_set and self.ids_to_titles[id] != title:  
                self.id_to_set_of_ids[id].add(self.title_to_page_id[title.strip()])
        print(self.page_id_to_set_of_titles)
        print(self.id_to_set_of_ids)
       
    title_to_page_id = {}
    def populate_title_to_page_id(self):
        for page in self.all_pages:
            title: str = ((page.find('title').text).strip()).lower()
            id: int = int(page.find('id').text)
            self.title_to_page_id[title] = id
        #print(self.title_to_page_id)
    ids_to_titles = {}
    def populate_ids_to_titles(self):
        for page in self.all_pages:
            title: str = ((page.find('title').text).strip()).lower()
            id: int = int(page.find('id').text)
            self.ids_to_titles[id] = title
            self.file_io.write_title_file(self.title_file, self.ids_to_titles)
        #print(self.ids_to_titles)

    def handle_Links(self, term : str, page_link : bool):
        if "|" in term:
            sliced = term[2:-2]
            no_bar = sliced.split("|")
            if page_link == True:
                return no_bar[0]
            else:
                return no_bar[1]
        else:
            sliced = term[2:-2]
            return sliced

    def remove_stop_words_and_stem(self, term: str):
        if term not in STOP_WORDS:
            processed_word =nltk_test.stem(term)
            self.word_corpus.add(processed_word)
            return processed_word

    def populate_word_to_ids_to_counts(self, word_stem: str, id : int):
        if word_stem != None:
            if word_stem not in self.word_to_id_to_count:
                self.word_to_id_to_count[word_stem] = {}
            if id not in self.word_to_id_to_count[word_stem]:
                self.word_to_id_to_count[word_stem][id] = 0
            self.word_to_id_to_count[word_stem][id]+=1

    id_to_highest_freq = {}
    def populate_id_to_most_freq_count(self):
        words= self.word_to_id_to_count.keys()
        for word in words:
            ids= self.word_to_id_to_count[word].keys()
            for id in ids:
                if id not in self.id_to_highest_freq:
                    self.id_to_highest_freq[id] = 0
                self.id_to_highest_freq[id] = max(self.id_to_highest_freq[id],\
                    self.word_to_id_to_count[word][id])
        #print(self.id_to_highest_freq)
        
    term_to_num_of_docs= {}
    def compute_n_i(self):
        words=  self.word_to_id_to_count.keys()
        for word in words:
            id_list = self.word_to_id_to_count[word].keys() #getting the id associated with each word
            for id in id_list:
                if word not in self.term_to_num_of_docs:
                    self.term_to_num_of_docs[word] = 0
                self.term_to_num_of_docs[word]+=1
        #print(self.term_to_num_of_docs)
            
    idf_dict = {}
    def compute_idf(self):
        n = len(self.all_pages)
        words= self.word_to_id_to_count.keys()#all the words in the corpus
        for word in words:
            n_i = self.term_to_num_of_docs[word]
            self.idf_dict[word] = math.log(n/n_i)
        #print(self.idf_dict)

    tf_dict= {}
    def compute_term_frequency(self):
        words= self.word_to_id_to_count.keys()
        for word in words:
            ids = self.word_to_id_to_count[word].keys()
            if  word not in self.tf_dict:
                self.tf_dict[word]= {}
            for id in ids:
                if id not in self.tf_dict[word]:
                    self.tf_dict[word][id]= 0
                term_frequency = self.word_to_id_to_count[word][id]
                self.tf_dict[word][id]=term_frequency/self.id_to_highest_freq[id]
        #print(self.tf_dict)
    
    words_to_ids_to_relevance= {}
    def compute_term_relevance(self):
        words=self.word_to_id_to_count.keys()
        for word in words:
            ids = self.word_to_id_to_count[word].keys()
            if word not in self.words_to_ids_to_relevance:
                self.words_to_ids_to_relevance[word] = {}
            for id in ids:
                if id not in self.words_to_ids_to_relevance[word]:
                    self.words_to_ids_to_relevance[word][id] = 0
                self.words_to_ids_to_relevance[word][id]= self.idf_dict[word] * self.tf_dict[word][id]
        #print(self.words_to_ids_to_relevance)
        
        

    def write_words_file(self):
        self.file_io.write_words_file(self.words_file, self.words_to_ids_to_relevance)

    
# if __name__ == "__main__":
#     var = Index(sys.argv[1],sys.argv[2],sys.argv[3])
#     pass

        

var = Index('our_wiki_files/testing_weights(gradescope)','indexer_output_files/titles', 'indexer_output_files/words')
    