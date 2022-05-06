import pytest
from index import Index
from query import Query

#INDEX UNIT TESTS

#TESTS PARSE METHOD
def test_parse():
    """tests if the parse method correctly parses through pages by checking if global dictionaries that are populated in the parse method are populated correctly"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    #parsing.xml is a regular file with text in different cases and different types of linking in each page
    assert index1.all_page_ids == {1,2,3} #checks if all pages are processed/parsed through
    assert index1.word_to_id_to_count == {'author': {3: 1},'categori': {2: 1},'cs200': {3: 1},'determin': {2: 1, 3: 1},'document': {1: 1, 2: 1},'gorgeou': {2: 1}, \
        'king': {3: 1},'list': {1: 1},'philosophi': {1: 1, 2: 1},'process': {1: 1}, 'relev': {2: 1},'scienc': {1: 1, 2: 1},'term': {1: 1, 2: 1},'xml': {3: 1},"king'": {3: 1},"xml'": {1: 1}}
    assert index1.id_to_links == {1: {2}, 2: {3}, 3: set()} #empty set is for pages that do not link to anything
    
    index2 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index2.all_page_ids == {13,2,100}
    #testingcase1.xml has pages that have repeated words (including the same word but repeated with different cases (uppercase, capitalized, etc))
    assert index2.word_to_id_to_count == {'cat': {13: 7, 100: 1}, 'flower': {2: 1},'garden': {2: 1},'tulip': {2: 3},'word': {100: 1}}
    assert index2.id_to_links == {13: set(), 2: set(), 100: set()} #Tests if the id_to_links dictionary is populated correctly in the parse method

    index3 = Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index3.all_page_ids == {1, 2}
    #testingcase2.xml has a page that links to the other page, also has numbers like '2000' in the text which is considered a term in the way that index parses 
    assert index3.word_to_id_to_count == {'merillium': {1: 4, 2: 2}, 'cool': {1: 2, 2: 1}, 'made': {1: 1}, 'underwat': {1: 1, 2: 1}, 'miner': {1: 2, 2: 1}, \
        '2000': {1: 1}, 'go': {1: 1}, 'one': {1: 1}, 'coin': {1: 1}, 'aquamarin': {2: 1}, 'granit': {2: 1}}
    assert index3.id_to_links == {1: set(), 2: set()} #both pages either link to themselves or to a page outside the corpus, therefore both have empty sets representing links

    #testing case that has a page with multiple instances of a link to the same document 
    index4 = Index('our_wiki_files/testingMultLinks.xml', 'titlefiles/multLinksTitles.txt', 'docfiles/multLinksDocs.txt', 'wordfiles/multLinkWords.txt')
    assert index4.all_page_ids == {1,2,3,4}
    assert index4.word_to_id_to_count == {'anyth': {3: 1},'b': {1: 1, 2: 1},'c': {2: 1, 3: 1, 4: 4},'link': {3: 1},'w': {2: 1}}
    assert index4.id_to_links == {1: {2, 4}, 2: {3, 4}, 3: set(), 4: {3}} #expected that 4: {3} even though there are four instances of links back to doc 3 in doc 4
    
def test_handle_links():
    """Testing if the handle_links method correctly removes the first and last two characters (the brackets)"""
    index1 = Index('wikis/SmallWiki.xml', 'titlefiles/titlesSmallWiki', 'docfiles/docsSmallWiki', 'wordfiles/wordsSmallWiki')
    assert index1.handle_Links('[[APPLES!]]', True) == 'APPLES!' #case with uppercase and special characters
    assert index1.handle_Links('[[Marry Me|chicken]]', False) == 'chicken' #tests if the link's text is extracted
    assert index1.handle_Links('[[Marry Me|chicken]]', True) == 'Marry Me' #tests if the address of the link is extracted
    assert index1.handle_Links('{{APPLES!}}', False) == 'APPLES!' #tests different brackets
    assert index1.handle_Links('{{}}', True) == '' #tests empty string case
    

def test_remove_stop_words_and_stem():
    """Testing if the remove_stop_words_and_stem helper method correctly returns a word if the argument is not a stop word"""
    #only one-word inputs because this function is only called when for-each looping through words
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.remove_stop_words_and_stem('a') == None 
    assert index1.remove_stop_words_and_stem('and') == None #words will always be lowercase due to .lower method call earlier in parse methd
    assert index1.remove_stop_words_and_stem('sci') == 'sci' #tests non stop word


def test_ids_to_titles_and_title_to_page_id():
    """Tests if the ids_to_titles and title_to_page_id global dictionaries are populated correctly by populate_title_page_id helper method"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.ids_to_titles == {1:'philosophy',2:'science',3:'cs200'}
    assert index1.title_to_page_id == {'cs200': 3, 'philosophy': 1, 'science': 2} #numbers in title

    #regular case
    index2 = Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index2.title_to_page_id == {'merillium is cool': 1, 'underwater minerals': 2}
    assert index2.ids_to_titles == {1: 'merillium is cool', 2: 'underwater minerals'}

    #special characters in title and capitalization
    index3 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index3.title_to_page_id == {'cat': 100, 'flower garden': 2, 'how are you?': 13}
    assert index3.ids_to_titles == {2: 'flower garden', 13: 'how are you?', 100: 'cat'}
