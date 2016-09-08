# This is a simple script used to extract the Amazon's categories and referral fees

import json

from urllib import request
from bs4 import BeautifulSoup

req = request.Request(
            'https://www.amazon.com/gp/help/customer/display.html?nodeId=1161240',
            headers={'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'}
        )
r = request.urlopen(req).read()
soup = BeautifulSoup(r, 'lxml')

# Returns a dictionary[category] = [percentage, flat fee]
def get_referral_costs(cost_dict):
    for td in soup.find_all('td', string='3D Printed Products'):
        tr = td.parent
        x = 2
        for td in tr.parent.find_all('td'):
            if x > 5:
                if not x % 3:
                    if not td.string:
                        td.string = 'Everything Else'
                    category = td.string
                    cost_dict[category] = []
                else:
                    if td.string:
                        cost_dict[category].append(td.string)
                    else:
                        cost_dict[category].append("--")
            x += 1
    return cost_dict

# Returns a list of categories
def get_categories(cat_list):
    for td in soup.find_all('td', string='3D Printed Products'):
        tr = td.parent
        x = 2
        for td in tr.parent.find_all('td'):
            if x > 5:
                if not x % 3:
                    if not td.string:
                        td.string = 'Everything Else'
                    cat_list.append(td.string)
            x += 1
    return cat_list

if __name__ == '__main__':
    category_list = get_categories([])
    with open('data.json', 'w') as outfile:
        json.dump(category_list, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
