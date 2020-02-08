from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re


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
    rawHTML = fetchFromURL('http://shakespeare.mit.edu')
    soup = BeautifulSoup(rawHTML, 'html.parser')
    #wb is binary mode and makes no changes as data is written
##    f = open("main.html", 'wb')
##    f.write(rawHTML)
##    f.close()
##    f = open("main.html", "r")
##    data = f.read()

    allLinks = soup.find_all('a')
    
    ################the following is for handling the play links
    
##    playsLinks = allLinks[2:-7]
##    
##    for link in playsLinks:
##        link = link.get('href')
##        link = link[:-11]
##        fullTextLink = ("http://shakespeare.mit.edu/" + link + "/full.html")
##        newHTML = fetchFromURL(fullTextLink)
##        soup = BeautifulSoup(newHTML, 'html.parser')
##        HTMLlink = link + ".html"
##        fOpen = open(HTMLlink, "wb")
##        fOpen.write(newHTML)
##        fOpen.close()

    ############the following is for handling the SONNET links
    
##    sonnetMainHTML = fetchFromURL('http://shakespeare.mit.edu/Poetry/sonnets.html')
##    soup = BeautifulSoup(sonnetMainHTML, 'html.parser')
##    allSonnetLinks = soup.find_all('a')
##    allSonnetLinks = allSonnetLinks[1:]
##
##    for sLink in allSonnetLinks:
##        sLink = sLink.get('href')
##        fullSLink = ("http://shakespeare.mit.edu/Poetry/" + sLink)
##        sonnetsHTML = fetchFromURL(fullSLink)
##        soup = BeautifulSoup(sonnetsHTML, 'html.parser')
##
##        sFOpen = open(sLink, "wb")
##        sFOpen.write(sonnetsHTML)
##        sFOpen.close()

    ############the following is for handling the remaining four poems
    
##    finalPoems = allLinks[40:-2]
##    for fLink in finalPoems:
##        fLink = fLink.get('href')
##        fLink = fLink[7:]
##        fullFLink = ("http://shakespeare.mit.edu/Poetry/" + fLink)
##        finalHTML = fetchFromURL(fullFLink)
##        soup = BeautifulSoup(finalHTML, 'html.parser')
##
##        finalOpen = open(fLink, 'wb')
##        finalOpen.write(finalHTML)
##        finalOpen.close()

##        fOpen = (link, "r")
##        data = f.read()
    #text locally, how do we tokenize it?

##    soup = BeautifulSoup(data, 'html.parser')
##    extractedText = soup.get_text()
##    extractedText = extractedText.lower()
##    tokenizedText = word_tokenize(extractedText)
    #print(tokenizedText)
    
    #anything that doesn't match this char set will be excluded
##    for term in tokenizedText:
##        reg = re.compile('[^a-zA-Z]')
##        term = reg.sub('', term)
##        print(term)


main()
