import xml.etree.ElementTree as et
#from nltk.corpus import stopwords
#STOP_WORDS = set(stopwords.words('english'))
#from nltk.stem import PorterStemmer
#nltk_test = PorterStemmer()
#nltk_test.stem("Stemming")
#To load the XML file into a tree and save the root, we can use this line:

def __init__(self, xml_file: str, title_file: str, docs_file : str, worsds_file: str):
    #what are the fields
    """
    :param xml_file: the name of the input file that the indexer will read in and parse
    :param title_file: maps document IDs to document titles
    :param doc_file: stores the rankings computed by PageRank
    :param worsds_file: 
    """
    wiki_tree = et.parse('test_files/test1_tf_idf.xml') #loads the xml file into a tree
    root = wiki_tree.getroot()#get the root of the tree
    all_pages = root.findall('page')#this gets all the pages
    for page in all_pages:
        pass
