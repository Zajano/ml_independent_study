# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: using BGG API requests to gather limited data

# scraping modules
import requests
from scrapy import Selector
from bs4 import BeautifulSoup

# for csv writing
import csv

# time delay for requests
import time

""" DEFINE FOR PROGRAM USE """
# output file name
file_name = 'games_data'

# choose order to gather games in and how many
# NOT FUNCTIONAL
# By number of votes = 1
# By BGG ranking = 2
order = 1
num_pages = 257

""" END DEFINITIONS """

# extract data from api structure
# https://github.com/ThaWeatherman/scrapers/tree/master/boardgamegeek
def get_val(tag, term):
    '''extract value from target in parent elements of BGG API'''
    try:
        val = tag.find(term)['value']
    except:
        val = 'NaN'
    return val

# starting urls for game list without page number
# order by number of votes
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

#variables for use in loop
# game_links = []
game_ids = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
# first 256 pages of bgg
for i in range(1,256):

    # build on base url to iterate through pages
    url = url1 + str(i) + url2

    # gets html content from given url
    time.sleep(1)
    print(i)
    html = requests.get(url).content

    # selector object to navigate
    sel = Selector(text = html)

    # built path from analyzing html
    x_path = '//tr[@id="row_"]/td[2]/a/@href'

    # extract text value from navigated path
    temp_links = sel.xpath(x_path).extract()

    # append the site name to get the full URL and ID of games
    for i in range(len(temp_links)):
        # game_links.append(bgg + temp_links[i])
        game_ids.append((temp_links[i]).split('/')[2])


# column of data to be collected
cols = ['type',
        'name',
        'year',
        'min_players',
        'max_players',
        'avg_time',
        'min_time',
        'max_time',
        'min_age',
        'users_rated',
        'avg_rating',
        'bay_rating',
        'owners',
        'traders',
        'wanters',
        'wishers',
        'total_comments',
        'weight_votes',
        'complexity',
        'categories',
        'mechanics']


# setup for BGG API request - API stats page and how many games per page
base = 'http://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1'
games_pp = 30

# file to write to for data
out_file = open(file_name + '.csv', 'w', encoding='utf-8')
writer = csv.writer(out_file)
writer.writerow(cols)

games = []

for i in range(0, len(game_ids), games_pp):
    url = base.format(','.join(game_ids[i:i+games_pp]))
    print('Requesting {}'.format(url))
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'xml')
    items = soup.find_all('item')
    for item in items:
        gtype = item['type']
        gname = get_val(item, 'name')
        gyear = get_val(item, 'yearpublished')
        gmin = get_val(item, 'minplayers')
        gmax = get_val(item, 'maxplayers')
        # gplay = get_val(item, 'playingtime')
        gminplay = get_val(item, 'minplaytime')
        gmaxplay = get_val(item, 'maxplaytime')
        if gminplay != 'NaN' and gmaxplay != 'NaN':
            gplay = (gminplay + gmaxplay) / 2
        else:
            gplay = 'NaN'

        gminage = get_val(item, 'minage')
        usersrated = get_val(item.statistics.ratings, 'usersrated')
        avg = get_val(item.statistics.ratings, 'average')
        bayesavg = get_val(item.statistics.ratings, 'bayesaverage')
        owners = get_val(item.statistics.ratings, 'owned')
        traders = get_val(item.statistics.ratings, 'trading')
        wanters = get_val(item.statistics.ratings, 'wanting')
        wishers = get_val(item.statistics.ratings, 'wishing')
        numcomments = get_val(item.statistics.ratings, 'numcomments')
        numweights = get_val(item.statistics.ratings, 'numweights')
        avgweight = get_val(item.statistics.ratings, 'averageweight')
        categories = [x['value'] for x in item.findAll(type='boardgamecategory')]
        mechanics = [x['value'] for x in item.findAll(type='boardgamemechanic')]

        new_row = ((gtype,
                     gname,
                     gyear,
                     gmin,
                     gmax,
                     gplay,
                     gminplay,
                     gmaxplay,
                     gminage,
                     usersrated,
                     avg,
                     bayesavg,
                     owners,
                     traders,
                     wanters,
                     wishers,
                     numcomments,
                     numweights,
                     avgweight,
                     categories,
                     mechanics))

        writer.writerow(new_row)

    #pause before another API request is made
    time.sleep(2)

print("~~~~~~~~~~~~Scraping complete!~~~~~~~~~~~~")
out_file.close()