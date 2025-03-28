"""  this is expand version of def method
def fatch_stats(selected_user, df):
    if selected_user =='Overall':
        num_msg = df.shape[0]  #df.shape return (rowCount, colCount), df.shape[0] shows row count
        words = []
        for msg in df['message']:
            words.extend(msg.split())
        return num_msg, len(words)
    else:
        num_msg = df[df['user'] == selected_user].shape[0]  # df.shape return (rowCount, colCount), df.shape[0] shows row count
        words = []
        for msg in df['message']:
            words.extend(msg.split())
        return num_msg, len(words)
"""
from collections import Counter

import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msg = df.shape[0]  # df.shape return (rowCount, colCount), df.shape[0] shows row count

    # fetch number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    # fetch number of media
    numOfMedia = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of link
   # numofLinks = df[df['message'].str.startswith("http")].shape[0]   #this is also can use for links
    extrct = URLExtract()
    links = []
    for i in df['message']:
        links.extend(extrct.find_urls(i))
    return num_msg, len(words), numOfMedia, len(links) # numofLinks
def most_busy_user(df):
    x = df['user'].value_counts().head()
    df =  round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    return x, df

def create_wordCloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc

# most common word i skipped

    # emoji uses
def emoji_finder(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emog_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emog_df

def timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    actvt = df['day_name'].value_counts()
    return actvt

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    actvt = df['month'].value_counts()
    return actvt

def user_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heatmp = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)
    return heatmp