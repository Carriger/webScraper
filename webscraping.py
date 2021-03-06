"""
Author: Travis Carriger
Description: file that will scrape web pages, tokenize, and output
a JSON file."""


from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
import re
import os.path
import os
import json


def fetchFromURL(url):
    #fetch content from URL via HTTP GET request
    try:
        with closing(get(url, stream = True)) as resp:
            if isGoodResponse(resp):
                return resp.content
            else:
                print("Error retrieving information")

    except RequestException as e:
        logError('Error during request to {0}:{1}' . format(url, str(e)))

def isGoodResponse(resp):
    #Returns true if response looks like HTML
    contentType = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and contentType is not None
            and contentType.find('html')> -1)

def logError(e):
    #log the errors or you'll regret it later...
    print(e)

def main():
    directoryList = os.listdir('.')  # '.' indicates the current directory
    #saving our main directly for later use
    homeDir = os.getcwd()
    rawHTML = fetchFromURL('http://shakespeare.mit.edu')
    soup = BeautifulSoup(rawHTML, 'html.parser')
    #finding all links from home page 
    allLinks = soup.find_all('a')

    ######## FUNCTION CALLS  #####################
    
    #function call to scrape plays and poems
    #these are purposely commented out so they don't
            #perform every time
    #playsScraper(allLinks, directoryList, homeDir)
    #sonnetScraper(directoryList, homeDir)
    #finalFewPoems(allLinks, directoryList, homeDir)
    #makingTextFiles(directoryList, homeDir)
    
    #funtion call to tokenize and porter stemmer
    tokenDict = tokenizer(directoryList, homeDir)
    #function call to kick off our JSON converter
    #JSONConverter(tokenDict)

    #functions to make our bigram index and JSONBiGrams 
    biGramsDict = biGramHelper(tokenDict)
    JSONBigram(biGramsDict)
    
    ################the following is for handling the play links
def playsScraper(allLinks, directoryList, homeDir):
    playsLinks = allLinks[2:-7]
    docUnits = "DocumentUnits"
    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == docUnits:
            os.chdir(dirItem) #go into subdirectory Document Units
            
            for link in playsLinks:
                link = link.get('href')
                link = link[:-11]
                fullTextLink = ("http://shakespeare.mit.edu/" + link + "/full.html")
                newHTML = fetchFromURL(fullTextLink)
                soup = BeautifulSoup(newHTML, 'html.parser')
                HTMLlink = link + ".html"
                    
                fOpen = open(HTMLlink, "wb")
                fOpen.write(newHTML)
                fOpen.close()
            #sends us back to the parent directory
            os.chdir(homeDir)

    ############the following is for handling the SONNET links
def sonnetScraper(directoryList, homeDir):
    docUnits = "DocumentUnits"
    sonnetMainHTML = fetchFromURL('http://shakespeare.mit.edu/Poetry/sonnets.html')
    soup = BeautifulSoup(sonnetMainHTML, 'html.parser')
    allSonnetLinks = soup.find_all('a')
    #getting rid of the first link, its useless
    allSonnetLinks = allSonnetLinks[1:]


    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == docUnits:
            os.chdir(dirItem) #go into subdirectory DocumentUnits

            for sLink in allSonnetLinks:
                sLink = sLink.get('href')
                fullSLink = ("http://shakespeare.mit.edu/Poetry/" + sLink)
                sonnetsHTML = fetchFromURL(fullSLink)
                soup = BeautifulSoup(sonnetsHTML, 'html.parser')

                sFOpen = open(sLink, "wb")
                sFOpen.write(sonnetsHTML)
                sFOpen.close()
            #sends us back to the parent directory
            os.chdir(homeDir)

    ############the following is for handling the remaining four poems
def finalFewPoems(allLinks, directoryList, homeDir):
    finalPoems = allLinks[40:-2]
    docUnits = "DocumentUnits"

    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == docUnits:
            os.chdir(dirItem) #go into subdirectory DocumentUnits
            for fLink in finalPoems:
                fLink = fLink.get('href')
                fLink = fLink[7:]
                fullFLink = ("http://shakespeare.mit.edu/Poetry/" + fLink)
                finalHTML = fetchFromURL(fullFLink)
                soup = BeautifulSoup(finalHTML, 'html.parser')

                finalOpen = open(fLink, 'wb')
                finalOpen.write(finalHTML)
                finalOpen.close()
            os.chdir(homeDir)

    ############## making the html pages into text files
