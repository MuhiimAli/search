Muhiim Ali, Jennifer Chen

1.Known Bugs:
    Words with apostrophes
    numbers (2000, 1 etc) counted in the terms

2. User Instructions:

type into terminal: python3 index.py relativeWikiPath titles.txt docs.txt words.txt
type into terminal: python3 query.py (--pagerank) titles.txt docs.txt words.txt

When query.py is run, the prompt 'search>' will appear and the user can input any word or phrase into the terminal. Pressing the enter button runs search and 
produces a result. If the input does not exist in the corpus, or if the input is empty, no results will be returned and the user will
be prompted to try a new search. After every search, the user is able to search again.

3.Program:

[INDEXER]

    File index.py is the indexer that processes the XML document and stores data such as a list of terms. The indexer also calculates and stores 
information such as the relevance between terms and documents. index.py also includes the code for PageRank.

    index.py includes the main method (__init__) which takes in the xml file and the names of the word, doc, and title files that are created when indexer is run.
Indexer's main method initializes all global dictionaries and calls methods. Method calls are called in a specific order so that 
dictionaries are populated and calculations are performed in an appropriate order. Multiple global dictionaries are populated 
to help later calculations, to help calculate pagerank values, and to eventually write title, docs, and word files for each xml file.

    First, the title to page id dictionary and the page id to title dictionary is populated.
    The parse method is then called to account for links and populate dictionaries that map ids to links as well as words to doc ids to count (the amount of times a word appears in the doc).
    After the xml file is parsed though, the weights dictionary is filled. A dictionary that maps words to its idf and words to docs and the term frequencies in those docs is then also filled through
    method calls. Using the term frequency and idf dictionary, term relevance is then calculated in a method call and a dictionary that 
    maps the words to doc ids to the word's term relevance in that document is populated.

    Using these dictionaries and method calls, pagerank values can be calculated and stored within another dictionary,and the title, docs, and words files can be written for the xml file.
    Indexer thus performs all the tasks it needs to do.

[QUERY]
    File query.py is the querier that parses in arguments for the index files and accounts for if pagerank will be used in the 
    search or not. The querier runs a REPL that takes in and proceses queries (searches). The querier then 
    ranks documents against the queries based on term relevance and, if specified, PageRank from the index files. These index
    files are the word file, doc file, and title file. 

    The query has a method for ranking pages called rank_pages that takes in a list of query words that exist in the wiki as well as a dictionary that has doc ids
    mapped to total relevance. This dictionary that maps ids to relevance is populated in the method populate_total_relevance which takes in a list of 
    processed query words. 

    If query's rank_pages method finds that there are no words in the query search that would match to results in the wiki, an informative message
    will be printed out that tells the user that there are no search results and that they should try a new search. 

[TESTING]

    Test_search contains the unit tests that were used to check for the functionality of index and query as we coded.
Tests were made by creating an insance of Index and texting if the dictionaries and methods were outputting properly. 


4.Extra/Unimplemented Features: 

    If there is a tie between documents, the search results outputs/ranks the document with the lower id value first.

5.Unit Testing:

    [INDEX.PY]

    [QUERY.PY]

6. System Testing:
----Test Invalid Number of Arguments in Query----------
In the terminal, type: python3 query.py docfiles/emptyDocs.txt wordfiles/emptyWords.txt
Returns: Usage:[--pagerank] <titleIndex> <documentIndex> <wordIndex>

This notifies the user to use the appropriate format and input the correct number and type of arguments.
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

----Test breaking ties------
WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/tiebreakerTitles.txt docfiles/tiebreakerDocs.txt wordfiles/tiebreakerWords.txt

    INPUT:major
    RESULTS:
    1 tiebreaker
    2 tiebreaker second
    3 tiebreaker third

    INPUT:minor
    RESULTS:
    1 tiebreaker second
    2 tiebreaker third

    INPUT: manor 
    RESULTS:
    1 tiebreaker third

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/tiebreakerTitles.txt docfiles/tiebreakerDocs.txt wordfiles/tiebreakerWords.txt

    INPUT:major
    RESULTS:
    1 tiebreaker
    2 tiebreaker second
    3 tiebreaker third

    INPUT:minor
    RESULTS:
    1 tiebreaker second
    2 tiebreaker third

    INPUT: manor 
    RESULTS:
    1 tiebreaker third

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

