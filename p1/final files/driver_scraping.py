# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: scraping BGG with a driver to crawl through pages

# scraping modules
import requests
from scrapy import Selector
from selenium import webdriver

# to avoid needing driver updates
from webdriver_manager.chrome import ChromeDriverManager

# pandas for csv and dataframe
import pandas as pd
import csv

# time delay for requests
import time

""" DEFINE FOR PROGRAM USE """
# how many pages to collect games from (100 games per page)
num_pages = 1

# output file name
file_name = 'temp_data'

""" END DEFINITIONS """

# using webdriver-manager so updates don't break code
driver = webdriver.Chrome(ChromeDriverManager().install())

# starting urls for game list (by number of votes) without page number
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

# TODO: urls for other sorting options (avg rating, rank, etc)

#variables for use in loop
game_links = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
# first 256 pages of bgg
for i in range(1,num_pages+1):

    # build on base url to iterate through pages
    url = url1 + str(i) + url2

    # gets html content from given url, make no more than 2 requests per second
    time.sleep(1)
    html = requests.get(url).content

    # selector object to navigate
    sel = Selector(text = html)

    # built path to target game link
    x_path = '//tr[@id="row_"]/td[2]/a/@href'

    # extract text value from navigated path
    temp_links = sel.xpath(x_path).extract()

    # append the site name to get the full URL of games
    for i in range(len(temp_links)):
        game_links.append(bgg + temp_links[i])

# get list of all mechanics
mech_page = 'https://boardgamegeek.com/browse/boardgamemechanic'
driver.get(mech_page)
mechanics_parent = driver.find_elements_by_xpath\
    ('//*[@id="maincontent"]/table/tbody')
all_mechs = []
for element in mechanics_parent:
    temp = element.find_elements_by_xpath\
        ('.//a')
    for a in temp:
        all_mechs.append(a.text)

# columns of data being collected
cols = ["title",
         "year",
         "min_players",
         "max_players",
         "avg_time",
         "geek_age",
         "community_age",
         "avg_rating",
         "num_ratings",
         "complexity",
         "comments",
         "fans",
         "views",
         "mechanics",
        "categories"]

# write to file in loop
out_file = open(file_name + '.csv', 'w', encoding='utf-8')
writer = csv.writer(out_file)
writer.writerow(cols)

game_info = []

# for each link in game_links:
for i in range(5):

    #pages with all the info I want
    stats = game_links[i] + "/stats"
    credits = game_links[i] + "/credits"

    #get list info from stats
    time.sleep(1)
    driver.get(stats)

    # TODO: check for expansion and skip if it is
    # check_expansion = driver.find_element_by_xpath\
    #     ('//div[@class="game-header-subtype ng-scope"]')
    # if check_expansion != []:
    #     check_text = str(check_expansion.text)
    #     if "EXPANSION" not in check_text:

    #gather elements from /stats page
    title = driver.find_elements_by_xpath\
        ('//div[@class="game-header-title-info"]/h1/a')
    year = driver.find_elements_by_xpath\
        ('//div[@class="game-header-title-info"]/h1/span')
    min_players = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[1]/div/span/span[1]')
    max_players = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[1]/div/span/span[2]')
    avg_time = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[2]/div/span/span/span[1]')
    max_time = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[2]/div/span/span/span[2]')
    geek_age = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[3]/div[1]/span')
    community_age = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[3]/div[2]/span/button/span')
    avg_rating = float(driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[1]/div[2]/a')[0].text)
    num_ratings = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[2]/div[2]/a')[0].text
    complexity = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[4]/div[2]/a/span')
    comments = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[5]/div[2]/a')[0].text
    fans = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[6]/div[2]/a')[0].text
    views = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[7]/div[2]')[0].text

    #check for valid entires and clean data
    if title != []:
        title = title[0].text
    if year != []:
        year = int(year[0].text[1:-1])
    else:
        year = None
    if min_players != []:
        min_players = int(min_players[0].text)
    else:
        min_players = None
    if max_players != []:
        max_players = int(max_players[0].text[1:])
    else:
        max_players = None
    if avg_time != []:
        avg_time = int(avg_time[0].text)
    else:
        avg_time = None
    if max_time != []:
        max_time = int(max_time[0].text[1:])
        avg_time = int((avg_time + max_time) // 2)
    if geek_age != []:
        try:
            geek_age = int(geek_age[0].text[:-1])
        except:
            geek_age = None
    else:
        geek_age = None
    if community_age != []:
        community_age = community_age[0].text
        if community_age != "(no votes)":
            community_age = community_age[:-1]
        else:
            community_age = None
    try:
        complexity = float(complexity[0].text)
    except:
        complexity = None


    #get rid of commas in numbers
    num_ratings = int(num_ratings.replace(',', ''))
    comments = int(comments.replace(',', ''))
    fans = int(fans.replace(',', ''))
    views = int(views.replace(',', ''))

    # get stuff from Credits page
    driver.get(credits)

    # get mechanics element, iterate through entries for lsit
    mechanics_parent = driver.find_elements_by_xpath\
        ('//*[@id="mainbody"]/div/div[1]/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/credits-module/ul/li[8]/div[2]/div')
    mechanics = []
    for element in mechanics_parent:
        temp = element.find_elements_by_xpath\
            ('.//a')
        for a in temp:
            mechanics.append(a.text)

    # same for categories
    category_parent = driver.find_elements_by_xpath\
        ('//*[@id="mainbody"]/div/div[1]/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div/div/div[2]/credits-module/ul/li[7]/div[2]/div')
    categories = []
    for element in category_parent:
        temp = element.find_elements_by_xpath\
            ('.//a')
        for a in temp:
            categories.append(a.text)

    new_row = ((title,
                 year,
                 min_players,
                 max_players,
                 avg_time,
                 geek_age,
                 community_age,
                 avg_rating,
                 num_ratings,
                 complexity,
                 comments,
                 fans,
                 views,
                 mechanics,
                 categories))

    # list for data frame, write row to file
    game_info.append(new_row)
    writer.writerow(new_row)

df = pd.DataFrame(game_info, columns= cols)

print(df.head())
df.to_csv('extra_data.csv')

print("~~~~~~~~~~~~Scraping complete!~~~~~~~~~~~~")
driver.close()
out_file.close()

