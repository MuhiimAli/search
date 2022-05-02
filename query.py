from locale import strcoll
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
    def __init__(self,page_rank: str, title_file: str, docs_file: str, words_file: str):
        self.file_io = file_io
        self.title_file = title_file
        self.docs_file = docs_file
        self.words_file = words_file
        self.page_rank = page_rank
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
        while True:
            query_set = set()
            user_input = input('search> ')
            if user_input == '' or ' ':
                print("Cannot search empty input. Please enter a word or different search input")
            if user_input == ':quit':
                return 
            tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            query_tokens = re.findall(tokenization_regex,user_input)
            for word in query_tokens:
                if word not in STOP_WORDS:
                    processed_word =nltk_test.stem(word)
                    query_set.add(processed_word)
            self.populate_total_relevance(query_set)
            
                

    
    def populate_total_relevance(self, query_set : list ):
        id_total_relevance = {}
        for query_word in query_set:
            if query_word in self.words_to_doc_relevance:
                for id in self.words_to_doc_relevance[query_word]: #looping through the pageids
                    if id not in id_total_relevance:
                            id_total_relevance[id]= 0
                    id_total_relevance[id]+=self.words_to_doc_relevance[query_word][id]
        all_keys = list(id_total_relevance.keys())
        self.rank_pages(all_keys, id_total_relevance)

    def rank_pages(self, all_keys: list, id_total_relevance: dict):
        if len(all_keys) == 0:
            print("No search results available. Try a different search!")
        if self.page_rank != '--pagerank':
            all_keys.sort(key = lambda x : id_total_relevance[x], reverse = True)
            range_x = min(10, len(all_keys))
            for x in range(range_x):
                print(str(x+1) + ' ' + self.ids_to_titles[all_keys[x]])
        else:
            all_keys.sort(key = lambda x : id_total_relevance[x]*self.ids_to_pageranks[x], reverse = True)
            range_x = min(10, len(all_keys))
            for x in range(range_x):
                print(self.ids_to_titles[all_keys[x]])
            
            
                    
        















if __name__ == "__main__":
    query = Query('our_wiki_files/test_query.xml', 'titlefiles/query1Titles', 'docfiles/query1Docs', 'wordfiles/query1Words')
#    query = Query(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


   
    #$ python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
    
