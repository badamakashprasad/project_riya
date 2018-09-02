from bs4 import BeautifulSoup
import requests
import re
from nltk.tokenize import sent_tokenize,word_tokenize
import nltk
class WikiData:

    def __init__(self, query):
        self.query = query

    def soupobject(self):
        a = requests.get("https://en.wikipedia.org/wiki/" + self.query)
        plain_text = a.text
        soup = BeautifulSoup(plain_text, "html.parser")
        return soup

    def textExtraction(self):
        soup = self.soupobject()
        s = soup.find('p').text
        s = re.sub(r'\[.*?\]|\(.*?\)','',s)
        sentence = sent_tokenize(s)
        words = word_tokenize(s)
        #print(nltk.pos_tag(word_tokenize(sentence[0])))
        ls = nltk.pos_tag(word_tokenize(sentence[0]))
        print(ls)
        #namedEnt = nltk.ne_chunk(ls)
        #print(namedEnt)




