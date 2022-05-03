import pytest
from index import Index
from query import Query

#INDEX UNIT TESTS
#TESTS PARSE METHOD
def test_parse():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.all_page_ids == {1,2,3}
    assert index1.word_to_id_to_count == {'author': {3: 1},'categori': {2: 1},'cs200': {3: 1},'determin': {2: 1, 3: 1},'document': {1: 1, 2: 1},'gorgeou': {2: 1}, 'king': {3: 1},'list': {1: 1},'philosophi': {1: 1, 2: 1},'process': {1: 1}, 'relev': {2: 1},'scienc': {1: 1, 2: 1},'term': {1: 1, 2: 1},'xml': {3: 1},"king'": {3: 1},"xml'": {1: 1}}
    assert index1.id_to_links == {1: {2}, 2: {3}, 3: set()}
    
    # index2 = Index()

def test_handle_links():
    index1 = Index('wikis/SmallWiki.xml', 'titlefiles/titlesSmallWiki', 'docfiles/docsSmallWiki', 'wordfiles/wordsSmallWiki')
    

def test_remove_stop_words_and_stem():
    #only one-word inputs because this function is only called when for-each looping through words
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.remove_stop_words_and_stem('a') == None
    assert index1.remove_stop_words_and_stem('and') == None #words will always be lowercase due to .lower method call earlier in parse methd
    assert index1.remove_stop_words_and_stem('sci') == 'sci'


def test_ids_to_titles_and_title_to_page_id():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.ids_to_titles == {1:'philosophy',2:'science',3:'cs200'}
    assert index1.title_to_page_id == {'cs200': 3, 'philosophy': 1, 'science': 2}


def test_ids_to_links():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.id_to_links == {1:{2},2:{3},3:set()}

#testing highest frequency calculations
def test_id_to_highest_freq():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.id_to_highest_freq == {1: 1, 2: 1, 3: 1}

def test_term_to_num_docs():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.term_to_num_of_docs == {'philosophi': 2, 'process': 1, "xml'": 1, 'document': 2, 'list': 1, 'term': 2, 'scienc': 2, 'determin': 2, 'relev': 1, 'gorgeou': 1, 'categori': 1, 'cs200': 1, 'xml': 1, "king'": 1, 'author': 1, 'king': 1}

# def test_empty_wikis():
#     # empty = Index('our_wiki_files/emptywiki.xml', 'emptyTitles', 'emptyDocs', 'emptyWords')
#     emptier = Index('our_wiki_files/emptierwiki.xml', 'emptierTitles', 'emptierDocs', 'emptierWords')

    

#TEST TERM TO DOC RELEVANCE and relevance calculations

def test_idf_dict():
    """This tests compute_idf in index.py"""
    pass

def test_words_to_ids_to_relevance():
    """Tests compute_relevance in index.py"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.words_to_ids_to_relevance == {'philosophi': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'process': {1: 1.0986122886681098}, "xml'": {1: 1.0986122886681098}, 'document': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'list': {1: 1.0986122886681098}, 'term': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'scienc': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'determin': {2: 0.4054651081081644, 3: 0.4054651081081644}, 'relev': {2: 1.0986122886681098}, 'gorgeou': {2: 1.0986122886681098}, 'categori': {2: 1.0986122886681098}, 'cs200': {3: 1.0986122886681098}, 'xml': {3: 1.0986122886681098}, "king'": {3: 1.0986122886681098}, 'author': {3: 1.0986122886681098}, 'king': {3: 1.0986122886681098}}

#TEST WEGIHTS
def test_weights_dict():
    """tests populate_weights_dict in index.py"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: pytest.approx(0.9, .001), 3: pytest.approx(0.04999999, .001)}, 2: {1: pytest.approx(0.04999, .001), 2: pytest.approx(0.04999, .001), 3: pytest.approx(0.9)}, 3: {1: pytest.approx(0.475), 2: pytest.approx(0.475), 3: pytest.approx(0.04999, .001)}}

#testing euclidean distance for pagerank
def test_euclidean_distance():
    pass

#TESTING PAGERANK
def test_pagerank1b_dict():
    pagerank = Index('our_wiki_files/PageRankExample1b.xml', 'pagerank1bTitles', 'pagerank1bDocs', 'pagerank1bWords')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.4326427),2: pytest.approx(0.2340239),3: pytest.approx(0.333333333)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank5():
    pagerank = Index('our_wiki_files/PageRankExample5.xml', 'pagerank5Titles', 'pagerank5Docs', 'pagerank5Words')
    print(pagerank.ids_to_pageRank_dict.values())
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.05242, 0.001), 2: pytest.approx(0.4476, 0.001), 3: pytest.approx(0.05243, 0.001), 4: pytest.approx(0.4476, 0.001)}
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