import sys
import requests
import asyncio
import concurrent.futures

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
        self.title_links = None

    def getTitle(self, response):
        return fromstring(response.content).findtext('.//title')

    def getBaseLink(self, link):
        return urlparse(link).hostname

    def getLink(self, response):
        return response.url

    def getLinkId(self, link):
        return link.split("/")[-1]

    async def checkForAliveLinks(self):
        title_links = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            responses = [
                loop.run_in_executor(
                    executor,
                    requests.get,
                    "{}/{}".format(self.base_link, i)
                )
                for i in range(self.start, self.end)
            ]
            for response in await asyncio.gather(*responses):
                if response.status_code == 200:
                    link = self.getLink(response)
                    title_links.append({
                        'title': self.getTitle(response),
                        'link': link,
                        'link_id': self.getLinkId(link),
                        'website': self.getBaseLink(link)
                    })

        self.title_links = title_links
        print("Done")

    def getLinks(self):
        print("Scraping links...", end="")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.checkForAliveLinks())
        return self.title_links

