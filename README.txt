Muhiim Ali, Jennifer Chen

1.Known Bugs:
    Words with apostrophes
    numbers (2000, 1 etc) counted in the terms

2. User Instructions:

type python3 index.py relativeWikiPath titles.txt docs.txt words.txt
type python3 query.py (--pagerank) titles.txt docs.txt words.txt

When query.py is run, the prompt 'search>' will appear and the user can input any word or phrase into the terminal. Pressing the enter button runs search and 
produces a result. If the input does not exist in the corpus, or if the input is empty, no results will be returned and the user will
be prompted to try a new search. After every search, the user is able to search again.

3.Program:

[INDEXER]

    File index.py is the indexer that processes the XML document and stores data such as a list of terms. The indexer also calculates and stores 
information such as the relevance between terms and documents. index.py also includes the code for PageRank.

    index.py includes the main method (__init__) which takes in the xml file and the names of the word, doc, and title files that are created when indexer is run.
Indexer's main method initializes all global dictionaries and calls methods. Method calls are called in a specific order so that 
dictionaries are populated and calculations are performed in an appropriate order.

    The parse method is then called to account for links and populate dictionaries that map ids to links as well as words to doc ids to count (the amount of times a word appears in the doc).
    The weights between documents are then calculated and the weight dictionary is populated. !!!FINISH!!!

[QUERY]
    File query.py is the querier that parses in arguments for the index files and accounts for if pagerank will be used in the 
    search or not. The querier runs a RELP that takes in and proceses queries (searches). The querier then 
    ranks documents against the queries based on term relevance and, if specified, PageRank from the index files. These index
    files are the word file, doc file, and title file. 

    The query has a method for ranking pages called rank_pages that takes in a list of query words that exist in the wiki as well as a dictionary that has doc ids
    mapped to total relevance. This dictionary that maps ids to relevance is populated in the method populate_total_relevance which takes in a list of 
    all the unsorted query words. 

    If query's rank_pages method finds that there are no words in the query search that would match to results in the wiki, an informative message
    will be printed out that tells the user that there are no search results and that they should try a new search. 

[TESTING]

    Test_search contains the unit tests that were used to check for the functionality of index and query as we coded.
Tests were made by creating an insance of Index and texting if the dictionaries and methods were outputting properly. 


4.Extra/Unimplemented Features: None

5.Unit Testing:

    [INDEX.PY]

    [QUERY.PY]

Tests not included in test_system:

    Testing FileNotFoundException:
        When 
    

6. System Testing:

-------Test FileNotFoundError------

In the terminal, type: python3 index.py wikis/nonexistantWiki.xml nonexistTitles.txt nonexistDocs.txt nondexistWords.txt
Returns: FileNotFoundError: [Errno 2] No such file or directory: 'wikis/nonexistantWiki.xml'

In the terminal, type: python3 query.py --pagerank nonexistTitles.txt nonexistDocs.txt nondexistWords.txt
Returns: FileNotFoundError: [Errno 2] No such file or directory: 'nonexistTitles.txt'

In the terminal, type: python3 query.py --pagerank tfidfTitles nonexistDocs.txt tfidfWords
Returns: FileNotFoundError: [Errno 2] No such file or directory: 'nonexistTitles.txt'

-------Test writing files------

In the terminal, type: python3 index.py wikis/SmallWiki.xml titlefiles/titlesparsing.txt docfiles/docsParsing.txt wordfiles/wordsparsing.txt
Side effect: Rewrites the existing text, docs, and word files according to SmallWiki. Originally, the text, docs, and word relative paths correlated
to txt docs for indexing the parsing.xml file. 

In terminal, type:  python3 index.py our_wiki_files/parsing.xml titlefiles/titlesparsing.txt docfiles/docsParsing.txt wordfiles/wordsparsing.txt
Side effect: After running the above index call, this index call 'reverses' the last one by rewriting the appropriate parsing.xml files 


----Test empty wiki---- #tests a wiki with no pages

WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/emptyTitles.txt docfiles/emptyDocs.txt wordfiles/emptyWords.txt

    INPUT: mom
    RESULTS: No search results available. Try a different search!

    INPUT: merillium
    RESULTS: No search results available. Try a different search!

    INPUT: a
    RESULTS: No search results available. Try a different search!

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: this is a sentence
    RESULTS: No search results available. Try a different search!

    INPUT: 2000
    RESULTS: No search results available. Try a different search!

    INPUT: :quit
    RESULTS: exits out of search

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/emptyTitles.txt docfiles/emptyDocs.txt wordfiles/emptyWords.txt

    INPUT: mom
    RESULTS: No search results available. Try a different search!

    INPUT: merillium
    RESULTS: No search results available. Try a different search!

    INPUT: a
    RESULTS: No search results available. Try a different search!

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: this is a sentence
    RESULTS: No search results available. Try a different search!

    INPUT: 2000
    RESULTS: No search results available. Try a different search!

    INPUT: :quit
    RESULTS: exits out of search
