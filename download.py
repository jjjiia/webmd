#!/usr/bin/env python

import urllib2
import sys
import json
from bs4 import BeautifulSoup, NavigableString
import re
import csv
import datetime
import os
import time
import random
from HTMLParser import HTMLParser
import urlparse, urllib
import string
import urllib2,cookielib
import math
duplicates = []
latestDictionary = {}

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def removeTags(html, *tags):
    soup = BeautifulSoup(html)
    for tag in tags:
        for tag in soup.findAll(tag):
            tag.replaceWith("")

    return soup
def download_conditions(url):
    import urllib2,cookielib
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "error "
        pass
        #print e.fp.read()
    content = page.read()
    soup = BeautifulSoup(content)
   # main = soup.find_all("div",{"class":"a-to-z list"})
    for div in soup.find_all("div",{"class":"a-to-z list"}):
        a = div.find_all('a')
        for link in a:     
            print link
    #print main

def loop_alphabet():
    #get links from all pages with conditions etc listed
    #pages = list(string.ascii_lowercase)
    pages = ['default', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    baseURL = "http://www.webmd.com/a-to-z-guides/health-topics/"
    for page in pages:
        url = baseURL+page+".htm"
        #print url
        download_conditions(url)


def findCancer(text,links):
    if "cancer" in str(text).lower() or "cancer" in str(links).lower():
        #find cancer index and surrounding text

        index = str(main).lower().index("cancer")
        cancerContext = str(main)[index-50: index+50]
        return ["true",cancerContext]
    else:
        return ["false","NA"]

#url = "http://www.webmd.com/skin-problems-and-treatments/tc/sunburn-topic-overview"
url = "http://www.webmd.com/heartburn-gerd/default.htm"
keyword = "cancer"
links = []
steps = 1


def download_content(url,outputfile):
    pages = []
    print "NEW LOOP"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
           
    #download url
    req = urllib2.Request(url, headers=hdr)
    try:
        page = urllib2.urlopen(req)
        content = page.read()
        soup = BeautifulSoup(content)
        main = soup.find_all("p")
        title = strip_tags(str(soup.title))

        outputRow = [title,url]
        #check for word
        if "cancer" in str(main).lower() or "cancer" in str(soup.title).lower():
            #find index and get text fragment
            index = str(main).lower().index("cancer")
            cancerContext = str(main)[index-50: index+60]
            outputRow.append([True, cancerContext])
           # print "NEXT"
        else: 
            #if no word, check links 
            outputRow.append([False, "NA"])
        
        for div in soup.find_all("div",{"id":"ContentPane5"}):
            a = div.find_all('a')
    
    
            links = []
            for link in a:
                linkContent = link.get('href')
                links.append(linkContent)
            outputRow.append(links)
            print title, len(links)
    
    
        #print "loop: ",loops, ", title:",title,", links: ",len(links)
    
        with open(outputfile, "a") as output:
            #print "WRITE NEW ROW"
            spamwriter = csv.writer(output)
            spamwriter.writerow(outputRow)
            
    except urllib2.HTTPError, e:
        print "error "
        return
        #print e.fp.read()
    
#    loops +=1
#    
#    #go to the links
#    for link in a:
#        #print link
#        linkContent = link.get('href')
#        try:
#            download_content(linkContent,outputfile,loops)
#            print "for links:", loops
#        except urllib2.URLError:
#            pass
#        if len(link) ==0:
#            return
#    if loops >5:
#        return

def openLinks(csvfile,outputfile):
    with open(csvfile,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            print "NEW SUBJECT", row[0]
            url = row[0]
            download_content(url,outputfile)
            time.sleep(random.random()*3)
            #break
openLinks("health_topics.csv","health_topics_1.csv")
#download_content(url,"test.csv",0)
