import pytest
from indexer import Indexer

def test_parse():
    vl = Indexer('wikis/test1_tf_idf.xml')
    print(vl.parse())