---------Test emptier wiki------- #tests wiki with pages and titles but no text

WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/emptierTitles.txt docfiles/emptierDocs.txt wordfiles/emptierWords.txt

    INPUT: movie
    RESULTS: No search results available. Try a different search!

    INPUT: 1
    RESULTS: No search results available. Try a different search!

    INPUT: page
    RESULTS: No search results available. Try a different search!

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: my family consists of my mom and dad
    RESULTS:
    1 ur mom
    2 ur dad

    INPUT: WHY DOES MY MOM ALWAYS BOTHER ME?
    RESULTS:
    1 ur mom

    INPUT: ur
    RESULTS:
    1 ur mom
    2 ur dad

    INPUT: :quit
    RESULTS: exits out of search

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/emptierTitles.txt docfiles/emptierDocs.txt wordfiles/emptierWords.txt

    INPUT: movie    
    RESULTS: No search results available. Try a different search!

    INPUT: 1
    RESULTS: No search results available. Try a different search!

    INPUT: page
    RESULTS: No search results available. Try a different search!

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: my family consists of my mom and dad
    RESULTS:
    1 ur mom
    2 ur dad

    INPUT: WHY DOES MY MOM ALWAYS BOTHER ME?
    RESULTS:
    1 ur mom

    INPUT: ur
    RESULTS:
    1 ur mom
    2 ur dad

    INPUT: :quit
    RESULTS: exits out of search

-----Test test_query.xml-----

   WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/query1Titles.txt docfiles/query1Docs.txt wordfiles/query1Words.txt

    INPUT: horse
    RESULTS: 
    1 page h
    2 page a
    3 page b
    4 page c
    5 page d
    6 page e

    INPUT: horse'
    RESULTS: 
    1 page h
    2 page a
    3 page b
    4 page c
    5 page d
    6 page e

    INPUT: horse's
    RESULTS:
    1 page f

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: on a farm there are cows
    RESULTS: No search results available. Try a different search!

    INPUT: Hey! which horses are the fastest
    RESULTS:
    1 page h
    2 page a
    3 page b
    4 page c
    5 page d
    6 page e  

    INPUT: what happened between horses and humans?
    RESULTS:
    1 page a
    2 page h
    3 page d
    4 page b
    5 page c
    6 page e

    INPUT: :quit
    RESULTS: exits out of search

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/query1Titles.txt docfiles/query1Docs.txt wordfiles/query1Words.txt

    INPUT: horse
    RESULTS: 
    1 page h
    2 page a
    3 page b
    4 page c
    5 page d
    6 page e

    INPUT: horse'
    RESULTS: 
    1 page h
    2 page a
    3 page b
    4 page c
    5 page d
    6 page e

    INPUT: horse's
    RESULTS:
    1 page f

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: what kind of food do horses eat
    RESULTS:
    1 page c
    2 page h
    3 page a
    4 page b
    5 page d
    6 page e

    INPUT: do cows like pineapple
    RESULTS: No search results available. Try a different search!

    INPUT: what happened between horses and humans?
    RESULTS:
    1 page a
    2 page d
    3 page h
    4 page b
    5 page c
    6 page e

    INPUT: :quit
    RESULTS: exits out of search

-------Test testingcase2.xml-----
    WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/titleCase2.txt docfiles/docsCase2.txt wordfiles/wordsCase2.txt

    INPUT: merillium
    RESULTS: 
    1 merillium is cool
    2 underwater minerals

    INPUT: mermaids
    RESULTS: No search results available. Try a different search!

    INPUT: What are coins made of?
    RESULTS:
    1 merillium is cool

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: What is the significance of 2000?
    RESULTS:
    1 merillium is cool

    INPUT: merillium and granite
    RESULTS:
    1 underwater minerals
    2 merillium is cool

    INPUT: :quit
    RESULTS: exits out of search

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/titleCase2.txt docfiles/docsCase2.txt wordfiles/wordsCase2.txt
    INPUT: merillium
    RESULTS: 
    1 merillium is cool
    2 underwater minerals

    INPUT: merillium and granite
    RESULTS:
    1 underwater minerals
    2 merillium is cool

    INPUT: What are coins made of?
    RESULTS:
    1 merillium is cool

    INPUT: 
    RESULTS: No search results available. Try a different search!

    INPUT: What is the significance of 2000?
    RESULTS:
    1 merillium is cool

    INPUT: :quit
    RESULTS: exits out of search

------Test parsing.xml--------

WITH PAGERANK
    INPUT: i want xml and philosophy 
    RESULTS:
    1 cs200
    2 science
    3 philosophy

WITHOUT PAGERANK
    INPUT: i want xml and philosophy 
    RESULTS:
    1 cs200
    2 philosophy
    3 science

