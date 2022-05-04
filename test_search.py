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
    
    index2 = Index('our_wiki_files/testingcase1.xml', 'titleCase1', 'docsCase1', 'wordsCase1')
    assert index2.all_page_ids == {13,2,100}
    assert index2.word_to_id_to_count == {'cat': {13: 7, 100: 1}, 'flower': {2: 1},'garden': {2: 1},'tulip': {2: 3},'word': {100: 1}}
    assert index2.id_to_links == {13: set(), 2: set(), 100: set()}

    index3 = Index('our_wiki_files/testingcase2.xml', 'titleCase2', 'docsCase2', 'wordsCase3')
    assert index3.all_page_ids == {1, 2}
    assert index3.word_to_id_to_count == {'merillium': {1: 4, 2: 2}, 'cool': {1: 2, 2: 1}, 'made': {1: 1}, 'underwat': {1: 1, 2: 1}, 'miner': {1: 2, 2: 1}, '2000': {1: 1}, 'go': {1: 1}, 'one': {1: 1}, 'coin': {1: 1}, 'aquamarin': {2: 1}, 'granit': {2: 1}}
    assert index3.id_to_links == {1: set(), 2: set()}

def test_handle_links():
    index1 = Index('wikis/SmallWiki.xml', 'titlefiles/titlesSmallWiki', 'docfiles/docsSmallWiki', 'wordfiles/wordsSmallWiki')
    assert index1.handle_Links('[[APPLES!]]', True) == 'APPLES!'
    assert index1.handle_Links('[[Marry Me|chicken]]', False) == 'chicken'
    assert index1.handle_Links('[[Marry Me|chicken]]', True) == 'Marry Me'
    assert index1.handle_Links('{{APPLES!}}', False) == 'APPLES!'
    assert index1.handle_Links('{{}}', True) == ''
    

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

def test_empty_wikis():
    empty = Index('our_wiki_files/emptywiki.xml', 'emptyTitles', 'emptyDocs', 'emptyWords')
    assert empty.all_page_ids == set()
    assert empty.idf_dict == {}
    assert empty.tf_dict == {}
    assert empty.words_to_ids_to_relevance == {}
    assert empty.all_pages == []

    emptier = Index('our_wiki_files/emptierwiki.xml', 'emptierTitles', 'emptierDocs', 'emptierWords')
    assert emptier.title_to_page_id == {'ur mom': 1, 'ur dad': 2}
    assert emptier.term_to_num_of_docs == {'dad': 1, 'mom': 1, 'ur': 2}
    assert emptier.id_to_highest_freq == {1: 1, 2: 1}
    assert emptier.ids_to_pageRank_dict == {1: pytest.approx(0.5), 2: pytest.approx(0.5)}
    assert emptier.tf_dict == {'dad': {2: 1.0}, 'mom': {1: 1.0}, 'ur': {1: 1.0, 2: 1.0}}
    assert emptier.idf_dict == {'dad': pytest.approx(0.69314718), 'mom': pytest.approx(0.69314718), 'ur': 0.0}

def test_one_page():
    one = Index('our_wiki_files/onepage.xml', 'titleOne', 'docsOne', 'wordOne')
    assert one.idf_dict == {'cpax': 0.0, 'lone': 0.0, 'page': 0.0}
    assert one.tf_dict == {'cpax': {1: 0.5}, 'lone': {1: 0.5}, 'page': {1: 1.0}}
    assert one.all_page_ids == {1}

#TEST TERM TO DOC RELEVANCE and relevance calculations

def test_idf_dict():
    """This tests compute_idf in index.py"""
    index1 = Index('wikis/test_tf_idf.xml', 'tfidfTitles', 'tfidfDocs', 'tfidfWords')
    assert index1.idf_dict == {'page': 0, '1': pytest.approx(1.0986, .001), 'dog': pytest.approx(0.40546, .001), 'bit': pytest.approx(0.405465, .001), 'man': pytest.approx(1.098612, .001), '2': pytest.approx(1.098612, .001), 'ate': pytest.approx(1.098612, .001), 'chees': pytest.approx(0.405465, .001), '3': pytest.approx(1.0986122, .001)}