-------Test testingcase1.xml-----

"""testingcase1.xml accounts for the case where a page is not linked to anything (thus being linked to every page other than itself)
as well as the case where a page is linked to a page outside of the corpus. This page outside of the corpus also contains text different fron its linked (case of having a pipe in link)"""

WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/titleCase1.txt docfiles/docsCase1.txt wordfiles/wordsCase1.txt

    INPUT: cat
    RESULTS:
    1 how are you?
    2 cat

    INPUT: cats in tulips
    RESULTS:
    1 flower garden
    2 how are you?
    3 cat

    INPUT: word
    RESULTS:
    1 cat

    INPUT: Here
    RESULTS: No search results available. Try a different search!

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/titleCase1.txt docfiles/docsCase1.txt wordfiles/wordsCase1.txt

    INPUT: cat
    RESULTS:
    1 how are you?
    2 cat   

    INPUT: which cat do you like?
    RESULTS:

    INPUT: word
    RESULTS:
    1 cat

    INPUT: Here
    RESULTS:
    No search results available. Try a different search!

-------Test testingcase2.xml-----
"""testingcase2.xml accounts for the case in which a page is linked to itself, as well as if a page is linked to a page whose link is different from the text it contains
(pipe in link)"""

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

----Testing SmallWiki-------
WITH PAGERANK
In the terminal, type: python3 query.py --pagerank titlefiles/titlesSmallWiki.txt docfiles/docsSmallWiki.txt wordfiles/wordsSmallWiki.txt

    INPUT: is history really what we think it is?
    RESULTS:
    1 carthage
    2 history
    3 military history
    4 intellectual history
    5 psychohistory
    6 utica, tunisia
    7 ash heap of history
    8 chronology
    9 war
    10 rome

    INPUT: 2000
    RESULTS:
    1 united states
    2 rome
    3 protoscholasticism
    4 germany
    5 history
    6 tertullian
    7 military history
    8 anachronism
    9 war
    10 intellectual history

WITHOUT PAGERANK
In the terminal, type: python3 query.py titlefiles/titlesSmallWiki.txt docfiles/docsSmallWiki.txt wordfiles/wordsSmallWiki.txt

    INPUT: is history really what we think it is?
    RESULTS:
    1 carthago delenda est
    2 intellectual history
    3 psychohistory
    4 outline of history
    5 historicity (philosophy)
    6 ash heap of history
    7 popular history
    8 history
    9 list of historical classifications
    10 local history

    INPUT: 2000
    RESULTS:
    1 protoscholasticism
    2 anachronism
    3 united states
    4 effects of war
    5 list of wartime cross-dressers
    6 conflict resource
    7 military history
    8 intellectual history
    9 antiquarian
    10 germany

----Testing MedWiki-----

