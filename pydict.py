#!/usr/bin/env python
# coding=UTF-8
import httplib, urllib,string,sys
from HTMLParser import HTMLParser

red="\33[31;1m"
lindigo="\33[36;1m"
indigo="\33[36m"
green="\33[32m"
yellow="\33[33;1m"
blue="\33[34;1m"
org="\33[0m"
light="\33[0:1m"
map=str(" æa:   ɑ       ʊɔɝəɚʌeɛŋ ʃʒ θð   iɪuopbtdkfvszmnhlrwj`,g ḷṃṇ").decode("UTF-8")
class MyHTMLParser(HTMLParser):
    show=0
    prefix=""
    postfix=org
    entry=1
    error=0
    redirect=0
    kkmode=0
    imgmode=0
    chimode=0
    pron=""
    result=[]
    def handle_starttag(self, tag, attrs):
        if tag == "div" and len(attrs)!=0:
                if attrs[0][1]=="pexplain":
                        self.show=1
                        self.prefix="  "+str(self.entry)+"."
                        self.entry+=1
                elif attrs[0][1]=="peng":
                        self.show=1
                        self.prefix="    "+indigo
                elif attrs[0][1]=="pchi":
                        self.show=1
                        self.prefix="    "+green
                elif attrs[0][1]=="ptitle":
                        self.kkmode=1
                        self.result.append(blue+"KK:[")
                        self.pron=""
                elif attrs[0][1]=="chinese-explain pexplain":
                        self.chimode=1
                elif attrs[0][1]=="pcixin":
                        self.show=1
                        self.prefix=red
        elif tag == "img" and self.kkmode==1:
               self.pron+=map[int(attrs[0][1][40:43])]
        elif tag == "em" and attrs[0][1] == "warning":
                self.error=1
        elif tag == "br" and self.kkmode == 1:
                self.result.append(self.pron.encode("UTF-8")+"]\n")
                self.pron=""
                self.result.append("DJ:[")
        elif tag == "li" and self.chimode ==1:
                self.show=1
        elif tag == "a" and self.error ==1:
                if len(attrs) == 1 and attrs[0][1]!="/azindex":
                        self.redirect=1
                else:
                        self.result.append(yellow+"Not Found!"+org+"\n")
                self.error=0
                

    def handle_data(self,data):
        if self.show == 1:
                self.result.append(self.prefix+data+self.postfix+"\n")
                self.show=0
        if self.redirect == 1:
                self.result.append("Spell Check: ["+yellow+data+org+"]\n")
                dict(data)
                self.redirect=0

    def handle_endtag(self, tag):
        if tag == "div":
                if self.kkmode ==1:
                        self.kkmode=0
                        self.result.append(self.pron.encode("UTF-8")+"]"+org+"\n")
                elif self.chimode==1:
                        chimode=0

        if tag == "img":
                imgmode=0
                

def showkk(attrs):
        for i in attrs:
                map[int(i[1][40:43])]
def dict(word):
        output=""
        print light+word+org
        h1=httplib.HTTPConnection("tw.dictionary.yahoo.com")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        params = urllib.urlencode({'p': word ,'ei' : 'UTF-8'})
        h1.request("POST", "/search",params, headers)
        r1=h1.getresponse()
        data1 = r1.read()
        index=string.index(data1,"sc\'")
        data=data1[0:index]
        data=data.replace("&#39;",'\'')
        data=data.replace("<b>",lindigo)
        data=data.replace("</b>",org)
        p=MyHTMLParser()
        p.feed(data)
        for s in p.result:
                output+=s
        print output
        
while(1):
        try:
                word=raw_input("<PyDict> ")
        except KeyboardInterrupt:
                print ""
                exit()
        dict(word)