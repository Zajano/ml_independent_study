# Author: Zack Jaffe-Notier
# Date: 6/4/2020
# Description: generates graphs from BGG data

# Import plotting and organization modules
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import chain

""" DEFINE FOR PROGRAM USE """
# csv file with BGG data - must have 'mechanics' and 'categories' columns
file_name = 'game_data.csv'
os.chdir(r"C:\Users\Zack\Desktop\work\OSU\406 - p1 - stats\final report\final files")

# True is display to screen is wanted - will allow for saving from screen
want_display = True

# True if saved file is wanted, then write the path to where they should be saved
want_file = False
graphs_loc = 'C:\\Users\\zacki\\Desktop\\OSU\\406 - p1 - stats\\testing\\'

# set to True for each graph wanted
pair_plot_graph             = False
average_ratings_vs_years    = False
game_complexity_vs_years    = False
top_mechanics_vs_complexity = False
top_mechanics_vs_years      = True
complexity_vs_gametime      = False
complexity_vs_rating        = False
mechanics_between_1990_2019 = False
min_play_age_vs_complexity  = False

""" END DEFINITIONS """

# import data, convert mechanics and categories to lists
bgg_data = pd.read_csv(file_name, encoding='latin-1', converters={'mechanics': eval, 'categories': eval})
sns.set()

# various filters
# print(bgg_data.minage.quantile(0.999)) # find where to trim limits of data ranges
bgg_games = bgg_data[bgg_data['type'] == 'boardgame']
recent_games = bgg_games[bgg_games['year'] > 1989] # 1850 - 99th percentile
recent_all = bgg_data[bgg_data['year'] > 1989]

# trimming for pair plot
trim_maxplayers = recent_all[recent_all['maxplayers'] <= 30] # 30 - 99th percentile
trim_mintime = trim_maxplayers[trim_maxplayers['minplaytime'] <= 120] # 120 - 90th percentile
trim_age = trim_mintime[trim_mintime['minage'] <= 18]
clean_bgg = trim_age[trim_age['maxplaytime'] <= 720]

# suppress warnings
pd.options.mode.chained_assignment = None  # default='warn'

def adj_mechs(frame, val):
    '''puts 'val' for all entries in col of dataframe'''
    mask = frame.mechanics.apply(lambda row: val in row)
    temp_games = frame[mask]
    temp_games['mechanics'] = val
    return temp_games

def pair_plot():
    '''Pair Plot to find interesting correlations'''
    print("preparing pair_plot...")
    # graph size and name
    sns.set(rc={'figure.figsize': (40, 40)})
    g_name = 'pair_plot'

    # trim unwanted columns
    p_plot = clean_bgg[['year','minplayers','maxplayers','minplaytime',
                        'maxplaytime','minage','users_rated','avg_rating',
                        'bay_rating','owners','traders','wanters','wishers',
                        'total_comments','total_weights','complexity']]

    g = sns.PairGrid(p_plot)
    g.map(plt.scatter)
    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print("pair_plot completed!")

def col_vs_year(col):
    '''given column by Year of release'''
    # graph size and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = col + '_vs_year'
    print("preparing " + g_name + "...")

    # copy recent games, convert years to str for graph
    bgg_years = recent_games.copy()
    bgg_years.year = bgg_years.year.astype(str)

    # plot data
    sns.lineplot(x='year', y=col, data=bgg_years)
    sns.stripplot(x='year', y=col, data=bgg_years, jitter=.3, size=3)
    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")

