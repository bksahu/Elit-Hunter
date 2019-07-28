import sys
import requests

from lxml.html import fromstring
from urllib.parse import urlparse

class MovieLinks:
    """
    A class to find movie links

    Attributes
    ----------
    base_link : str
        base link of the movies link website
    start : int
        starting address index
    end : int
        ending address index

    Methods
    -------
    getTitle
        returns title of the link
    checkIfLinkAlive
        returns request object if link is alive
    getLinks
        return valid links with there title
    """
    def __init__(self, base_link, start=0, end=None):
        assert type(base_link) is str
        self.base_link = base_link
        self.start = start
        self.end = end

    def getTitle(self, request):
        return fromstring(request.content).findtext('.//title')

    def checkIfLinkAlive(self, link):
        request = requests.get(link)
        if request.status_code == 200:
            return request
        return None

    def getBaseLink(self, link):
        return urlparse(link).hostname

    def getLinks(self):
        print("Scraping links...")
        if not self.end:
            self.end = sys.maxsize
        title_links = []
        for i in range(self.start, self.end):
            link = '{}/{}'.format(self.base_link, i)

            request = self.checkIfLinkAlive(link)

            if request:
                title_links.append({
                    'title': self.getTitle(request),
                    'link': link,
                    'link_id': i,
                    'website': self.getBaseLink(link)
                })
            # if next 100 links are inactive break
            if i - self.start and not self.end >= 50:
                break
        return title_links

