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
    # "NEW LOOP"
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
        cancerWordTF = False
        cancerWords = ["cancer","carcinogen","carcinogenic" ,"carcinoma" ,"Hodgkin's disease","leukaemia","leukemia","lymphoma","malignancy","malignancy","malignant tumor","melanoma","metastasis","metastasis","precancerous","sarcoma"," cancerous","metastasize", "metastatic"]
        foundCancerWords = []
        for word in cancerWords:
            if "http://www.webmd.com/cancer" in str(soup.title).lower() or word in str(soup.title).lower():
                cancerWordTF = True
                foundCancerWords.append(word)
        print foundCancerWords
                #break
       # if " cancer" in str(main).lower() or "cancer" in str(soup.title).lower() or "cancer " in str(main).lower():
            #find index and get text fragment
        if cancerWordTF == True:
            keyWord = foundCancerWords[0]
            outputRow.append([True, foundCancerWords])
            
            #try:
            #   # index = str(main).lower().index(keyWord)
            #   # #print index
            #   # if index<50:
            #   # 	cancerContext = clean(str(main)[0: index+80])
            #   # else:
            #   # 	cancerContext = clean(str(main)[index-50: index+60])
            #    outputRow.append([True, foundCancerWords])
            #except ValueError:
            #    outputRow.append([True, foundCancerWords])
            # print "NEXT"
        else: 
            #if no word, check links 
            outputRow.append([False, "NA"])
        
        links = []
        for div in soup.find_all("p"):
        #for div in soup.find_all("div",{"id":"ContentPane5"}):
            a = div.find_all('a')
    
    
            
            for link in a:
                linkContent = link.get('href')
                links.append(linkContent)
        outputRow.append(links)
        #print clean(title), len(links)
    
    
        #print "loop: ",loops, ", title:",title,", links: ",len(links)
    
        with open(outputfile, "a") as output:
            #print "WRITE NEW ROW"
            spamwriter = csv.writer(output)
            spamwriter.writerow(outputRow)
            
    except urllib2.HTTPError, e:
        print "error "
        return

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def clean(actor):
    actor = ''.join([i if ord(i) < 128 else '' for i in actor])
    return actor
    
#def cleanFirstFile(infile,outfile):
#    with open(infile,"rb") as csvfile:
#        spamreader = csv.reader(csvfile)
#        repeats=0
#        trueCount = 0
#        unique_pages = []
#        allUniquePages = []
#        finishedPages = []
#        allRepeats=0
#
#
#        for row in spamreader:
#            url = row[1]
#            finishedPages.append(url)
#        #print finishedPages
#        csvfile.seek(0)
#        for row in spamreader:
#            urls = []
#            title = clean(row[0])
#            url = row[1]
#            cancer = clean(row[2])
#            #print row
#            if "true" in cancer.lower():
#                trueCount+=1
#            if title+url in unique_pages:
#                repeats+=1
#            else:
#                unique_pages.append(title+url)
#                #print title,len(row[3].split(", "))
#                #print row
#                for link in row[3].split(","):
#                    if str(link)!= "None":
#                        cleanLink = clean(str(link))
#                        #print cleanLink
#                        cleanLink = str(link).replace("'","").replace("]","").replace("[","")
#                    
#                        if cleanLink in allUniquePages or cleanLink in finishedPages or "#" in str(cleanLink) or "http://" not in str(cleanLink):
#                            allRepeats+=1
#                        else:
#                            allUniquePages.append(cleanLink)
#                        
#                        if cleanLink in urls:
#                            repeats +=1
#                        else:
#                            urls.append(str(cleanLink))
#                    
#                newRow = [title,url,clean(str(cancer)),urls]
#        
#                with open(outfile,"a") as output:
#                    spamwriter = csv.writer(output)
#                    #print newRow
#                    spamwriter.writerow(newRow)
#
#        print trueCount
#        print "need to look up", len(allUniquePages)
#        print "allrepeats; ",allRepeats,repeats
#        return allUniquePages
                #break
def doNothing():
    doNothingCount = 0