def top_mechs_vs_complexity():
    '''top 10 mechanics by complexity'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(8,16)})
    g_name = 'top_mechs_vs_complexity'
    print("preparing " + g_name + "...")

    # # number of each type of mechanic and category
    # mech_counts = pd.Series(list(chain.from_iterable(bgg_data.mechanics))).value_counts()
    # cat_counts = pd.Series(list(chain.from_iterable(bgg_data.categories))).value_counts()

    # # 10 most popular of each type
    # top_mechs = list(mech_counts.nlargest(n=10).index.values)
    # top_cats = list(cat_counts.nlargest(n=10).index.values)

    # get sets of top mechanics
    dice_games = adj_mechs(bgg_data, 'Dice Rolling')
    hand_games = adj_mechs(bgg_data, 'Hand Management')
    var_games = adj_mechs(bgg_data, 'Variable Player Powers')
    set_games = adj_mechs(bgg_data, 'Set Collection')
    mod_games = adj_mechs(bgg_data, 'Modular Board')
    draft_games = adj_mechs(bgg_data, 'Card Drafting')
    hex_games = adj_mechs(bgg_data, 'Hexagon Grid')
    coop_games = adj_mechs(bgg_data, 'Cooperative Game')
    tile_games = adj_mechs(bgg_data, 'Tile Placement')
    area_games = adj_mechs(bgg_data, 'Area Majority / Influence')

    # combine - keeping duplicates
    mechs_grouped = pd.concat([dice_games, hand_games, var_games, set_games, mod_games,
                               draft_games, hex_games, coop_games, tile_games, area_games],
                              ignore_index=True, sort=False)

    # filter out no votes and plot
    mech_groups_x = mechs_grouped[mechs_grouped["complexity"] > 0]
    sns.violinplot(x='complexity', y='mechanics', data=mech_groups_x, bw=0.15)
    sns.swarmplot(x='complexity', y='mechanics', data=mech_groups_x,
                  size=1.25, edgecolor='gray', linewidth=0.25)

    # rotate labels
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")
    # plt.tight_layout()

    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")

def top_mechs_vs_years():
    '''top 10 mechanics printed over the years'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = 'top_mechs_vs_years'
    print("preparing " + g_name + "...")

    # get sets of top mechanics
    dice_games = adj_mechs(recent_all, 'Dice Rolling')
    hand_games = adj_mechs(recent_all, 'Hand Management')
    var_games = adj_mechs(recent_all, 'Variable Player Powers')
    set_games = adj_mechs(recent_all, 'Set Collection')
    mod_games = adj_mechs(recent_all, 'Modular Board')
    draft_games = adj_mechs(recent_all, 'Card Drafting')
    hex_games = adj_mechs(recent_all, 'Hexagon Grid')
    coop_games = adj_mechs(recent_all, 'Cooperative Game')
    tile_games = adj_mechs(recent_all, 'Tile Placement')
    area_games = adj_mechs(recent_all, 'Area Majority / Influence')

    # plot and print
    sns.kdeplot(dice_games['year'], shade=True, bw=0.125, label='Dice Rolling')
    sns.kdeplot(hand_games['year'], shade=True, bw=0.125, label='Hand Management')
    sns.kdeplot(var_games['year'], shade=True, bw=0.125, label='Variable Powers')
    sns.kdeplot(set_games['year'], shade=True, bw=0.125, label='Set Collection')
    sns.kdeplot(mod_games['year'], shade=True, bw=0.125, label='Modular Board')
    sns.kdeplot(draft_games['year'], shade=True, bw=0.125, label='Card Drafting')
    sns.kdeplot(hex_games['year'], shade=True, bw=0.125, label='Hexagon Grid')
    sns.kdeplot(coop_games['year'], shade=True, bw=0.125, label='Cooperative Game')
    sns.kdeplot(tile_games['year'], shade=True, bw=0.125, label='Tile Placement')
    sns.kdeplot(area_games['year'], shade=True, bw=0.125, label='Area Majority')

    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")