def makingTextFiles(directoryList, homeDir):
    docUnits = "DocumentUnits"

    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == docUnits:
            os.chdir(dirItem) #go into subdirectory DocumentUnits
            directoryList = os.listdir('.')
            #going through html files within DocumentUnits
            for dirItem in directoryList:
                fileOpen = open(dirItem, 'r')
                data = fileOpen.read()
                fileOpen.close()
                #text locally, now to tokenize
                soup = BeautifulSoup(data, 'html.parser')
                extractedText = soup.get_text()
                extractedText = extractedText.lower()
                newDItem = dirItem[:-5] + '.txt'

                fileOut = open(newDItem, "w")
                fileOut.write(extractedText)
                fileOut.close()
            os.chdir(homeDir)


    ##################   iterating through text files and tokenizing
def tokenizer(directoryList, homeDir):
    docUnits = "DocumentUnits"
    #setting up our docID file
    #docIDFile = open("DocumentID.txt", "w")
    #docIDFile.write("Document Name and corresponding ID\n\n")
    #setting up empty token dict
    tokenDict = {}
    docID = 1 
    #getting into our textfiles directory
    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == docUnits:
            os.chdir(dirItem) #go into subdirectory DocumentUnits
            directoryList = os.listdir('.')
            #going through txt files within TextFiles
            for dirItem in directoryList:
                if dirItem[-4:] == '.txt':
                    fileOpen = open(dirItem, 'r')
                    data = fileOpen.read()
                    fileOpen.close()
                    #text locally, now tokenizing
                    tokenizedText = word_tokenize(data)
                    for term in tokenizedText:
                        if len(term) >= 4:
                            #anything that doesn't match this char excluded
                            reg = re.compile('[^a-zA-Z]')
                            term = reg.sub('', term)
                            #function call to our porter stemmer
                            term = porterStemmerHelper(term)
                            #this will create our dictionary and associated document
                            #that it occurs in. If already in dict, we simply update
                            #the values list that already exists
                            if term not in tokenDict:
                                frequency = 1
                                tokenDict[term] = [[frequency],[docID]]
                            else:
                                #isolating docID
                                if docID not in tokenDict[term][1]:
                                    #isolating docID
                                    tempDocID = tokenDict[term][1]
                                    #this makes our dict values of type list
                                    tempDocID = list(tempDocID) + [docID]
                                    #updating docID
                                    tokenDict[term][1] = tempDocID
                                #isolating frequency
                                tempFreq = tokenDict[term][0]
                                tempFreq[0] += 1
                                tokenDict[term][0] = list(tempFreq)
                                
                    #writing out to our docID file
##                    writeline = (dirItem + "\t" + str(docID) + "\n")
##                    docIDFile.write(writeline)
                                    
                    docID += 1
        #sending us back to the main file folder 
        os.chdir(homeDir)
    #docIDFile.close()
    #returns our token dict
    return tokenDict

def biGramHelper(tokenDict):
    biGramsDict = {}
    for term in tokenDict.keys():
        dollarTerm = "$"+term+"$"
        index = 0
        while index < len(term)+1:
            #stepping through our terms 2 chars at a time
            biGrams = dollarTerm[index]+(dollarTerm[index + 1])
            if biGrams not in biGramsDict:
                biGramsDict[biGrams] = [term]
            else:
                temp = biGramsDict[biGrams]
                temp = temp + [term]
                #alphabetizing our terms
                temp = sorted(temp)
                biGramsDict[biGrams] = temp
            index += 1

    return biGramsDict
        

def porterStemmerHelper(term):
    porter = PorterStemmer()
    term = porter.stem(term)
    return term

    ##### Function to export our tokenDict into a JSON file
def JSONConverter(tokenDict):
    #setting up our JSON file, sort_keys alphabitizes
    with open("JSONFile.txt", "w") as outfile:
        json.dump(tokenDict, outfile, sort_keys = True)

def JSONBigram(biGramsDict):
    #setting up our JSON file, sort_keys alphabitizes
    with open("JSONBigrams.txt", "w") as outfile:
        json.dump(biGramsDict, outfile, sort_keys = True)
    
        
main()
