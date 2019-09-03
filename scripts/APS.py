"""
scraper to pull journal info from APS journals
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# holds information about an individual volume
class volume:
    """
    small class to hold information about an individual volume
    """
    # initialize object
    def __init__(self):
        self.nIssues=0
        return
    # index all issues in this volume
    def indexIssues(self,url):
        html=urlopen(url)
        soup=BeautifulSoup(html,'html.parser')
        features=soup.find_all('b')
        self.nIssues=len(features)
        
        return

# Class to hold information involving all APS journals
# input abbreviation (e.g., PRL, PRB etc)
class APS:
    """
    aps journal main class
    """
    def __init__(self,abbrev,url='https://journals.aps.org/'):
        """
        initialize class
        
        Notes
        -----
        This is still incomplete

        Parameters
        ----------
        abbrev : journal abbreviation
        url : base url of journal
        """
        self.abbrev=abbrev
        self.baseurl=url+abbrev+'/'
        self.volumeurl=url+abbrev+'/issues/'
        return
    
    # scrape the information about # of volumes
    def indexVolumes(self):
        html=urlopen(self.volumeurl)
        soup=BeautifulSoup(html,'html.parser')

        features=soup.find_all('a',href=True)
        self.volumes={}
        self.nVolumes=0
        for f in features:
            if '/'+self.abbrev+'/issues/' in f['href']:
                string=f['href'].strip('/'+self.abbrev+'/issues/')
                loc=string.find('#')
                if loc != -1:
                    self.volumes.update({string[:loc]:volume()})
                    self.nVolumes=self.nVolumes+1

        return
    # scrape info about number of issues in each volume
    # if All is true, it indexes all volumes, otherwise only volume num
    # verbose gives status updates, skipping (skip) # of steps
    def indexIssues(self,All=True,num=1,verbose=False,skip=1):
        self.nIssues=0
        if All:
            n=0
            for i in self.volumes:
                if verbose and n%skip==0:
                    print(str(n)+'/'+str(len(self.volumes)))
                n=n+1
                url=self.volumeurl+i+'#v'+i
                self.volumes[i].indexIssues(url)
                self.nIssues=self.nIssues+self.volumes[i].nIssues
            return
        else:
            url=self.volumeurl+str(num)+'#v'+str(num)
            self.volumes[str(num)].indexIssues(url)
            
            return
    
    # print a link to a chosen volume/issue
    # if vol==False, links to the current page
    def link(self,vol=False,iss=1):
        if vol:
            return self.volumeurl+str(vol)+'/'+str(iss)
        else:
            return self.baseurl

    #Functions to scrape an issue to retrive all article information.
    #Input is base URL. Output is list of article names, corresponding 
    #authors, DOI, keywords, etc.
    
    #Function to get the months range and year for the volume/issue
    def monthRange(self, v, i):
        issURL = self.link(vol = v, iss = i )
        html=urlopen(issURL)
        soup=BeautifulSoup(html,'html.parser')

        head = soup.find_all('div',class_="panel")
        rng = head[0].find('h5').get_text().split()
#        months = rng.getText()
#        print(head[0])
#        print(rng.get_text())
        print(' '.join(rng))
        #String manipulation to extract month range and year
        mos = rng[0] + ' - ' + rng[2]
        yr = rng[-1]
        return [mos, yr]
    
    #Method to get issue titles
    def issueListing(self, v, i):
        """
        Lists out all the papers in the specified volume and issue.
        Inputs:
        v: journal volume number
        i: journal issue number
        """
        #list of URLS within the issue
#        links = []
        issURL = self.link(vol = v, iss = i )
        html=urlopen(issURL)
        soup=BeautifulSoup(html,'html.parser')
        URLs = [] #Empty list
        
#        titles = soup.find_all('h5', class_="title")
#        authors = soup.find_all('h6', class_="authors")
#        pubs = soup.find_all('h6', class_="pub-info")
#        for t, a, p in zip(titles, authors, pubs):
        blocks = soup.find_all('div', class_="article panel article-result")
        for b in blocks:
#            print(b)
            titletag = b.find('h5', class_="title")
            title = titletag.get_text()
            #Extract abstract url from title head
            aURL = titletag.find('a', href = True)['href']
            alink = 'https://journals.aps.org' + aURL
            #Print out the scraped information
            print(title)
            print(alink)
            #Extract research area and topic keywords
            kwlist = b.find('ul', class_="inline-list subjects")
            #If the list tag exists
            if kwlist:
                lis = kwlist.find_all('li')
                kws = [li.get_text() for li in lis]  
                print(kws)
                #Add utf-8 encode
#                print(kws.encode('utf-8'))            
            print('----------------------------------------------------------------')        
            #Collect URLs in the issue
            URLs.append('https://journals.aps.org' + aURL)
        return URLs
    

    
class Article:
    """
    Article class 
    Attributes: Paper ID, URL, title, authors, journal, year, volume, issue, article number,
    page numbers, keywords, DOI number,  
    Methods: abstract, formatted citation string, citations to, citations from
    """
    #Pass on inherited values from the upper classes
    def __init__(self, url):
        #Input article URL
        html = urlopen(url)
        soup = BeautifulSoup(html,'html.parser')
#        infos = soup.find_all('meta', name = "citation_title")
        infos = soup.find_all("meta", {"name" : re.compile(r"citation_*")})
#        print(infos)
        #Strip content values and assign to article attributes
        self.Publisher = infos[0]['content']
        self.Title = infos[1]['content']
        self.pubdate = infos[2]['content']
        self.DOI = infos[3]['content']
        self.Journal = infos[4]['content']
        self.jour = infos[5]['content']
        self.vol = infos[6]['content']
        self.iss = infos[7]['content']
        self.pgone = infos[8]['content']
        return
        
    
    #Create article ID
#    def articleID(self, url):
#        """
#        Method to create an article ID for the specified article
#        """    
#        html=urlopen(url)
#        soup=BeautifulSoup(html,'html.parser')
#        features=soup.find_all('b')
#        
#        return    
#    def articleAuthors():
#       """
#       Method to extract authors. 
#       Handles the author affiliations.
#       Adds new author name to Authors database.
#       """
    
#    def articleKeywords(self, v, i):
#        """
#        Method to extract keywords. 
#        Adds new keywords to Keywords database.
#        """
#        issURL = self.link(vol = v, iss = i )
#        html=urlopen(issURL)
#        soup=BeautifulSoup(html,'html.parser')
#        keylists = soup.find_all('ul', class_="inline-list subjects")
#        for ks in keylists:
#            kw = ks.find_all('li')
#            keywords = [li.get_text() for li in kw]
#            print(keywords)
#        return
    def viewAbstract(self):
        """
        Method to print out the abstract for the article
        """
        #Encode text as utf-8