def makeCleanLinksDictionary(infile,uniqueLinksCsv,yesCsv,noCsv,deadendNoCsv):
    uniqueLinksFile = open(uniqueLinksCsv,"w")
    uniqueLinksWriter = csv.writer(uniqueLinksFile)
    
    yesFile = open(yesCsv,"w")
    yesWriter = csv.writer(yesFile)

    noFile = open(noCsv,"w")
    noWriter = csv.writer(noFile)
    

    deadendNoFile = open(deadendNoCsv,"w")
    deadendNoWriter = csv.writer(deadendNoFile)
    
    with open(infile,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        uniqueTargetLinks = []
        trueRows = 0
        falseRows = 0
        deadends = 0
        for row in spamreader:
            #print row
            title = row[0]
            link = row[1]
            tf = row[2]
            links = row[3].replace("u'","'").replace("-fl","-flu").replace("-yo","-you").replace("-fluu","-flu").replace("-youu","-you").replace("[","").replace("]","").replace("'","").split(", ")
            cleanLinks = []
            
            
            #for each outlink, get unique ones from false pages
            for targetLink in links:
                if "http" in targetLink and "webmd" in targetLink:
                    #print targetLink
                    cleanLinks.append(targetLink)
                    if targetLink in uniqueTargetLinks:
                        #print "repeat"
                        doNothing()
                    elif "True" in tf:
                        #print "true"
                        doNothing()
                    else:
                        #print "not true, and not duplicate"
                        uniqueLinksWriter.writerow([targetLink])
                        uniqueTargetLinks.append(targetLink)
                    
            newRow = [title,link,tf,cleanLinks]
            
            #save true and false source pages in different files
            if "True" in tf:
                trueRows+=1
                yesWriter.writerow(newRow)
                
            else:
                #print "false"
                if len(links)==1:
                    #print "deadend, no cancer"
                    deadendNoWriter.writerow([title,link,tf])
                    deadends+=1
                else:
                    falseRows+=1
                    noWriter.writerow(newRow)
                
        print "true:",trueRows, " false:",falseRows,"deadends",deadends
        yesFile.close()
        noFile.close()
        deadendNoFile.close()
            #print newRow
            #break
rt = "data_redo_4/"


def makeLinkArray(infile):
    array = []
    with open(infile,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #print row[0]
            array.append(row[0])
    return array

def makeLinkArrayFromRow(infile):
    array = []
    with open(infile,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            #print row[0]
            array.append(row[1])
    return array

def openLinks(csvfile,outputfile,i):
    
    badLinks = open(rt+"badLinks.csv","a")
    badLinksWriter = csv.writer(badLinks)
    
    with open(csvfile,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        done  =0
        finishedarray = []
       # for j in range(0,i):
       #     print j
        finishedarray += makeLinkArray(rt+"uniqueLinks_0.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_1.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_2.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_3.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_4.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_5.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_6.csv")
        finishedarray += makeLinkArray(rt+"uniqueLinks_7.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_8.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_9.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_10.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_11.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_12.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_13.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_14.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_15.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_16.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_17.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_18.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_19.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_20.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_21.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_22.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_23.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_24.csv")
        ##
        #finishedarray += makeLinkArray(rt+"uniqueLinks_25.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_26.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_27.csv")
        #finishedarray += makeLinkArray(rt+"uniqueLinks_28.csv")
        
        
        #finishedarray += makeLinkArrayFromRow(rt+"uniqueLinks_2_results.csv")
       # print len(finishedarray)
        #array2 = makeLinkArray("conditions_2.csv")
        #array3 = makeLinkArray("conditions_3.csv")
        #array4 = makeLinkArray("conditions_4.csv")
        #array5 = makeLinkArray("conditions_5.csv")
        #array6 = makeLinkArray("conditions_6.csv")
        repeat = 0
        newarray = []
        for row in spamreader:
            newarray.append(row[0])
       # print newarray
        print "existing: ", len(finishedarray), " to lookup: ", len(newarray)
        newarrayNoDups = []
        for link in newarray:
            if link in finishedarray or link in newarrayNoDups:
                done+=1
            else:
                newarrayNoDups.append(link)
                
        print "need to lookup: ",len(newarrayNoDups),"done: ",done
        
#        print newarrayNoDups
        
        for url in newarrayNoDups:
            if "http:" in str(url) and "webmd" in str(url):
                print url
                try:
                    download_content(url,outputfile)
                    time.sleep(random.random())
                except:
                    print url
                    badLinksWriter.writerow([url])
                    pass
#
#openLinks("conditions_results1","conditions_results2.csv")
#download_content(url,"test.csv",0)
iteration = str(8)
plus1 = str(int(iteration)+1)
openLinks(rt+"uniqueLinks_"+iteration+".csv",rt+"uniqueLinks_"+iteration+"_results.csv",iteration)
makeCleanLinksDictionary(rt+"uniqueLinks_"+iteration+"_results.csv",rt+"uniqueLinks_"+plus1+".csv",rt+"true_"+plus1+".csv",rt+"false_"+plus1+".csv",rt+"deadendfalse_"+plus1+".csv")

#for i in range(2,30):
#    print i
#    iteration = str(i)
#    plus1 = str(int(iteration)+1)
#    openLinks(rt+"uniqueLinks_"+iteration+".csv",rt+"uniqueLinks_"+iteration+"_results.csv",i)
#    makeCleanLinksDictionary(rt+"uniqueLinks_"+iteration+"_results.csv",rt+"uniqueLinks_"+plus1+".csv",rt+"true_"+plus1+".csv",rt+"false_"+plus1+".csv",rt+"deadendfalse_"+plus1+".csv")
##    #
def checkAgain(previousFalse,linkresultsCsv,noCsv,yesCsv,deadendNoCsv):
   #make linkresults a dictionary, check in linkresults, set initial to false
    linkresultsFile = open(linkresultsCsv,"r")
    linkresultsReader = csv.reader(linkresultsFile)
    linkDictionary = {}
    for row in linkresultsReader:
        #print row[1],row[2]
        linkDictionary[row[1]]=row[2]
    #print linkDictionary
    yesFile = open(yesCsv,"w")
    yesWriter = csv.writer(yesFile)

    noFile = open(noCsv,"w")
    noWriter = csv.writer(noFile)
    
    deadendNoFile = open(deadendNoCsv,"w")
    deadendNoWriter = csv.writer(deadendNoFile)
    
    #take all false outlinks from previouse
    
    with open(previousFalse,"rb") as csvfile:
        spamreader = csv.reader(csvfile)
        notInDictionary = []
        for row in spamreader:
            #print row
            tf = False
            title = row[0]
            link = row[1]
            links = row[3].replace(" u'"," '").replace("[","").replace("]","").replace("'","").split(", ")
            #print links
            trueLinks = []
            
            for targetLink in links:
                #print targetLink
                if targetLink in linkDictionary.keys():
                    if "True" in linkDictionary[targetLink]:
                        tf = True
                        trueLinks.append(targetLink)
                else:
                    if targetLink in notInDictionary:
                        print "repeat"
                    else:
                        notInDictionary.append(targetLink)
                    print "not in the dictionary, need to look up", targetLink

            if tf == True:
                yesWriter.writerow(link,title,tf,trueLinks)
            else:
               #print "false"
               if len(links)==1:
                   #print "deadend, no cancer"
                   deadendNoWriter.writerow([title,link,tf])
               else:
                   noWriter.writerow(row)
        print notInDictionary
        print len(notInDictionary)    
#            tf = linkDictionary[link]
            #links = row[3].replace("u'","'").replace("[","").replace("]","").replace("'","").split(", ")
            #cleanLinks = []
           # print tf
    #if anylink true, change to true
    #save to true file
    #else save false file
    #save deadends
    #get unique outlinks, save to file
#checkAgain(rt+"false_initial.csv",rt+"uniqueLinks_initial_results.csv",rt+"false_1.csv",rt+"true_1.csv",rt+"deadendfalse_1.csv")
#makeCleanLinksDictionary(rt+"uniqueLinks_initial_results.csv",rt+"uniqueLinks_1.csv",rt+"true_1.csv",rt+"false_initial.csv",rt+"deadendfalse_initial.csv")


#'http://www.webmd.com/fitness-exercise/rm-quiz-sports-injury-savvy',



##print len(missing)
#download_content("http://www.webmd.com/hw-popup/melanoma-7813","test.csv")