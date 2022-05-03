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
        wiki_tree = et.parse(self.xml_file) #loads the xml file into a tree
        root = wiki_tree.getroot()#get the root of the tree
        self.all_pages = root.findall('page')#this gets all the pages
        self.file_io = file_io
        self.word_to_id_to_count = {} #dictinary mapping words to doc ids to the amount of times a word appears in that specific doc
        self.all_page_ids = set() #set of all page ids
        self.weights_dict = {} #instantiating weights_dict which is a double dictionary that maps a doc id to another doc id which maps to the weight between the external doc id and the internal doc id
        self.id_to_links = defaultdict(set)
        self.title_to_page_id = {} #dictionary mapping page title to its id
        self.ids_to_titles = {} #dictionary mapping page id to its title
        self.id_to_highest_freq = {} #dictionary mapping a doc id to the number of occurances of the term with the highest frequency in the doc
        self.term_to_num_of_docs= {} #dictionary mapping each term to the number of documents it appears in
        self.idf_dict = {} #dictionary mapping word to its idf
        self.words_to_ids_to_relevance= {} #dictionary mapping words to internal dict of the ids of the docs it appears in mapped to the relevance score
        self.tf_dict= {} #dictionary mapping word/term to an internal dictionary that maps doc ids that the word appears in to the term frequency of the word in the specific doc
        self.ids_to_pageRank_dict= {} #dictionary mapping doc ids to its pagerank score 
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
        """Parses the inputted xml file, populates id_to_links, calls populate_word_to_ids_to_counts to populate word_to_ids_to_counts dict
        Parameters: none
        Returns:none
        """
        if len(self.all_pages) == 0:
            print("Empty wiki")
        for page in self.all_pages:#looping through all the pages
            page_title: str = (page.find('title').text).lower() #getting the title of each page.
            if page.find('text').text != None:
                page_text: str = (page.find('text').text).lower() #getting the text of each page (as a str)
            else:
                page_text: str = ''
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
        
        
        
    def compute_idf(self):
        """"Computing the idf of a word and populating idf_dict
        Parameters: none
        Returns: none
        """
        n = len(self.all_pages) #counting how many pages there are in total
        words= self.word_to_id_to_count.keys()#all the words in the dictionary
        for word in words: #looping through each word
            n_i = self.term_to_num_of_docs[word] #extracting and storing the number of documents a word appears in
            self.idf_dict[word] = math.log(n/n_i) #calculating idf and mapping word to idf in idf_dict

    
    def compute_term_frequency(self):
        """Calculates term frequency and populates tf_dict
        Param: none
        Returns: none
        """
        words= self.word_to_id_to_count.keys() #obtains all words that appear in documents
        for word in words: #looping through each word
            ids = self.word_to_id_to_count[word].keys() #obtains all ids of the docs that the current word appears in
            if  word not in self.tf_dict: 
                self.tf_dict[word]= {}
            for id in ids:
                if id not in self.tf_dict[word]:
                    self.tf_dict[word][id]= 0
                term_frequency = self.word_to_id_to_count[word][id]
                self.tf_dict[word][id]=term_frequency/self.id_to_highest_freq[id]

    def compute_term_relevance(self):
        """Computes term relevance and populating words_to_ids_to_relevance dict
        Param: none
        Returns: none
        """
        words=self.word_to_id_to_count.keys() #obtaining all words that appear in a document
        for word in words:
            ids = self.word_to_id_to_count[word].keys() #obtaining the ids of docs that the word appears in
            if word not in self.words_to_ids_to_relevance:
                self.words_to_ids_to_relevance[word] = {}
            for id in ids:
                if id not in self.words_to_ids_to_relevance[word]:
                    self.words_to_ids_to_relevance[word][id] = 0
                self.words_to_ids_to_relevance[word][id]= self.idf_dict[word] * self.tf_dict[word][id] #calculating term freq and mapping the internal dict doc id to term frequency
    def write_words_file(self):
        """Once we have term frequency and words_to_ids_to_relevance dict populated, the words file can be created
        Param: none
        Returns: none"""
        self.file_io.write_words_file(self.words_file, self.words_to_ids_to_relevance)
    
    def populate_weights_dict(self):
        """Calculating weights and populating weights_dict
        Param: none 
        Returns: none
        """
        n = len(self.all_page_ids) #obtaining the amount of pages in wiki
        e = 0.15 #instantiating e
        for j in self.all_page_ids: #looping thru all ids
            if j not in self.weights_dict: #mapping current id to internal dictionary
                self.weights_dict[j] = {}
            for k in self.all_page_ids: #looping through all ids again, followed are cases comparing docs
                if j == k: #case calculating/mapping the weight when a doc is linked to itself
                    self.weights_dict[j][k] = e/n
                elif k in self.id_to_links[j]: #calculating/mapping weight if j is liked to k
                    nk= len(self.id_to_links[j])
                    self.weights_dict[j][k] = e/n + (1-e)*1/nk
                elif  self.id_to_links[j] == set():#calculating/mapping weight if j is not linked to anything
                    nk = n-1
                    self.weights_dict[j][k] = e/n + (1-e)*1/nk
                else: #calculating/mapping weight if any other case
                    self.weights_dict[j][k] = e/n

    def euclidean_distance(self,page_rank: dict, r : dict):
        """Helper method calculating euclidean distance for final ranking
        Parameters:
        page_rank -- dictionary of ids mapped to pagerank value
        r-- dictionary that maps ids to pagerank value
        
        Returns: Euclidean Distance"""
        r_dict = list(r.items()) #getting the KV pairs and storing in tuple
        page_rank_dict = list(page_rank.items()) 
        r_array= np.array(r_dict) #converting dictionary to an array
        page_rank_array = np.array(page_rank_dict)
        dist = np.sqrt(np.sum(np.square(r_array-page_rank_array))) #computing euclidean distance
        return dist
    
    
    def compute_page_rank(self):
        """Computes PageRank values and populates ids_to_pageRank_dict
        Param: none
        Returns: none
        """
        r_dict = {}
        n = len(self.all_page_ids)
        delta = 0.001
        for id in self.all_page_ids:
            r_dict[id] = 0   #initializes every rank in r to be 0
            self.ids_to_pageRank_dict[id] = 1/n #initializes every rank in r' to be 1/n
        while self.euclidean_distance(self.ids_to_pageRank_dict,r_dict) > delta: #while loop runs and populates ids_to_pagerank_dict until the rank computation converges sufficiently
            r_dict = self.ids_to_pageRank_dict.copy() #setting r dict to be the current pagerank dict
            for j in self.all_page_ids: #looping through page ids
                self.ids_to_pageRank_dict[j] = 0 
                for k in self.all_page_ids:
                    self.ids_to_pageRank_dict[j] = self.ids_to_pageRank_dict[j] + self.weights_dict[k][j] * r_dict[k] #computing rank

    def write_docs_file(self):
        """Once we have the ranking values of our docs we can create and write the docs file"""
        self.file_io.write_docs_file(self.docs_file,self.ids_to_pageRank_dict)

    
if __name__ == "__main__":
    """Main method"""
    if len(sys.argv)-1:
        var = Index(*sys.argv[1:])
    else:
        print('Usage: <XML filepath> <titles filepath> <docs filepath> <words filepath>')
    

