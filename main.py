import pandas as pd
import numpy as np
import json
import seaborn as sns
from itertools import combinations
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

pd.options.mode.chained_assignment = None


def read_data_files(): # called
    df_1 = pd.read_csv('data//IMDBdata_MainData.csv')
    df_2 = pd.read_csv('data//IMDBdata_MainData2.csv')
    data = pd.concat([df_1, df_2]).drop_duplicates(subset=['Title']).reset_index(drop=True)

    with open('data//kinds_in_mind_data.json', 'r') as f:
        kim = json.load(f)

    kim_data = pd.DataFrame(kim.items(), columns=['Title', 'Rating'])

    return data, kim_data

def processing(mpa_data, kim_data): #called
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



################## notebook

# mpa_data, kim_data = read_data_files()
# post92 = processing(mpa_data, kim_data)
# percentages = calculate_unweighted_percentage(post92)
#
# # Normalizing
# mean_percentage = dict(percentages.mean())
# normalize_dict = percentages.to_dict()
#
# # Normalizing agg score (col=10)
# post92['weighted_agg'] = post92.apply(calculate_weighted_score,args=[10, mean_percentage, normalize_dict], axis=1)
# percentages['weighted_kim_score'] = post92.groupby('Year')['weighted_agg'].mean()
#
# # Category wise
# cols_to_process = ['Sex','Violence','Language']
# for col in cols_to_process:
#     post92[col] = post92[col].astype('int32')
#
# post92['weighted_sex'] = post92.apply(calculate_weighted_score,args=[7, mean_percentage, normalize_dict], axis=1)
# post92['weighted_violence'] = post92.apply(calculate_weighted_score,args=[8, mean_percentage, normalize_dict], axis=1)
# post92['weighted_language'] = post92.apply(calculate_weighted_score,args=[9, mean_percentage, normalize_dict], axis=1)
#
# percentages['weighted_sex_score'] = post92.groupby('Year')['weighted_sex'].mean()
# percentages['weighted_violence_score'] = post92.groupby('Year')['weighted_violence'].mean()
# percentages['weighted_language_score'] = post92.groupby('Year')['weighted_language'].mean()


#
# # Correlation
# calculate_score_correlation(temp_viz_df)