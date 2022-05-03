from locale import strcoll
from numpy import empty
#from sqlalchemy import all
import file_io
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
import re
import sys

class Query:
    def __init__(self, title_file: str, docs_file: str, words_file: str):
        """Constructor for query"""
        self.file_io = file_io
        self.title_file = title_file
        self.docs_file = docs_file
        self.words_file = words_file
        self.ids_to_titles = {} 
        self.ids_to_pageranks = {}
        self.words_to_doc_relevance = {}
        self.read_title_file()
        self.read_docs_file()
        self.read_words_file()
        self.repl()
    
    def read_title_file(self):
        self.file_io.read_title_file(self.title_file,self.ids_to_titles)
    def read_docs_file(self):
        self.file_io.read_docs_file(self.docs_file, self.ids_to_pageranks)
    def read_words_file(self):
        self.file_io.read_words_file(self.words_file, self.words_to_doc_relevance)
   
    def repl(self):
        """Repl method"""
        while True:
            query_set = set() #initializing a set to store processed query words
            user_input = input('search> ') #asking for user input
            if user_input == ':quit': #if the user inputs quit, the query closes out
                return 
            tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+''' 
            query_tokens = re.findall(tokenization_regex,user_input) #tokenizing the query
            for word in query_tokens: #looping through each word in query
                if word not in STOP_WORDS: #removing stop words
                    processed_word =nltk_test.stem(word) #stemming
                    query_set.add(processed_word) #adding processed words to query_set
            self.populate_total_relevance(query_set) #calling helper method
            
    
    def populate_total_relevance(self, query_set : list ):
        """Populates local id_to_total_relevance dictionary and uses local dictionary to rank pages

        Parameters:
        query_set -- list of processed words that were inputted to search

        Returns: none
        """
        id_total_relevance = {} #instantiating local dictionary for mapping ids to total relevance of the query
        for query_word in query_set: #looping through query set
            if query_word in self.words_to_doc_relevance: #if the processed query word exists in the wiki
                for id in self.words_to_doc_relevance[query_word]: #looping through the pageids
                    if id not in id_total_relevance: 
                            id_total_relevance[id]= 0
                    id_total_relevance[id]+=self.words_to_doc_relevance[query_word][id] #summing the relevance of each word in the query in each page
        all_keys = list(id_total_relevance.keys()) #obtaining all the ids of the docs in which query words appear
        self.rank_pages(all_keys, id_total_relevance) #calling helper method

    def rank_pages(self, all_keys: list, id_total_relevance: dict):
        """Prints search results based on if pagerank is used or not
        Parameters:
        all_keys -- list of ids of the docs in which query words appear
        id_total_relevance -- dictionary that maps all the ids of the docs that query words appear in to the total relevance of the entire query
        (in other words, the summation of the relevance of each query word in the doc)

        Returns: none

        Side Effects: produces an informative message if the query produces no results
        """
        if len(all_keys) == 0:
            print("No search results available. Try a different search!")
        if sys.argv[1] == '--pagerank' and len(sys.argv) - 1 == 4: #if the first argument is pagerank and the number of arguments is 4, then pagerank shuld be enabled
            #ask if we need to check the num of arguments here if we do it in main  method JEN JEN JEN 
            all_keys.sort(key = lambda x : id_total_relevance[x]*self.ids_to_pageranks[x], reverse = True) #sorting page ids based on their rank times total relevance, sorting from greatest to least value
            range_x = min(10, len(all_keys)) #setting the range of how many page results are printed
            for x in range(range_x): #looping through each page slot in the range
                print(str(x+1) + ' ' + self.ids_to_titles[all_keys[x]]) #printing the page results
        else: #if pagerank is not used in outputting results
            all_keys.sort(key = lambda x : id_total_relevance[x], reverse = True) #sorting page ids based on their total relevance, sorted from greates to least value
            range_x = min(10, len(all_keys)) 
            for x in range(range_x):
                print(str(x+1) + ' ' + self.ids_to_titles[all_keys[x]])#printing the page results
            
            
                    
if __name__ == "__main__":
    """Main method
    """
    if len(sys.argv) - 1 == 4 and  sys.argv[1] == '--pagerank': #checking if pagerank is being used for the search
        query = Query(*sys.argv[2:]) #instantiating the query
    elif len(sys.argv) - 1 !=4: #if the number of arguments is not 4 (if pagerank is not included)
        query = Query(*sys.argv[1:]) #Instantiating the query
    else:
        print('Usage:[--pagerank] <titleIndex> <documentIndex> <wordIndex>')
