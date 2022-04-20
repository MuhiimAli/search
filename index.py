import xml.etree.ElementTree as et
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
nltk_test.stem("Stemming")
#To load the XML file into a tree and save the root, we can use this line:
root: ElementTree = et.parse(<xml filepath>).getroot()git