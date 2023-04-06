# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: scraping basics

# scraping modules
import requests
from scrapy import Selector
from selenium import webdriver
from bs4 import BeautifulSoup

# to avoid needing driver updates
from webdriver_manager.chrome import ChromeDriverManager

# pandas for csv and dataframe
import pandas as pd
import csv

# time delay for requests
import time

# only works for age poll currently
def get_results(poll):
    '''given poll element, returns most voted for value'''
    val = None
    max_votes = 0
    results = poll.xpath('.//result')
    for result in results:
        num_votes = int(result.xpath('./@numvotes').extract()[0])
        if num_votes > max_votes:
            max_votes = num_votes
            val = int(result.xpath('./@value').extract()[0])
    return val

# extract data from api structure
# https://github.com/ThaWeatherman/scrapers/tree/master/boardgamegeek
def get_val(parent, term):
    '''given parent element, returns stored value at term element'''
    try:
        val = parent.find(term)['value']
    except:
        val = 'NaN'
    return val

# using webdriver-manager so updates don't break code
driver = webdriver.Chrome(ChromeDriverManager().install())

# starting urls for game list without page number
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

#variables for use in loop
game_links = []
game_ids = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links and IDs
# first 258 pages of bgg - everything with 30 or more community votes
for i in range(1,258):

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
        game_links.append(bgg + temp_links[i])
        game_ids.append((temp_links[i]).split('/')[2])

# columns of data being collected
cols = ["type",
        "title",
        "year",
        "min_players",
        "max_players",
        # "sug_players",
        "min_time",
        "max_time",
        "avg_time",
        "min_age",
        "com_age",
        "bay_rating",
        "avg_rating",
        "num_ratings",
        "complexity",
        "comp_votes",
        "comments",
        "views",
        "fans",
        "owners",
        "traders",
        "wanters",
        "wishers",
        "mechanics",
        "categories"]

# write to file in loop
out_file = open('games_data.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(out_file)
writer.writerow(cols)

# setup for BGG API request - API stats page and how many games per page
base = 'http://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1'
games_pp = 1

game_info = []

# for each link in game_links:
for i in range(len(game_links)):

    # request API and driver stats page
    time.sleep(1)
    stats = game_links[i] + "/stats"
    driver.get(stats)
    url = base.format(game_ids[i])
    print('Requesting {}'.format(stats))
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'xml')
    items = soup.find_all('item')

    # for poll data
    html = req.content
    sel = Selector(text=html)

    # fans and page views
    try:
        fans = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[6]/div[2]/a')[0].text
        views = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[7]/div[2]')[0].text
    except:
        time.sleep(30)
        driver.get(stats)
        fans = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[6]/div[2]/a')[0].text
        views = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[7]/div[2]')[0].text


    for item in items:
        type = item['type']
        title = get_val(item, 'name')
        year = get_val(item, 'yearpublished')
        min_players = get_val(item, 'minplayers')
        max_players = get_val(item, 'maxplayers')


        # TODO: get suggested number of players from community poll
        # best number of players poll
        # play_poll = sel.xpath('//poll[@name="suggested_numplayers"]')
        # sug_players = max(get_results(play_poll))
        # print(title, sug_players)

        # time = get_val(item, 'playingtime')
        min_time = int(get_val(item, 'minplaytime'))
        max_time = int(get_val(item, 'maxplaytime'))
        if min_time != 'NaN' and max_time != 'NaN':
            avg_time = (min_time + max_time) / 2
        else:
            avg_time = 'NaN'

        geek_age = get_val(item, 'minage')
        age_poll = sel.xpath('//poll[@name="suggested_playerage"]')
        com_age = get_results(age_poll)

        bay_rating = get_val(item.statistics.ratings, 'bayesaverage')
        avg_rating = get_val(item.statistics.ratings, 'average')
        num_ratings = get_val(item.statistics.ratings, 'usersrated')

        complexity = get_val(item.statistics.ratings, 'averageweight')
        comp_votes = get_val(item.statistics.ratings, 'numweights')

        comments = get_val(item.statistics.ratings, 'numcomments')
        owners = get_val(item.statistics.ratings, 'owned')
        traders = get_val(item.statistics.ratings, 'trading')
        wanters = get_val(item.statistics.ratings, 'wanting')
        wishers = get_val(item.statistics.ratings, 'wishing')

        categories = [x['value'] for x in item.findAll(type='boardgamecategory')]
        mechanics = [x['value'] for x in item.findAll(type='boardgamemechanic')]

    # gather elements from /stats page
    # community_age = driver.find_elements_by_xpath\
    #     ('//ul[@class="gameplay"]/li[3]/div[2]/span/button/span')

    # get rid of commas in numbers
    # broken @ https://boardgamegeek.com/boardgame/204583/kingdomino/stats
    try:
        fans = int(fans.replace(',', ''))
    except:
        fans = 0

    try:
        views = int(views.replace(',', ''))
    except:
        views = 0


    new_row = ((type,
                title,
                year,
                min_players,
                max_players,
                # sug_players,
                min_time,
                max_time,
                avg_time,
                geek_age,
                com_age,
                bay_rating,
                avg_rating,
                num_ratings,
                complexity,
                comp_votes,
                comments,
                views,
                fans,
                owners,
                traders,
                wanters,
                wishers,
                mechanics,
                categories))

    # list for data frame, write row to file
    # game_info.append(new_row)
    writer.writerow(new_row)

# df = pd.DataFrame(game_info, columns= cols)

# print(df.head())
# df.to_csv('extra_extra_data.csv')

driver.close()
out_file.close()