#testing highest frequency calculations


def test_id_to_highest_freq():
    """Tests if the compute_most_freq_count_and_n_i() helper method computes highest frequency correctly and populates id_to_highest_freq() dictionary appropriately"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.id_to_highest_freq == {1: 1, 2: 1, 3: 1}

    index2 = Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index2.id_to_highest_freq == {1: 4, 2: 2} #accurate because the word 'merillium' appears in the first page 4 times

    index3 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index3.id_to_highest_freq == {2: 3, 13: 7, 100: 1} #"cat" is repeated 7 times in doc id 13

    index4 = Index('our_wiki_files/testingMultLinks.xml', 'titlefiles/multLinksTitles.txt', 'docfiles/multLinksDocs.txt', 'wordfiles/multLinkWords.txt')
    assert index4.id_to_highest_freq == {1: 1, 2: 1, 3: 1, 4: 4} #text in link that is repeated is counted

def test_term_to_num_docs():
    """Tests if the compute_most_freq_count_and_n_i() helper method populates term_to_num_of_docs() appropriately"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing')
    assert index1.term_to_num_of_docs == {'philosophi': 2, 'process': 1, "xml'": 1, 'document': 2, 'list': 1, 'term': 2, 'scienc': 2, 'determin': 2, 'relev': 1,\
        'gorgeou': 1, 'categori': 1, 'cs200': 1, 'xml': 1, "king'": 1, 'author': 1, 'king': 1} #testing words with diff cases (capitalized, lowercase, etc)

    index3 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index3.term_to_num_of_docs == {'cat': 2, 'flower': 1, 'garden': 1, 'tulip': 1, 'word': 1} #testing words in mult docs

    index4 = Index('our_wiki_files/testingMultLinks.xml', 'titlefiles/multLinksTitles.txt', 'docfiles/multLinksDocs.txt', 'wordfiles/multLinkWords.txt')
    assert index4.term_to_num_of_docs == {'anyth': 1, 'b': 2, 'c': 3, 'link': 1, 'w': 1} #testing text in links

def test_empty_wikis():
    """Tests if empty wikis are indexed appropriately by checking if the global variables are populated as expected"""
    empty = Index('our_wiki_files/emptywiki.xml', 'emptyTitles', 'docfiles/emptyDocs.txt', 'wordfiles/emptyWords.txt')
    #all global dictionaries and sets should be empty because there are no pages in emptywiki
    assert empty.all_page_ids == set()
    assert empty.idf_dict == {} #empty idf test
    assert empty.tf_dict == {} #empty tf test
    assert empty.words_to_ids_to_relevance == {}
    assert empty.all_pages == []
    assert empty.word_to_id_to_count == {}
    assert empty.id_to_links == {}
    assert empty.ids_to_pageRank_dict == {}
    assert empty.weights_dict == {}
    assert empty.term_to_num_of_docs == {}

    emptier = Index('our_wiki_files/emptierwiki.xml', 'docfiles/emptierDocs.txt', 'docfiles/emptierDocs.txt', 'wordfiles/emptierWords.txt')
    #emptier wiki only has two pages with titles and no text. Only text in the titles should be considered in computations and dictionaries
    assert emptier.title_to_page_id == {'ur mom': 1, 'ur dad': 2}
    assert emptier.term_to_num_of_docs == {'dad': 1, 'mom': 1, 'ur': 2} #only title page words accounted for, "ur" appears in both titles
    assert emptier.id_to_highest_freq == {1: 1, 2: 1} #highest frequency for each page is only based on words in the title
    assert emptier.ids_to_pageRank_dict == {1: pytest.approx(0.5), 2: pytest.approx(0.5)} #because both pages have the same weights and pagerank value calculations 
    assert emptier.tf_dict == {'dad': {2: 1.0}, 'mom': {1: 1.0}, 'ur': {1: 1.0, 2: 1.0}}
    assert emptier.idf_dict == {'dad': pytest.approx(0.69314718), 'mom': pytest.approx(0.69314718), 'ur': 0.0} #because "ur" appears in both pages, its idf is 0
    assert emptier.word_to_id_to_count == {'dad': {2: 1}, 'mom': {1: 1}, 'ur': {1: 1, 2: 1}}
    assert emptier.weights_dict == {1: {1: 0.075, 2: pytest.approx(0.92499999, .001)}, 2: {1: pytest.approx(0.92499999, .001), 2: 0.075}}

