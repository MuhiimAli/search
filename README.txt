Muhiim Ali, Jennifer Chen

1.Known Bugs:
    Words with apostrophes

2. User Instructions:

When query.py is run, the user can input any word or phrase into the terminal. Pressing the enter button runs query and 
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
    The weights between documents are then calculated and the weight dictionary is populated.

[QUERY]
    File query.py is the querier that parses in arguments for the index files and accounts for if pagerank will be used in the 
    search or not. The querier runs a RELP that takes in and proceses queries (searches). The querier then 
    ranks documents against the queries based on term relevance and, if specified, PageRank from the index files. These index
    files are the word file, doc file, and title file. 

[TESTING]

    Test_search contains the unit tests that were used to check for the functionality of index and query as we coded.
Tests were made by creating an insance of Index and texting if the dictionaries and methods were outputting properly. 


4.Extra/Unimplemented Features: None

5.Unit Testing:

    [INDEX.PY]

    [QUERY.PY]

6.System Testing:


Test_empty
    test empty search produces

Test test_query.xml
    INPUT: "horse"

    INPUT: "horse's"

Test testingcase2.xml
    INPUT: merillium