WITH PAGERANK
In the terminal, type: python3 query.py --pagerank MedWikiTitles.txt MedWikiDocs.txt MedWikiWords.txt

    INPUT: fire
    RESULTS: 
    1 firewall (construction)
    2 empress suiko
    3 justin martyr
    4 hephaestus
    5 pale fire
    6 new amsterdam
    7 falklands war
    8 hermann g?ring
    9 guam
    10 parmenides

    INPUT: cats
    RESULTS: 
    1 netherlands
    2 pakistan
    3 morphology (linguistics)
    4 northern mariana islands
    5 kattegat
    6 hong kong
    7 normandy
    8 isle of man
    9 kiritimati
    10 grammatical gender

    INPUT: United States
    RESULTS: 
    1 netherlands
    2 ohio
    3 illinois
    4 michigan
    5 federated states of micronesia
    6 pakistan
    7 government
    8 monarch
    9 imperial units
    10 louisiana

    INPUT: united
    RESULTS:
    1 imperial units
    2 netherlands
    3 pakistan
    4 inch
    5 joule
    6 franklin d. roosevelt
    7 ohio
    8 portugal
    9 illinois
    10 oregano 

    INPUT: watch
    RESULTS:
    1 international criminal court
    2 luanda
    3 nail (fastener)
    4 fahrenheit 451
    5 meher baba
    6 joseph stalin
    7 martin waldseem?ller
    8 shock site
    9 meditation
    10 kraftwerk 

    INPUT: pope
    RESULTS:
    1 pope
    2 pope urban vi
    3 monarch
    4 pope paul vi
    5 pope gregory viii
    6 pope clement iii
    7 pope alexander iv
    8 pope benedict iii
    9 pope gregory v
    10 pope gregory xiv

    INPUT: battle
    RESULTS:
    1 navy
    2 nazi germany
    3 portugal
    4 netherlands
    5 monarch
    6 falklands war
    7 normandy
    8 paolo uccello
    9 history of the netherlands
    10 mesolithic

    INPUT: search
    RESULTS:
    1 pope
    2 empress jit?
    3 netherlands
    4 empress suiko
    5 planet
    6 new amsterdam
    7 george berkeley
    8 hinduism
    9 mercury (planet)
    10 meher baba

    INPUT: computer science 
    RESULTS: 
    1 graphical user interface
    2 portugal
    3 ontology
    4 magnetosphere
    5 j?rgen habermas
    6 planet
    7 junk science
    8 mercury (planet)
    9 john von neumann
    10 immunology

    INPUT: :quit
    RESULTS: exits out of search

WITHOUT PAGERANK
In the terminal, type: python3 query.py MedWikiTitles.txt MedWikiDocs.txt MedWikiWords.txt
    
    INPUT: fire
    RESULTS: 
    1 firewall (construction)
    2 pale fire
    3 ride the lightning
    4 g?tterd?mmerung
    5 fsb
    6 keiretsu
    7 hephaestus
    8 kab-500kr
    9 izabella scorupco
    10 justin martyr

    INPUT: cats
    RESULTS: 
    1 kattegat
    2 kiritimati
    3 morphology (linguistics)
    4 northern mariana islands
    5 lynx
    6 freyja
    7 politics of lithuania
    8 isle of man
    9 nirvana (uk band)
    10 autosomal dominant polycystic kidney

    INPUT: United States
    RESULTS: 
    1 federated states of micronesia
    2 imperial units
    3 joule
    4 knowledge aided retrieval in activity context
    5 imperialism in asia
    6 elbridge gerry
    7 martin van buren
    8 pennsylvania
    9 finite-state machine
    10 louisiana

    INPUT: united
    RESULTS:
    1 imperial units
    2 joule
    3 gauss (unit)
    4 imperialism in asia
    5 knowledge aided retrieval in activity context
    6 inch
    7 elbridge gerry
    8 fsb
    9 martin van buren
    0 los angeles international airport

    INPUT: watch
    RESULTS:
    1 shock site
    2 martin waldseem?ller
    3 g?tterd?mmerung
    4 fahrenheit 451
    5 prometheus award
    6 kraftwerk
    7 mandy patinkin
    8 nirvana (uk band)
    9 gregory chaitin
    10 luanda   

    INPUT: pope
    RESULTS:
    1 pope alexander iv
    2 pope benedict iii
    3 pope clement iii
    4 pope gregory v
    5 pope gregory viii
    6 pope gregory xiv
    7 pope formosus
    8 pope eugene ii
    9 pope alexander viii
    10 pope

    INPUT: battle
    RESULTS:
    1 paolo uccello
    2 j.e.b. stuart
    3 navy
    4 heart of oak
    5 irish mythology
    6 oda nobunaga
    7 front line
    8 girolamo aleandro
    9 mehmed ii
    10 lorica segmentata

    INPUT: search
    RESULTS:
    1 natasha stott despoja
    2 kaluza?klein theory
    3 eth
    4 php-nuke
    5 gopher (protocol)
    6 isa (disambiguation)
    7 lorisidae
    8 geocaching
    9 library reference desk
    10 demographics of liberia

    INPUT: computer science 
    RESULTS: 
    1 leo (computer)
    2 pcp
    3 junk science
    4 hacker (term)
    5 malware
    6 gary kildall
    7 motherboard
    8 foonly
    9 pvc (disambiguation)
    10 graphical user interface

    INPUT: :quit
    RESULTS: exits out of search