def test_words_to_ids_to_relevance():
    """Tests compute_relevance in index.py"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.words_to_ids_to_relevance == {'philosophi': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'process': {1: 1.0986122886681098}, "xml'": {1: 1.0986122886681098}, 'document': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'list': {1: 1.0986122886681098}, 'term': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'scienc': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'determin': {2: 0.4054651081081644, 3: 0.4054651081081644}, 'relev': {2: 1.0986122886681098}, 'gorgeou': {2: 1.0986122886681098}, 'categori': {2: 1.0986122886681098}, 'cs200': {3: 1.0986122886681098}, 'xml': {3: 1.0986122886681098}, "king'": {3: 1.0986122886681098}, 'author': {3: 1.0986122886681098}, 'king': {3: 1.0986122886681098}}

#TEST WEGIHTS
def test_weights_dict():
    """tests populate_weights_dict in index.py"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: pytest.approx(0.9, .001), 3: pytest.approx(0.04999999, .001)}, 2: {1: pytest.approx(0.04999, .001), 2: pytest.approx(0.04999, .001), 3: pytest.approx(0.9)}, 3: {1: pytest.approx(0.475), 2: pytest.approx(0.475), 3: pytest.approx(0.04999, .001)}}

    index2 = Index('our_wiki_files/testing_weights_2.xml', 'weightsTitles2', 'weightsDocs2','weightsWords2')
    assert index2.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: 0.9, 3:pytest.approx(0.049999, .001)}, 2: {1: 0.9, 2: pytest.approx(0.049999, .001), 3: pytest.approx(0.049999, .001)}, 3: {1: 0.475, 2: 0.475, 3: pytest.approx(0.049999, .001)}}

    index3 = Index('our_wiki_files/PageRankExample1b.xml', 'pagerank1bTitles', 'pagerank1bDocs', 'pagerank1bWords')
    assert index3.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: 0.475, 3: 0.475}, 2: {1: 0.475, 2: pytest.approx(0.049999, .001), 3: 0.475}, 3: {1: 0.9, 2: pytest.approx(0.049999, .001), 3: pytest.approx(0.049999, .001)}}

# testing euclidean distance for pagerank
def test_euclidean_distance():
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.euclidean_distance({1: 0.3333,2:0.3333,3:0.33333}, {1:0, 2:0,3:0}) == pytest.approx(0.57731)
    assert index1.euclidean_distance({1: 0.111111,2:0.111111,3:0.111111,4:0.111111,5:0.111111,6:0.111111,7:0.111111,8:0.111111,9:0.111111}, {1:0, 2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}) == pytest.approx(0.333333)
    assert index1.euclidean_distance({},{}) == 0
    assert index1.euclidean_distance({1:0},{1:0}) == 0

#TESTING PAGERANK
def test_pagerank1b_dict():
    pagerank = Index('our_wiki_files/PageRankExample1b.xml', 'pagerank1bTitles', 'pagerank1bDocs', 'pagerank1bWords')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.4326427),2: pytest.approx(0.2340239),3: pytest.approx(0.333333333)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

    #Testing if Small Wiki's pagerank values sum to 1
def test_smallWiki_dict():
    pagerank2 = Index('wikis/SmallWiki.xml', 'titlefiles/titlesSmallWiki', 'docfiles/docsSmallWiki','wordfiles/wordsSmallWiki')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank2():
    pagerank2 = Index('wikis/PageRankExample2.xml', 'pagerank2Titles', 'pagerank2Docs', 'pagerank2Words')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank3():
    pagerank3 = Index('wikis/PageRankExample3.xml', 'pagerank3Titles', 'pagerank3Docs', 'pagerank3Word')
    assert sum(pagerank3.ids_to_pageRank_dict.values()) == pytest.approx(1)


def test_pagerank6():
    pagerank6 = Index('our_wiki_files/PageRankExample6.xml', 'pageRank6Titles', 'pageRank6Docs', 'pageRank6Words')
    assert pagerank6.ids_to_pageRank_dict == {1: pytest.approx(0.22726, 0.001), 2: pytest.approx(0.37899, 0.001), 3: pytest.approx(0.29175, 0.001), 4: pytest.approx(0.101996, 0.001)}
    assert sum(pagerank6.ids_to_pageRank_dict.values()) == pytest.approx(1)


def test_pagerank5():
    pagerank = Index('our_wiki_files/PageRankExample5.xml', 'pagerank5Titles', 'pagerank5Docs', 'pagerank5Words')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.05242, 0.001), 2: pytest.approx(0.4476, 0.001), 3: pytest.approx(0.05243, 0.001), 4: pytest.approx(0.4476, 0.001)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

#QUERY UNIT TESTS
# def test_query1():
#     query1 = Query('--pagerank', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')

    