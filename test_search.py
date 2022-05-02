import pytest
from index import Index
from query import Query

#INDEX UNIT TESTS
#TESTS PARSE METHOD
def test_parse():
    index1 = Index('our_wiki_files/parsing.xml', 'titlesParsing', 'docsParsing', 'wordsParsing')
    assert index1.all_page_ids == {1,2,3}
    assert index1.word_to_id_to_count == {'author': {3: 1},'categori': {2: 1},'cs200': {3: 1},'determin': {2: 1, 3: 1},'document': {1: 1, 2: 1},'gorgeou': {2: 1}, 'king': {3: 1},'list': {1: 1},'philosophi': {1: 1, 2: 1},'process': {1: 1}, 'relev': {2: 1},'scienc': {1: 1, 2: 1},'term': {1: 1, 2: 1},'xml': {3: 1},"king'": {3: 1},"xml'": {1: 1}}
    assert index1.id_to_links == {1: {2}, 2: {3}, 3: set()}
    
    # index2 = Index()

def test_handle_links():
    index1 = Index('wikis/SmallWiki.xml', 'titlesSmallWiki', 'docsSmallWiki', 'wordsSmallWiki')
    

def test_remove_stop_words_and_stem():
    #only one-word inputs because this function is only called when for-each looping through words
    index1 = Index('our_wiki_files/parsing.xml', 'titlesParsing', 'docsParsing', 'wordsParsing')
    assert index1.remove_stop_words_and_stem('a') == None
    assert index1.remove_stop_words_and_stem('and') == None #words will always be lowercase due to .lower method call earlier in parse methd
    assert index1.remove_stop_words_and_stem('sci') == 'sci'


# def test_write_docs_files(): Do I need this?
#     pass

def test_ids_to_titles_and_title_to_page_id():
    pass


def test_ids_to_links():
    pass

def test_id_to_highest_freq():
    pass

def test_term_to_num_docs():
    pass

#TEST TERM TO DOC RELEVANCE
def test_words_to_ids_to_relevance():
    pass

#TEST WEGIHTS
def test_weights_dict():
    pass

#TESTING PAGERANK
def test_pagerank1b_dict():
    pagerank = Index('our_wiki_files/PageRankExample1b.xml', 'pagerank1bTitles', 'pagerank1bDocs', 'pagerank1bWords')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.4326427),2: pytest.approx(0.2340239),3: pytest.approx(0.333333333)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

#QUERY UNIT TESTS
def test_query1():
    pass

#SYSTEM TESTING
# def test_system1():
#     indexer = Index('our_wiki_files/test_query.xml', 'query1Titles', 'query1Docs', 'query1Words')
#     query = Query('our_wiki_files/test_query.xml', 'query1Titles', 'query1Docs', 'query1Words')
    

#what should the diff be?^

#system pagerank test
#system relevance test