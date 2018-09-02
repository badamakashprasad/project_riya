import xml.sax
import requests
from bs4 import BeautifulSoup


class TextReader:
    def __init__(self):
        self.text = ""

    def soupObject(self, url):
        source_code = requests.get(url)
        plain_text = source_code.text
        return BeautifulSoup(plain_text)

    def dataExtract(self, url):
        soup = self.soupObject(url)
        for data in soup.find_all('div', {'class': 'article_content clearfix'}):
            print(data.get_text())


class NewsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.guid = ""
        self.pubdate = ""
        # Call when an element starts

    def startElement(self, tag,attributes):
        self.CurrentData = tag
        if tag == "item":
            print("Item:::::")

        # Call when an elements ends

    def endElement(self, tag):
        if self.CurrentData == "title":
            print("title: {}".format(self.title))
        elif self.CurrentData == "guid":
            print("guid: {}".format(self.guid))
        elif self.CurrentData == "pubDate":
            print("pubdate: {}".format(self.pubdate))
        self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "title" and content is not "Times of India":
            self.title = content
        elif self.CurrentData == "guid":
            self.guid = content
        elif self.CurrentData == "pubDate":
            self.pubdate = content


if __name__ == "__main__":
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = NewsHandler()
    parser.setContentHandler(Handler)
    parser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
