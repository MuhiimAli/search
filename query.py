from sqlalchemy import true
import file_io
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
import re

class Query:
    def __init__(self,title_file: str, docs_file: str, words_file: str):
        self.file_io = file_io
        self.title_file = title_file
        self.docs_file = docs_file
        self.words_file = words_file
        self.read_title_file()
        self.read_docs_file()
        self.read_words_file()
    
        
    ids_to_titles = {}
    def read_title_file(self):
        self.file_io.read_title_file(self.title_file,self.ids_to_titles)
        print(self.ids_to_titles)

    ids_to_pageranks = {}
    def read_docs_file(self):
        self.file_io.read_docs_file(self.docs_file, self.ids_to_pageranks)
        print(self.ids_to_pageranks)
    
    words_to_doc_relevance = {}
    def read_words_file(self):
        self.file_io.write_words_file(self.words_file, self.words_to_doc_relevance)
        print(self.words_to_doc_relevance)





        pass




    def repl():
        pass
        # tokenization_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        # while true:
        #     user_input = input(' search>')
        #     query_tokens = re.findall(tokenization_regex,user_input)
        #     for word in query_tokens:
        #         if word not in STOP_WORDS:
        #             processed_word =nltk_test.stem(word)
        #             #return processed_word
        #             print(processed_word)

if __name__ == "__main__":
    pass
    query = Query('titles.txt','docs.txt','words.txt')


   
    #$ python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
    