def test_one_page():
    """Tests if wiki with only one page is indexed appropriately by checking if the global variables are populated as expected"""
    one = Index('our_wiki_files/onepage.xml', 'titlefiles/titleOne.txt', 'docfiles/docsOne.txt', 'wordfiles/wordOne.txt')
    assert one.idf_dict == {'cpax': 0.0, 'lone': 0.0, 'page': 0.0}
    assert one.tf_dict == {'cpax': {1: 0.5}, 'lone': {1: 0.5}, 'page': {1: 1.0}}
    assert one.all_page_ids == {1}
    assert one.weights_dict == {1: {1: 0.15}} #weight for one page should be e/n
    assert one.word_to_id_to_count == {'cpax': {1: 1}, 'lone': {1: 1}, 'page': {1: 2}}
    assert one.term_to_num_of_docs == {'cpax': 1, 'lone': 1, 'page': 1} #should all be 1 because there's only one page
 

#TEST TERM TO DOC RELEVANCE and relevance calculations

def test_idf_dict():
    """This tests the compute_idf helper method in index.py and if idf_dict is populated appropriately"""
    index1 = Index('wikis/test_tf_idf.xml', 'titlefiles/tfidfTitles.txt', 'docfiles/tfidfDocs.txt', 'wordfiles/tfidfWords.txt')
    #regular test
    assert index1.idf_dict == {'page': 0, '1': pytest.approx(1.0986, .001), 'dog': pytest.approx(0.40546, .001), 'bit': pytest.approx(0.405465, .001),\
        'man': pytest.approx(1.098612, .001), '2': pytest.approx(1.098612, .001), 'ate': pytest.approx(1.098612, .001), 'chees': pytest.approx(0.405465, .001), '3': pytest.approx(1.0986122, .001)}
    #regular test
    index3 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index3.idf_dict == {'cat': pytest.approx(0.4054651, .001),'flower': pytest.approx(1.0986123, .001),'garden': pytest.approx(1.0986123, .001), 'tulip': pytest.approx(1.0986123, .001),'word': pytest.approx(1.0986123, .001)}

    
