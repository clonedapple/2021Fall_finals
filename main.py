import pandas as pd
import numpy as np
import json
import seaborn as sns
from itertools import combinations
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

pd.options.mode.chained_assignment = None

###############Hypothesis 1###################

def read_movies_data_files(): # called
    df_1 = pd.read_csv('data//IMDBdata_MainData.csv')
    df_2 = pd.read_csv('data//IMDBdata_MainData2.csv')
    data = pd.concat([df_1, df_2]).drop_duplicates(subset=['Title']).reset_index(drop=True)

    with open('data//kinds_in_mind_data.json', 'r') as f:
        kim = json.load(f)

    kim_data = pd.DataFrame(kim.items(), columns=['Title', 'Rating'])

    return data, kim_data

def movies_processing(mpa_data, kim_data): #called
    temp_join = pd.merge(mpa_data, kim_data, on='Title')
    temp_join = temp_join[['Title', 'Rated', 'Released', 'Genre', 'Plot', 'Rating']]

    # extracting Year
    temp_join['Year'] = temp_join['Released'].str.split(' ', expand=True)[2]

    temp_join = temp_join.dropna()
    temp_join[['Sex', 'Violence', 'Language']] = temp_join['Rating'].str.split('.', expand=True)

    # calculating Aggregate score
    temp_join['agg_score'] = temp_join['Sex'].astype(int) + temp_join['Violence'].astype(int) + temp_join[
        'Language'].astype(int)

    # Making values uniform
    temp_join['Rated'] = temp_join['Rated'].replace('TV-14', 'PG-13')
    temp_join['Rated'] = temp_join['Rated'].replace('TV-MA', 'R')
    temp_join['Rated'] = temp_join['Rated'].replace('TV-PG', 'PG')
    temp_join['Rated'] = temp_join['Rated'].replace('NC-17', 'R')
    temp_join['Rated'] = temp_join['Rated'].replace('TV-G', 'G')
    temp_join['Rated'] = temp_join['Rated'].replace('TV-Y', 'G')

    # removing values which are not rated
    temp_join = temp_join[temp_join.Rated != 'UNRATED']
    temp_join = temp_join[temp_join.Rated != 'APPROVED']
    temp_join = temp_join[temp_join.Rated != 'NOT RATED']

    # Ignoring all values before 1992
    post92 = temp_join[temp_join['Year'].astype(int) > 1991]

    return post92

def calculate_unweighted_score(data): #called
    percentages = data.groupby('Year')['Rated'].apply(lambda x: x.value_counts(normalize=True)).unstack()
    percentages['unw_kim_score'] = data.groupby('Year')['agg_score'].mean()

    return percentages


def calculate_weighted_score(row, col_num, mean_percentage, normalize_dict): #called
    year = row[6]
    rated = row[1]
    weight = mean_percentage[rated] / normalize_dict[rated][year]
    return row[col_num] * weight


def calculate_score_correlation(data):
    correlations = {}
    cols_corr = ['weighted_sex_score', 'weighted_violence_score', 'weighted_language_score']
    comb = combinations(cols_corr, 2)
    for i in comb:
        corr, pval = pearsonr(data[i[0]], data[i[1]])
        correlations[i] = {'correlation': corr, 'p-value': pval}

    return correlations

###############Hypothesis 2###################

def read_music_data_files():
    music_df = pd.read_csv('data//tcc_ceds_music.csv')
    charts_df = pd.read_csv('data//charts.csv')

    # import profanity words
    profanity_list = []
    with open('data//bad_words.txt', 'r') as fp:
        for row in fp:
            profanity_list.append(row.replace('\n', ''))

    return music_df, charts_df, profanity_list


def music_processing(charts_df,music_df):
    charts_df['song'] = charts_df['song'].str.lower()
    charts_df = charts_df.drop_duplicates(subset=['song', 'artist'])
    charts_df['artist'] = charts_df['artist'].str.lower()

    merged_music = music_df.merge(charts_df, left_on=['track_name', 'artist_name'], right_on=['song', 'artist'],
                                  how='inner')
    post59 = merged_music[merged_music['release_date'] >= 1959][
        ['artist_name', 'track_name', 'release_date', 'genre', 'lyrics', 'violence', 'obscene', 'topic', 'rank']]

    # low numbers for hip-hop. replacing with pop
    post59['genre'].replace('hip hop', 'pop', inplace=True)

    return post59

def calculate_prof_percent(row, profanity_list):
    lyrics = row[4].split(' ')
    total_length = len(lyrics)
    counter = 0
    for word in lyrics:
        if word in profanity_list:
            counter += 1
    return (counter / total_length) * 100


def plot_genres(data, popularity):
    sns.set(rc={'figure.figsize': (11.7, 8.27)})
    sns.set_theme(style="whitegrid")
    #     plt.style.use("bmh")

    plt.style.use("seaborn-dark")

    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#2F3235'  # bluish dark grey

    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey

    plt.rcParams['axes.linewidth'] = 2
    #     ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter

    genres = list(data['genre'].unique())
    for genre in genres:
        temp = data[data['genre'] == genre]

        def popularity_lookup(row):
            year = row[0]
            pop_value = popularity[row[1]][year] * 100

            return pop_value

        temp['percent_share'] = temp.apply(lambda x: popularity_lookup(x), axis=1)
        temp = temp.drop('genre', 1)

        # normalizing data due to difference in scale
        cols_to_normalize = ['percent_share', 'percent_prof']
        temp[cols_to_normalize] = temp[cols_to_normalize].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

        corr = pearsonr(temp['percent_prof'], temp['percent_share'])
        title_text = f"Genre: {genre.capitalize()}, Correlation value: {corr[0]:.4f}, P-Value: {corr[1]:.4f}"

        sns.lmplot(data=pd.melt(temp, ['release_date']), x='release_date', y='value', hue='variable', height=10,
                   palette=['#08F7FE', '#FE53BB'], aspect=1.2, scatter_kws={"s": 20}, line_kws={"linewidth": 4}).set(
            title=title_text)



