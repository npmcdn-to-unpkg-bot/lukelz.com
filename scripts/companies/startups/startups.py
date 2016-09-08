# This script parses Angel.co company pages for their tech stacks.
# Just input a list of companies and a dictionary to hold the self.dict_data.

# import time
# import random
import json
from urllib import request, error
from bs4 import BeautifulSoup

class AngelList:
    """Attributes
    root_category: tech stack root category key codes
    """

    root_categories = {
            '323': 'Engineering',
            '331': 'DevOps',
            '332': 'Products',
            '333': 'Sales and Marketing',
            '334': 'Operations',
        }

    def __init__(self, company_name):
        self.name = company_name
        self.angel_url = 'https://angel.co/' + str(self.name)
        req = request.Request(
            self.angel_url,
            headers={'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'}
        )
        try:
            r = request.urlopen(req).read()
            soup = BeautifulSoup(r, 'lxml')
            self.locations = self.update_locations(soup)
            self.markets = self.update_markets(soup)
            self.size = self.update_size(soup)
            self.stack = self.update_stack(soup)
            print(str(self.name) + "'s AngelList data added.")
        except (error.HTTPError, UnicodeEncodeError):
            print("Could not get " + str(self.name) + "'s AngelList data!")
        """
        soup = BeautifulSoup(open('angel_pinterest.htm'), 'lxml')
        self.locations = self.update_locations(soup)
        self.markets = self.update_markets(soup)
        self.size = self.update_size(soup)
        self.stack = self.update_stack(soup)
        """

    def update_locations(self, soup):
        locations = []
        for span in soup.find_all('span', class_='js-location_tags'):
            for a in span.find_all('a', class_='tag'):
                locations.append(a.string)
        return locations

    def update_markets(self, soup):
        markets = []
        for span in soup.find_all('span', class_='js-market_tags'):
            for a in span.find_all('a', class_='tag'):
                markets.append(a.string)
        return markets

    def update_size(self, soup):
        span = soup.find('span', class_='js-company_size')
        if span:    
            return span.string[1:-1] # Remove newline chars

    # Update stack for specific company
    def update_stack(self, soup):
        stacks = {}
        for a in soup.find_all('a', class_='u-actAsLink category'):
            category = a.string[1:-1] # Removes newline chars
            key = a.parent.parent.parent['data-category'] # The root category key used by angel.co
            name = a.parent.a.string
            stacks[name] = {'category': category, 'root_category': self.root_categories[key]}
        return stacks

class Company(AngelList):
    """Attributes:

    commended_by: [string]

    AngelList:
    location: [string]
    markets: [string]
    size: int, # employees
    stack: [{'category':, 'root_category':, 'count':}]
    stage: string, 'series A/B/C'
    signal: int
    
    GlassDoor:
    salary: int
    career_opportunity: double
    work_life_balance:
    colleague_quality:
    remote_work: boolean

    LinkedIn:

    """
    def __init__(self, name):
        self.name = name
        AngelList.__init__(self, name)

    def __str__(self):
        return self.name

"""Methods to get company names lists"""

# Return a list of company names from a Angel.co startup database htm file
def angelist_company_names(file):
    lst = []

    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

        for div in soup.find_all('div', class_="name"):
            if div.a:
                lst.append(div.a.text)           
        return lst

# Returns the list of top startups from the first n-pages of startupranking.com
def startupranking_company_names(num_pages):
    lst = []
    for i in range(num_pages):
        req = request.Request(
            'http://startupranking.com/top/united-states/' + str(i + 1),
            headers={'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'}
        )
        r = request.urlopen(req).read()
        soup = BeautifulSoup(r, 'lxml')

        for div in soup.find_all('div', class_="name"):
            if div.a:
                name = div.a.text
                name = name.replace(" ", "-")
                name = name.replace(".", "-")
                b = name.encode('utf-8')
                name = b.decode('utf-8')
                lst.append(name)
    return lst


if __name__ == '__main__':
    company_names = [
        "socotra",
        "magic",
        "airtable",
        "benchling",
        "affinity",
        "theartistunion",
        "comma-ai",
        "gigster",
        "triplebyte",
        "opendoor",
        "angellist",
        "quip",
        "soylent",
        "color-genomics",
        "blend-labs",
        "checkr",
        "wealthfront",
        "affirm",
        "docker",
        "wish",
        "doordash",
        "meteor",
        "medium",
        "clever",
        "reddit",
        "asana",
        "oscar-health",
        "quora",
        "zenefits",
        "gusto",
        "buzzfeed",
        "magic-leap",
        "teespring",
        "intercom",
        "stripe",
        "slack",
        "lyft",
        "uber",
        "pinterest",
        "airbnb",
    ]

    data = []
    for name in company_names:
        company = Company(name)
        data.append({
            name, {
                'locations': company.locations,
                'markets': company.markets,
                'size': company.size,
                'stack': company.stack,
            }
        })

    with open('home/static/data/new_breakoutlist.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