def test_words_to_ids_to_relevance():
    """Tests compute_relevance helper method in index.py by testing if the words_to_ids_to_relevance dict is populated appropriately"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing.txt')
    assert index1.words_to_ids_to_relevance == {'philosophi': {1: pytest.approx(0.405465), 2: pytest.approx(0.405465108)}, 'process': \
        {1: pytest.approx(1.0986123)}, "xml'": {1: pytest.approx(1.09861229)}, 'document': {1: pytest.approx(0.4054651), 2: pytest.approx(0.4054651)}, \
        'list': {1: pytest.approx(1.09861229)}, 'term': {1: pytest.approx(0.40546511), 2: pytest.approx(0.4054651)}, 'scienc': {1: pytest.approx(0.4054651),\
        2: pytest.approx(0.4054651)}, 'determin': {2: pytest.approx(0.4054651), 3: pytest.approx(0.4054651)}, 'relev': {2: pytest.approx(1.09861229)}, 'gorgeou': \
        {2: pytest.approx(1.09861229)}, 'categori': {2: pytest.approx(1.09861229)}, 'cs200': {3: pytest.approx(1.09861229)}, 'xml': {3: pytest.approx(1.09861229)},\
        "king'": {3: pytest.approx(1.09861229)}, 'author': {3: pytest.approx(1.09861229)}, 'king': {3: pytest.approx(1.09861229)}}
    
    #test case of pages with no text
    emptier = Index('our_wiki_files/emptierwiki.xml', 'docfiles/emptierDocs.txt', 'docfiles/emptierDocs.txt', 'wordfiles/emptierWords.txt')
    assert emptier.words_to_ids_to_relevance == {'dad': {2: pytest.approx(0.693147, 0.001)}, 'mom': {1: pytest.approx(0.69314718, .001)},'ur': {1: 0, 2: 0}}
    
    #regular test
    index2 = Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index2.words_to_ids_to_relevance == {'merillium': {1: 0.0, 2: 0.0}, 'cool': {1: 0.0, 2: 0.0}, 'made': {1: pytest.approx(0.173287, .001)}, 'underwat': {1: 0.0, 2: 0.0}, \
        'miner': {1: 0.0, 2: 0.0}, '2000': {1: pytest.approx(0.173287, .001)}, 'go': {1: pytest.approx(0.173287, .001)}, 'one': {1: pytest.approx(0.173287, .001)}, 'coin': {1: pytest.approx(0.173287, .001)}, \
        'aquamarin': {2: pytest.approx(0.34657359)}, 'granit': {2: pytest.approx(0.34657359)}}
    #test case of pages with text of the same word but different cases (lowercase, capitalized, etc)
    index3 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index3.words_to_ids_to_relevance == {'cat': {13: pytest.approx(0.4054651, .001), 100: pytest.approx(0.4054651, .001)}, 'flower': {2: pytest.approx(0.3662041, .001)}, 'garden': {2: pytest.approx(0.3662041, .001)}, \
        'tulip': {2: pytest.approx(1.09861229, .001)}, 'word': {100: pytest.approx(1.09861229, .001)}}
    
#TEST WEGIHTS
def test_weights_dict():
    """tests populate_weights_dict helper method in index.py"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing', 'wordfiles/wordsParsing.txt')
    assert index1.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: pytest.approx(0.9, .001), 3: pytest.approx(0.04999999, .001)}, 2: {1: pytest.approx(0.04999, .001),\
        2: pytest.approx(0.04999, .001), 3: pytest.approx(0.9)}, 3: {1: pytest.approx(0.475), 2: pytest.approx(0.475), 3: pytest.approx(0.04999, .001)}}

    #one page linked to another page with a similar title to a page within the corpus except the link title is capitalized
    index2 = Index('our_wiki_files/testing_weights_2.xml', 'titlefiles/weightsTitles2.txt', 'docfiles/weightsDocs2.txt','wordfiles/weightsWords2.txt')
    assert index2.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: 0.9, 3:pytest.approx(0.049999, .001)}, 2: {1: 0.9, 2: pytest.approx(0.049999, .001), 3: \
        pytest.approx(0.049999, .001)}, 3: {1: 0.475, 2: 0.475, 3: pytest.approx(0.049999, .001)}}

    #a page linked to every other page and a page outside of the corpus, id 2 does not link to anything and therefore links to every other doc but itself
    index3 = Index('our_wiki_files/PageRankExample1b.xml', 'titlefiles/pagerank1bTitles.txt', 'docfiles/pagerank1bDocs.txt', 'wordfiles/pagerank1bWords.txt')
    assert index3.weights_dict == {1: {1: pytest.approx(0.049999, .001), 2: 0.475, 3: 0.475}, 2: {1: 0.475, 2: pytest.approx(0.049999, .001), 3: 0.475}, 3: {1: 0.9, 2:\
        pytest.approx(0.049999, .001), 3: pytest.approx(0.049999, .001)}}

    #page linked to another page outside the corpus
    index4 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index4.weights_dict == {2: {2: pytest.approx(0.05, .01), 13: 0.475, 100: 0.475}, 13: {2: 0.475, 13: pytest.approx(0.05, .01), \
        100: 0.475},100: {2: 0.475, 13: 0.475, 100: pytest.approx(0.05, .01)}}
    
    #one document linked to itself and the other document linked to a page outside the corpus
    index5 =Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index5.weights_dict == {1: {1: 0.075, 2: pytest.approx(0.924999, .001)}, 2: {1: pytest.approx(0.924999, .001), 2: 0.075}}

    #case one tests for the weight of a file with just one page. Should be 1 but in reality is .15 due to e. 
#     one = Index('our_wiki_files/onepage.xml', 'titlefiles/titleOne.txt', 'docfiles/docsOne.txt', 'wordfiles/wordOne.txt')
#     assert one.weights_dict == {1: {1:1}}


