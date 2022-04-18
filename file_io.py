"""
Provides functionality for reading from/writing to the 3 index files used by
indexer and querier in search
"""

def write_title_file(title: str, dictionary: dict):
    """
    Writes the dictionary of documents to titles into a file to be read in querying
    output looks like:
    id1::title1
    id2::title2

    :param title: the document that titles will get written to
    :param dictionary: a hashmap that maps a page's id to its title
    :return: n/a
    """
    with open(title, "w") as title_fh:
        for id_num, title in dictionary.items():
            title_fh.write(str(id_num) + "::" + title + "\n")


def write_document_file(docs: str, ids_to_pageranks: dict):
    """
    Writes the dictionary of ids the value of
    that page's rank from the Pagerank algorithm to be read in querying
    output looks like:
    id1 pagerank1
    id2 pagerank2
    :param docs: filepath to docs file 
    :param ids_to_pageranks: dictionary of ids --> pageranks
    :return: n/a
    """
    with open(docs, "w") as docs_fh:
        for id_num in ids_to_pageranks.keys():
            docs_fh.write(" " + str(ids_to_pageranks[id_num]))
            docs_fh.write("\n")


def write_words_file(words: str, words_to_doc_relevance: dict):
    """
    Writes the dictionary of words to ids to number of appearances

    output looks like:
    word1 id1_1 freq1_1 id1_2 freq1_2 ...
    word2 id2_1 freq2_1 id2_2 freq2_2 ...

    :param words: the file that will get written to
    :param words_to_doc_relevance: the dictionary that provides words -> ids -> term relevance
    :return: n/a
    """
    with open(words, "w") as words_fh:
        for word, ids_to_relevance in words_to_doc_relevance.items():
            words_fh.write(word + " ")
            for id_num, relevance in ids_to_relevance.items():
                words_fh.write(str(id_num) + " " + str(relevance) + " ")
            words_fh.write("\n")

def read_title_file(titles: str, ids_to_titles: dict):
    """
    reads the id and titles written in titles into the ids_to_titles dictionary

    :param titles: the file name that contains ids and titles
    :param ids_to_titles: the dictionary that ids and title will get written into
    :return: n/a
    """
    with open(titles, "r") as titles_fh:
        for line in titles_fh:
            line = line.strip()
            if line == "":
                continue
            split = line.split("::")
            ids_to_titles[int(split[0])] = split[1]


def read_docs_file(docs: str, ids_to_pageranks: dict):
    """
    reads in the pageranks written in docs to into ids_to_pageranks dictionary
    :param docs: filepath to docs file 
    :param ids_to_pageranks: dictionary of ids to pageranks 
    :return: n/a
    """
    with open(docs, "r") as docs_fh:
        for line in docs_fh:
            line = line.strip()
            if line == "":
                continue
            split = line.split(" ")
            if len(split) > 1:
                ids_to_pageranks[int(split[0])] = float(split[1])


def read_words_file(words: str, words_to_doc_relevance: dict):
    """
    reads in the term relevance written in words into words_to_doc_relevance dictionary

    :param words: the file name that the words_to_doc_frequency dictionary was written to
    :param words_to_doc_frequency: a double dictionary, where a word is a key to a dictionary
    in which an id is a key to a frequency
    :return: n/a
    """
    with open(words, "r") as words_fh:
        for line in words_fh:
            line = line.strip()
            if line == "":
                continue
            split = line.split(" ")
            word = split[0]
            for i in range(1, len(split), 2):
                page_id = int(split[i])
                relevance = float(split[i+1])
                if word not in words_to_doc_relevance:
                    words_to_doc_relevance[word] = {}
                words_to_doc_relevance[word][page_id] = relevance
