"""
scraper to pull journal info from APS journals
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

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
