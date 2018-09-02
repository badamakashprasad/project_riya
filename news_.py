import sqlite3
import requests
from bs4 import BeautifulSoup
import xml.sax
import csv

class DataListSql:
    def __init__(self,table):
        self.conn = sqlite3.connect('toinews.db')
        self.table = table


    def __del__(self):
        self.conn.close()

    def createtable(self):
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(self.table))
        t = cursor.fetchall()
        if not t:
            self.conn.execute(
                "CREATE TABLE {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "TITLE TEXT NOT NULL,"
                "LINK TEXT NOT NULL,"
                "DATE TEXT NOT NULL)".format(self.table))

        return

    def insertdata(self, table, title, link, date):
        self.conn.execute(
            "INSERT INTO {} (TITLE,LINK,DATE) VALUES ({},{},{})".format(table, repr(title), repr(link), repr(date)))
        self.conn.commit()
        cr = self.conn.execute("SELECT ID FROM {} WHERE LINK = {}".format(table,repr(link)))
        for r in cr:
            print(r[0])
            id = r[0]
        #d = TextReader(link)
        #d.datarecordcsv(table,id)
        return

    def selectdata(self, table, link):
        cursor = self.conn.execute("SELECT ID FROM {} WHERE LINK = {}".format(table, link))
        if cursor:
            return True
        else:
            return False


class TextReader:
    def __init__(self, url):
        self.url = url

    def soupObject(self):
        source_code = requests.get(self.url)
        plain_text = source_code.text
        return BeautifulSoup(plain_text, "html.parser")

    def dataExtract(self):
        soup = self.soupObject()
        text = []
        for data in soup.find_all('div', {'class': 'article_content clearfix'}):
            print(data.get_text())
            text.append(data.get_text())
        return text

    def datarecordcsv(self, table, id):
        text = self.dataExtract()
        record = text
        with open(table + ".csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([id, record])
            f.close()
            return True


class NewsHandlerXml(xml.sax.ContentHandler):
    def __init__(self,table):
        self.CurrentData = ""
        self.table = table
        self.title = ""
        self.guid = ""
        self.pubdate = ""
        self.record = []
        self.db = DataListSql(table)
        self.db.createtable()

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "item":
            print("Item:::::")
            self.record.clear()

    def endElement(self, tag):
        if self.CurrentData == "title":
            print("title: {}".format(self.title))
            self.record.append(str(self.title))
        elif self.CurrentData == "guid":
            print("guid: {}".format(self.guid))
            self.record.append(str(self.guid))
        elif self.CurrentData == "pubDate":
            print("pubdate: {}".format(self.pubdate))
            self.record.append(str(self.pubdate))
        self.CurrentData = ""
        if len(self.record) == 3:
            print(self.record)
            self.db.insertdata(self.table,self.record[0],self.record[1],self.record[2])
            self.record.clear()

    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "guid":
            self.guid = content
        elif self.CurrentData == "pubDate":
            self.pubdate = content


if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    conn = sqlite3.connect("toinews.db")
    cursor = conn.execute("SELECT * FROM NEWS")
    name = []
    link = []
    for row in cursor:
        name.append(row[1])
        link.append(row[2])

    conn.close()

    for n,l in zip(name,link):
        Handler = NewsHandlerXml(n)
        parser.setContentHandler(Handler)
        parser.parse(l)
        del Handler






    """
    name = "TOPNEWSTORIES"
    link = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
    Handler = NewsHandlerXml(name)
    parser.setContentHandler(Handler)
    parser.parse(link)
    """