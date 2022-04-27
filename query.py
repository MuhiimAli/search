from locale import strcoll
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
        self.read_title_file()
        self.read_docs_file()
        self.read_words_file()
        self.repl()
    
    ids_to_titles = {}
    def read_title_file(self):
        self.file_io.read_title_file(self.title_file,self.ids_to_titles)

    ids_to_pageranks = {}
    def read_docs_file(self):
        self.file_io.read_docs_file(self.docs_file, self.ids_to_pageranks)
    
    words_to_doc_relevance = {}
    def read_words_file(self):
        self.file_io.read_words_file(self.words_file, self.words_to_doc_relevance)
   
    def repl(self):
        query_set = set()
        while True:
            user_input = input('search>')
            tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            query_tokens = re.findall(tokenization_regex,user_input)
            for word in query_tokens:
                if word not in STOP_WORDS:
                    processed_word =nltk_test.stem(word)
                    query_set.add(processed_word)
            self.compute_query_relevance(query_set)

    
    def compute_query_relevance(self, query_set : list ):
        id_total_relevance = {}
        id_total_relevance_with_pageRak = {}
        for query_word in query_set:
            for id in self.words_to_doc_relevance[query_word]: #looping through the pageids
                if id not in id_total_relevance:
                        id_total_relevance[id]= 0
                id_total_relevance[id]+=self.words_to_doc_relevance[query_word][id]

        if self.page_rank == '-pagerank':
            total_relevance_lst = list(id_total_relevance.items())
            total_relevance_lst.sort(key=lambda x:x[1], reverse = True)
            # for x in range(5):
            #     total_relevance_lst.
        else:
            for id in id_total_relevance:
                if id not in id_total_relevance_with_pageRak:
                    id_total_relevance_with_pageRak[id] = 0
                id_total_relevance_with_pageRak[id] = id_total_relevance[id]*self.ids_to_pageranks[id]
            print(id_total_relevance_with_pageRak)
            
        















if __name__ == "__main__":
    query = Query('-pagerank','titles.txt','docs.txt','words.txt')
   # query = Query(sys.argv[1],sys.argv[2],sys.argv[3])


   
    #$ python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
    