def complexity_vs_playtime():
    '''boring and predictable results'''
    g_name = 'complexity_vs_playtime'

    # trimming extreme values from data
    b_c = bgg_data[bgg_data['complexity'] > 0]
    b_mint1 = b_c[b_c['minplaytime'] <= 120]
    b_mint2 = b_mint1[b_mint1['minplaytime'] > 0]
    c_v_p2 = b_mint2[b_mint2['maxplaytime'] <= 720]
    c_v_p = c_v_p2[c_v_p2['maxplaytime'] > 0]

    # new 'average playtime' column for graph
    c_v_p['avg_playtime'] = (c_v_p['minplaytime'] + c_v_p['maxplaytime']) / 2

    sns.regplot(x='complexity', y='avg_playtime', data=c_v_p, line_kws={"color": "grey"})
    plt.show()
    print(g_name + " completed!")

def comp_v_rating():
    '''complexity/average rating relationship'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(8,4)})
    g_name = 'complexity_vs_rating'
    print("preparing " + g_name + "...")

    # filter, plot, print
    cvr = bgg_data[bgg_data['complexity'] > 0]
    sns.regplot(x='complexity', y='avg_rating', data=cvr, line_kws={"color": "grey"})
    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")

def mechanics_years_dumbell(year1, year2):
    '''mechanics popularity changes between two years'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize': (8, 16)})
    g_name = 'mechs_' + str(year1) + '_' + str(year2) + '_db'
    print("preparing " + g_name + "...")

    first_year_data = bgg_data[bgg_data['year'] == year1]
    second_year_data = bgg_data[bgg_data['year'] == year2]

    # number of each type of mechanic and category
    year1_counts = pd.Series(list(chain.from_iterable(first_year_data.mechanics))).value_counts()
    year2_counts = pd.Series(list(chain.from_iterable(second_year_data.mechanics))).value_counts()

    sorted_counts = year1_counts.sort_values(ascending=False)

    mech_years = pd.concat([sorted_counts, year2_counts], axis=1).fillna(0)
    # mech_range = range(1, len(mech_years.index) + 1)

    # get percentages instead of totals
    sum1, sum2 = mech_years[0].sum(), mech_years[1].sum()
    mech_years[0] = mech_years[0] / sum1
    mech_years[1] = mech_years[1] / sum2

    # plot and organize data
    plt.hlines(y=mech_years.index, xmin=mech_years[0], xmax=mech_years[1], color='grey', alpha=0.4)
    plt.scatter(mech_years[0], mech_years.index, color='skyblue', alpha=1, label='1990')
    plt.scatter(mech_years[1], mech_years.index, color='green', alpha=0.4, label='2019')
    plt.legend()
    plt.ylabel('Category')
    plt.xlabel('Games Published')

    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")

def vs_heatmap(col1, col2):
    '''generates heatmap from density of 2 column relations'''

    # graph dimensions and name
    sns.set(rc={'figure.figsize':(10,10)})
    g_name = col1 + '_vs_' + col2 + '_heatmap'
    print("preparing " + g_name + "...")

    # filter and plot
    cvr = clean_bgg[clean_bgg[col1] > 0]
    cvr = cvr[cvr[col2] > 0]
    g = sns.jointplot(x=col1, y=col2, data=cvr, kind="kde", color="m")
    # g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+") # too many points
    g.ax_joint.collections[0].set_alpha(0)
    g.set_axis_labels(str(col1), str(col2))

    # save and display
    if want_file:   plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    if want_display:    plt.show()
    print(g_name + " completed!")


def main():
    if pair_plot_graph: pair_plot()
    if average_ratings_vs_years:    col_vs_year('avg_rating')
    if game_complexity_vs_years:    col_vs_year('complexity')
    if top_mechanics_vs_complexity: top_mechs_vs_complexity()
    if top_mechanics_vs_years:  top_mechs_vs_years()
    if complexity_vs_gametime:  complexity_vs_playtime()
    if complexity_vs_rating:    comp_v_rating()
    if mechanics_between_1990_2019: mechanics_years_dumbell(1990, 2019)
    if min_play_age_vs_complexity:  vs_heatmap('complexity', 'minage')
    print("~~~~~~~~~~~~Done generating graphs!~~~~~~~~~~~~")

if __name__ == "__main__": main()