def test_euclidean_distance():
    """Tests if the euclidean distance computation helper method computes the euclidean distance appropriately"""
    index1 = Index('our_wiki_files/parsing.xml', 'titlefiles/titlesParsing', 'docfiles/docsParsing.txt', 'wordfiles/wordsParsing.txt')
    assert index1.euclidean_distance({1: 0.3333,2:0.3333,3:0.33333}, {1:0, 2:0,3:0}) == pytest.approx(0.57731) #3 docs
    assert index1.euclidean_distance({1: 0.111111,2:0.111111,3:0.111111,4:0.111111,5:0.111111,6:0.111111,7:0.111111,8:0.111111,9:0.111111}, {1:0, 2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0})\
        == pytest.approx(0.333333) #more than 3 docs
    assert index1.euclidean_distance({},{}) == 0 #empty dictionary
    assert index1.euclidean_distance({1:0},{1:0}) == 0 

#TESTING PAGERANK

def test_pagerank1_dict():
    """testing Pagerank1.xml for the case that there exists both 
    a page links to a page outside of the corpus and a page links to a page that contains text different from the link text"""
    pagerank1 = Index('wikis/PageRankExample1.xml', 'titlefiles/pagerank1Titles.txt', 'docfiles/pagerank1Docs.txt', 'wordfiles/pagerank1Words.txt')
    assert pagerank1.ids_to_pageRank_dict == {1: pytest.approx(0.4326427, 0.001), 2: pytest.approx(0.2340239, 0.001), 3: pytest.approx(0.33333, 0.001)}
    assert sum(pagerank1.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank1b_dict():
    """Testing pagerank1b for the case that a page has no link and therefore links to every page other than itself"""
    pagerank = Index('our_wiki_files/PageRankExample1b.xml', 'titlefiles/pagerank1bTitles.txt', 'docfiles/pagerank1bDocs.txt', 'wordfiles/pagerank1bWords.txt')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.4326427),2: pytest.approx(0.2340239),3: pytest.approx(0.333333333)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_smallWiki_dict():
    """Testing if small wiki's pagerank values sum to approximately 1"""
    pagerank2 = Index('wikis/SmallWiki.xml', 'titlefiles/titlesSmallWiki', 'docfiles/docsSmallWiki.txt','wordfiles/wordsSmallWiki.txt')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_medWiki_dict():
    """Testing if med wiki's pagerank values sum to approximately 1"""
    pagerank2 = Index('wikis/MedWiki.xml', 'MedWikiTitles.txt', 'MedWikiDocs.txt','MedWikiWords.txt')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_bigWiki_dict():
    """Testing if big wiki's pagerank values sum to approximately 1"""
    pagerank2 = Index('wikis/BigWiki.xml', 'BigWikiTitles.txt', 'BigWikiDocs.txt','BigWikiWords.txt')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank2():
    """testing PageRank2 xml file which includes no special linking cases"""
    pagerank2 = Index('wikis/PageRankExample2.xml', 'titlefiles/pagerank2Titles.txt', 'docfiles/pagerank2Docs.txt', 'wordfiles/pagerank2Words.txt')
    assert sum(pagerank2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_pagerank3():
    """Testing pagerank3 example for the case that a page is linked to itself"""
    pagerank3 = Index('wikis/PageRankExample3.xml', 'titlefiles/pagerank3Titles.txt', 'docfiles/pagerank3Docs.txt', 'wordfiles/pagerank3Word.txt')
    assert pagerank3.ids_to_pageRank_dict == {1: 0.05242784862611451, 2: 0.05242784862611451, 3: 0.4475721513738852, 4: 0.44757215137388523}
    assert sum(pagerank3.ids_to_pageRank_dict.values()) == pytest.approx(1)


def test_pagerank6():
    """Testing pagegrank 6, another xml file with no special linking cases"""
    pagerank6 = Index('our_wiki_files/PageRankExample6.xml', 'titlefiles/pageRank6Titles.txt', 'docfiles/pageRank6Docs.txt', 'wordfiles/pageRank6Words.txt')
    assert pagerank6.ids_to_pageRank_dict == {1: pytest.approx(0.22726, 0.001), 2: pytest.approx(0.37899, 0.001), 3: pytest.approx(0.29175, 0.001), 4: pytest.approx(0.101996, 0.001)}
    assert sum(pagerank6.ids_to_pageRank_dict.values()) == pytest.approx(1)


def test_pagerank5():
    """Testing pagerank 5 for the case that a page has a link to a page outside of the corpus"""
    pagerank = Index('our_wiki_files/PageRankExample5.xml', 'titlefiles/pagerank5Titles.txt', 'docfiles/pagerank5Docs.txt', 'wordfiles/pagerank5Words.txt')
    assert pagerank.ids_to_pageRank_dict == {1: pytest.approx(0.05242, 0.001), 2: pytest.approx(0.4476, 0.001), 3: pytest.approx(0.05243, 0.001), 4: pytest.approx(0.4476, 0.001)}
    assert sum(pagerank.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_testing1():
    """testingcase1.xml accounts for the case where a page is not linked to anything (thus being linked to every page other than itself)
    as well as the case where a page is linked to a page outside of the corpus. This page outside of the corpus also contains text different fron its linked 
    (case of having a pipe in link)"""

    index2 = Index('our_wiki_files/testingcase1.xml', 'titlefiles/titleCase1.txt', 'docfiles/docsCase1.txt', 'wordfiles/wordsCase1.txt')
    assert index2.ids_to_pageRank_dict == {2: pytest.approx(0.3333, 0.001), 13: pytest.approx(0.3333, 0.001), 100: pytest.approx(0.3333, 0.001)}
    assert sum(index2.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_testing2():
    """testingcase2.xml accounts for the case in which a page is linked to itself, as well as if a page is linked to a page whose link is different from the text it contains
    (pipe in link)"""
    
    index3 = Index('our_wiki_files/testingcase2.xml', 'titlefiles/titleCase2.txt', 'docfiles/docsCase2.txt', 'wordfiles/wordsCase2.txt')
    assert index3.ids_to_pageRank_dict == {1: pytest.approx(0.5, 0.001), 2: pytest.approx(0.5, 0.001)}
    assert sum(index3.ids_to_pageRank_dict.values()) == pytest.approx(1)

def test_tiebreaker():
    """testing the case in which all pages have the same word the same amount of times"""
    tie = Index('our_wiki_files/tiebreaker.xml', 'titlefiles/tiebreakerTitles.txt', 'docfiles/tiebreakerDocs.txt', 'wordfiles/tiebreakerWords.txt')
    assert tie.ids_to_pageRank_dict == {1: pytest.approx(0.33333, 0.001),2: pytest.approx(0.33333, 0.001),3:pytest.approx(0.33333, 0.001)}
    #this result makes sense as all the pages are tied in rank since they have the same word appear the same amount of times. 

def test_multLinks():
    """multLinks.xml is a file containing multiple pages with one page having multiple instances of the same link"""
    index4 = Index('our_wiki_files/testingMultLinks.xml', 'titlefiles/multLinksTitles.txt', 'docfiles/multLinksDocs.txt', 'wordfiles/multLinkWords.txt')
    #this result makes sense because, for example, page 4 has a higher pagerank value than 1 and 2 since it is linked to the least amount of pages, among other factors.
    assert index4.ids_to_pageRank_dict == {1: pytest.approx(0.141786846, .001), 2: pytest.approx(0.202145947, .001), 3: pytest.approx(0.3680377, .001),4: pytest.approx(0.288029492, .001)}

# def test_one_page_pagerank():
#     """Tests if wiki with only one page has expected pagerank value
#     This test is not running as expected because the sum of all pagerank values should be 1 but 
#     because of the way weights is calculated, the weight of one page is .15 and the sum of all 
#     pagerank values is not 1"""
#     one = Index('our_wiki_files/onepage.xml', 'titlefiles/titleOne.txt', 'docfiles/docsOne.txt', 'wordfiles/wordOne.txt')
#     assert one.ids_to_pageRank_dict == {1: 1}
#     assert sum(one.ids_to_pageRank_dict.values()) == pytest.approx(1)
#     assert one.weights_dict == {1: {1: 1}}



# QUERY UNIT TESTS
def test_query1():
    """Testing if the global dictionaries in query are populated appropriately which would account for the methods in query computing and mapping correctly"""
    query1 = Query(False, 'titlefiles/titlesParsing.txt', 'docfiles/docsParsing.txt', 'wordfiles/wordsParsing.txt')
    assert query1.ids_to_titles == {1: 'philosophy', 2: 'science', 3: 'cs200'} #testing titles with capitalization, numbers
    assert query1.ids_to_pageranks == {1: pytest.approx(0.214862), 2: pytest.approx(0.3972272), 3: pytest.approx(0.3879107)}
    assert sum(query1.ids_to_pageranks.values()) == pytest.approx(1)
    