import math
import xml.etree.ElementTree as et
import file_io
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
import numpy as np
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
from collections import defaultdict
import re
import sys


class Index:
    def __init__(self, xml_file : str, title_file : str, docs_file: str, words_file: str):
        """Main method, initializes global dictionaries 
        Parameters:
        :param xml_file: the name of the input file that the indexer will read in and parse
        :param title_file: maps document IDs to document titles
        :param doc_file: stores the rankings computed by PageRank
        :param words_file: stores the relevance of documents to words

        Returns: none

        Throws: none
        """
        self.xml_file = xml_file
        self.title_file = title_file
        self.docs_file = docs_file
        self.words_file = words_file
        self.tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        self.link_regex = '''\[\[[^\[]+?\]\]'''
        #self.word_corpus = set()
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.file_io = file_io
       # self.populate_ids_to_titles()
        self.word_to_id_to_count = {} 
        self.all_page_ids = set()
        self.weights_dict = {} #creating weights dict
        self.id_to_links = defaultdict(set)
        self.title_to_page_id = {}
        self.ids_to_titles = {}
        self.id_to_highest_freq = {}
        self.term_to_num_of_docs= {}
        self.idf_dict = {}
        self.words_to_ids_to_relevance= {}
        self.tf_dict= {}
        self.ids_to_pageRank_dict= {}
        self.populate_title_page_id()
        self.parse()
        self.populate_weights_dict()
        self.compute_page_rank()
        self.compute_most_freq_count_and_n_i()
        self.compute_idf()
        self.compute_term_frequency()
        self.compute_term_relevance()
        self.write_docs_file()
        self.write_words_file()
        self.write_title_file()
    
        
   
    def parse(self):
        """Parses the inputted xml file
        Parameters:
        Returns:
        """
        for page in self.all_pages:#looping through all the pages
            page_text: str = (page.find('text').text).lower() #getting the text of each page (as a str)
            page_title: str = (page.find('title').text).lower() #getting the title of each page.
            id: int = int(page.find('id').text)
            self.all_page_ids.add(id) #keeps track of all the page ids
            page_tokens = re.findall(self.tokenization_regex,page_title +' '+ page_text)
            links = re.findall(self.link_regex, page_text)
            for term in page_tokens: #looping through a list of words
                if term in links:#if the word is link
                    sliced_address = self.handle_Links(term,True)
                    if sliced_address!= self.ids_to_titles[id] and sliced_address in self.title_to_page_id:
                        self.id_to_links[id].add(self.title_to_page_id[sliced_address])
                    sliced_text_links= self.handle_Links(term, False)
                    sliced_links_token = re.findall(self.tokenization_regex, sliced_text_links)#tokenizes link texts
                    for word in sliced_links_token:
                        processed_link_text = self.remove_stop_words_and_stem(word)
                        self.populate_word_to_ids_to_counts(processed_link_text, id)
                else: #if the word is not a link
                    processed_link_text= self.remove_stop_words_and_stem(term)
                    self.populate_word_to_ids_to_counts(processed_link_text, id)

        #print(self.word_corpus)
        print(self.id_to_links)

   #populating both title title_to_page_id and ids_to_titles at the same time increases efficiency as we don't have to loop through the pages twice for both dict
    def populate_title_page_id(self): 
        """Populates title_to_page_id and ids_to_titles dictionaries

        Parameters: none
        Returns: none
        Throws: none
        """
        for page in self.all_pages: #looping through all pages
            title: str = ((page.find('title').text).strip()).lower()  #getting title
            id: int = int(page.find('id').text)
            self.title_to_page_id[title] = id #mapping title to id
            self.ids_to_titles[id] = title #mapping id to title
        
    
    def write_title_file(self):
        """Writes in a file for the titles
        Parameters: none
        Returns: none
        Throws: none
        """
        self.file_io.write_title_file(self.title_file, self.ids_to_titles)


    def handle_Links(self, term : str, page_link : bool):
        """Processes words in text that are links

        Parameters:
        term -- word that is a link
        page_link -- boolean if the word returned should be the link address or the link text
        
        Return:
        no_bar or sliced -- a string of the processed link
        
        Throws: none
        """
        if "|" in term: #if text of link is different than the page it links too
            sliced = term[2:-2] #obtaining the word from term without the link brackets by extracting all letters except the first and last two characters
            no_bar = sliced.split("|") #splitting the word along the bar to obtain a list of the word(s) before and after the bar
            if page_link == True: #if the desired returned word is the link address
                return no_bar[0] #return the left word(s) of the bar
            else:
                return no_bar[1] #return the right word(s) of the bar
        else: #if text of link is the same as the page it links too
            sliced = term[2:-2] 
            return sliced

    def remove_stop_words_and_stem(self, term: str):
        """If the argument is not a stop word, the word is reduced to the base root/stem of the word
        Parameters:
        term -- string to be stripped of stop words and stemmed 
        Returns: string of processed input string
        Throws: none
        """
        if term not in STOP_WORDS: #if the word is not a stop word, the word is stemmed
            processed_word = nltk_test.stem(term)
            #self.word_corpus.add(processed_word)
            return processed_word

    def populate_word_to_ids_to_counts(self, word_stem: str, id : int):
        """Fills the double dictionary that maps words to an internal dictionary of ids mapped to the word count
        Parameters:
        word_stem -- string of the stemmed word, key of the outer dictionary
        id -- integer id of the doc that the word_stem appears in
        Returns: none
        Throws: none
        """
        if word_stem != None: #if word is not null/none
            if word_stem not in self.word_to_id_to_count: #if word is not yet put in outer dictionary
                self.word_to_id_to_count[word_stem] = {} #creating internal dictionary that the word_stem maps to
            if id not in self.word_to_id_to_count[word_stem]: #if id not yet in the internal dictionary that word_stem maps to
                self.word_to_id_to_count[word_stem][id] = 0 #id mapped to 0
            self.word_to_id_to_count[word_stem][id]+=1 #increasing count by 1

    
    def compute_most_freq_count_and_n_i(self):
        """Populates term_to_num_of_docs dictionary and id_to_highest_freq dictionary
        Parameters: none
        Returns: none
        Throws: none
        """
        words = self.word_to_id_to_count.keys() #extracting all words in word_to_id_to_count
        for word in words: #looping thru each word
            ids= self.word_to_id_to_count[word].keys() #extracting all ids
            for id in ids: #looping thru each id
                if word not in self.term_to_num_of_docs:
                    self.term_to_num_of_docs[word] = 0
                self.term_to_num_of_docs[word]+=1 #counting each doc that the term appears in
                if id not in self.id_to_highest_freq:
                    self.id_to_highest_freq[id] = 0
                self.id_to_highest_freq[id] = max(self.id_to_highest_freq[id],\
                    self.word_to_id_to_count[word][id]) #mapping id to the highest frequency by comparing the value that the id is currently mapped to to the count of the current word
        #print(self.id_to_highest_freq)
        #return id_to_highest_freq
        
        
    def compute_idf(self):
        n = len(self.all_pages)
        words= self.word_to_id_to_count.keys()#all the words in the corpus
        for word in words:
            n_i = self.term_to_num_of_docs[word]
            self.idf_dict[word] = math.log(n/n_i)

        #return idf_dict
        # print(self.idf_dict)

    
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
        #return tf_dict
        #print(self.tf_dict)
    
    
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


    
    
    def populate_weights_dict(self): #populating weights_dict
        n = len(self.all_page_ids)
        e = 0.15
        for j in self.all_page_ids: #looping thru all ids
            if j not in self.weights_dict:
                self.weights_dict[j] = {}
            for k in self.all_page_ids:
                if k not in self.weights_dict[j]:
                    self.weights_dict[j][k] = {}
                if j == k:
                    self.weights_dict[j][k] = e/n
                elif k in self.id_to_links[j]: 
                    nk= len(self.id_to_links[j])
                    self.weights_dict[j][k] = e/n + (1-e)*1/nk
                elif  self.id_to_links[j] == set():
                    nk = n-1
                    self.weights_dict[j][k] = e/n + (1-e)*1/nk
                else:
                    self.weights_dict[j][k] = e/n

      
      
        #print(self.weights_dict)
    

    def euclidean_distance(self,page_rank: dict, r : dict):
        r_dict = list(r.items())
        page_rank_dict = list(page_rank.items())
        #converting dictionary to an array
        r_array= np.array(r_dict)
        page_rank_array = np.array(page_rank_dict)
        dist = np.sqrt(np.sum(np.square(r_array-page_rank_array)))
        return dist

    
    
    def compute_page_rank(self):
        r_dict = {}
        n = len(self.all_page_ids)
        for id in self.all_page_ids:
            r_dict[id] = 0   #initializes every rank in r to be 0
            self.ids_to_pageRank_dict[id] = 1/n #initializes every rank in r' to be 1/n
        while self.euclidean_distance(self.ids_to_pageRank_dict,r_dict) > 0.001:
            r_dict = self.ids_to_pageRank_dict.copy()
            for j in self.all_page_ids:
                self.ids_to_pageRank_dict[j] = 0
                for k in self.all_page_ids:
                    self.ids_to_pageRank_dict[j] = self.ids_to_pageRank_dict[j] + self.weights_dict[k][j] * r_dict[k]
        print('ids_to_pageRank' + str(self.ids_to_pageRank_dict))
        #return self.ids_to_pageRank_dict
        #pass

    def write_docs_file(self):
        self.file_io.write_docs_file(self.docs_file,self.ids_to_pageRank_dict)
        #pass
    
if __name__ == "__main__":
    var = Index(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4])
    

# # time python3 index.py wikis/MedWiki.xml titles.txt docs.txt words.txt
#time python3 index.py our_wiki_files/test_word_relevance_2.xml titles.txt docs.txt words.txt
# # 
        

# var = Index('wikis/MedWiki.xml', 'titles.txt','docs.txt', 'words.txt')
# #     # python3 index.py wikis/SmallWiki.xml titles.txt docs.txt words.txt

