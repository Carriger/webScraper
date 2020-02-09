from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
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
    homeDir = os.getcwd()
    docUnits = "DocumentUnits"
    
    rawHTML = fetchFromURL('http://shakespeare.mit.edu')
    soup = BeautifulSoup(rawHTML, 'html.parser')

    allLinks = soup.find_all('a')
    
    ################the following is for handling the play links
    
##    playsLinks = allLinks[2:-7]
##    for dirItem in directoryList:
##        if os.path.isdir(dirItem) and dirItem == docUnits:
##            os.chdir(dirItem) #go into subdirectory Document Units
##            
##            for link in playsLinks:
##                link = link.get('href')
##                link = link[:-11]
##                fullTextLink = ("http://shakespeare.mit.edu/" + link + "/full.html")
##                newHTML = fetchFromURL(fullTextLink)
##                soup = BeautifulSoup(newHTML, 'html.parser')
##                HTMLlink = link + ".html"
##                    
##                fOpen = open(HTMLlink, "wb")
##                fOpen.write(newHTML)
##                fOpen.close()
##            #sends us back to the parent directory
##            os.chdir(homeDir)

    ############the following is for handling the SONNET links
    
##    sonnetMainHTML = fetchFromURL('http://shakespeare.mit.edu/Poetry/sonnets.html')
##    soup = BeautifulSoup(sonnetMainHTML, 'html.parser')
##    allSonnetLinks = soup.find_all('a')
##    allSonnetLinks = allSonnetLinks[1:]
##
##    for dirItem in directoryList:
##        if os.path.isdir(dirItem) and dirItem == docUnits:
##            os.chdir(dirItem) #go into subdirectory DocumentUnits
##
##            for sLink in allSonnetLinks:
##                sLink = sLink.get('href')
##                fullSLink = ("http://shakespeare.mit.edu/Poetry/" + sLink)
##                sonnetsHTML = fetchFromURL(fullSLink)
##                soup = BeautifulSoup(sonnetsHTML, 'html.parser')
##
##                sFOpen = open(sLink, "wb")
##                sFOpen.write(sonnetsHTML)
##                sFOpen.close()
##            #sends us back to the parent directory
##            os.chdir(homeDir)

    ############the following is for handling the remaining four poems
    
##    finalPoems = allLinks[40:-2]
##
##    for dirItem in directoryList:
##        if os.path.isdir(dirItem) and dirItem == docUnits:
##            os.chdir(dirItem) #go into subdirectory DocumentUnits
##            for fLink in finalPoems:
##                fLink = fLink.get('href')
##                fLink = fLink[7:]
##                fullFLink = ("http://shakespeare.mit.edu/Poetry/" + fLink)
##                finalHTML = fetchFromURL(fullFLink)
##                soup = BeautifulSoup(finalHTML, 'html.parser')
##
##                finalOpen = open(fLink, 'wb')
##                finalOpen.write(finalHTML)
##                finalOpen.close()
##            os.chdir(homeDir)


        ############## making the html pages into text files

##    #contents of the current working directory
##    directoryList = os.listdir('.')  # '.' indicates the current directory
##    for dirItem in directoryList:
##        if os.path.isdir(dirItem) and dirItem == docUnits:
##            os.chdir(dirItem) #go into subdirectory DocumentUnits
##            directoryList = os.listdir('.')  # '.' indicates the current directory
##            #going through html files within DocumentUnits
##            for dirItem in directoryList:
##                fileOpen = open(dirItem, 'r')
##                data = fileOpen.read()
##                fileOpen.close()
##                #text locally, how do we tokenize it?
##                soup = BeautifulSoup(data, 'html.parser')
##                extractedText = soup.get_text()
##                extractedText = extractedText.lower()
##                newDItem = dirItem[:-5] + '.txt'
##
##                fileOut = open(newDItem, "w")
##                fileOut.write(extractedText)
##                fileOut.close()
##            os.chdir(homeDir)

        ##################iterating through text files and tokenizing
    txtFiles = "TextFiles"
    directoryList = os.listdir('.')  # '.' indicates the current directory
    for dirItem in directoryList:
        if os.path.isdir(dirItem) and dirItem == txtFiles:
            os.chdir(dirItem) #go into subdirectory TextFiles
            directoryList = os.listdir('.')  # '.' indicates the current directory
            #going through html files within DocumentUnits
            for dirItem in directoryList:
                tokenDict = {}
                docID = 1            
                #isolating our text file types
                if dirItem == "LoversComplaint.txt":
                    fileOpen = open(dirItem, 'r')
                    data = fileOpen.read()
                    fileOpen.close()
                    #text locally, now tokenizing
                    tokenizedText = word_tokenize(data)
                    #anything that doesn't match this char set will be excluded
                    for term in tokenizedText:
                        if len(term) >= 4:
                            reg = re.compile('[^a-zA-Z]')
                            term = reg.sub('', term)
                            if term not in tokenDict:
                                tokenDict[term] = docID
##                                else:
##                                    temp = tokenDict[term]
##                                    if tokenDict[term] != docID:
##                                        tokenDict[term] = 
                                    
                    docID += 1
                print(tokenDict)



            
            
        



main()
