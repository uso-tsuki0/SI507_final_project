import requests as req
import json
import re
import ast
import pandas as pd
from bs4 import BeautifulSoup
import time
import numpy as np

class Song:
    def __init__(self, title="No Title", author="No Author", release_date="0000000000", json=None):
        self.attributes = {
            'title': title,
            'author': author,
            'rank_curr': None,
            'rank_high': None,
            'weeks_on_chart': None,
            'score': None,
        }
        if json:
            self.attributes['release_date'] = int(json['releaseDate'][0:10].replace('-', '') + '00')
        else:
            self.attributes['release_date'] = int(release_date)

    def get_rank(self, rank_curr, rank_high, weeks_on_chart):
        self.attributes['rank_curr'] = rank_curr
        self.attributes['rank_high'] = rank_high
        self.attributes['weeks_on_chart'] = weeks_on_chart
    
    def get_score(self):
        self.attributes['score'] = 1 + 2 / (self.attributes['rank_curr'] + self.attributes['rank_high']) + 0.005 * self.attributes['weeks_on_chart']

    def read_json(self, dict):
        self.attributes = dict

class Artist:
    def __init__(self, name='None', json=None):
        if json:
            self.attributes = json
        else:
            self.attributes = {
                'name': name,
                'songs': [],
                'neighbors': {},
                'score': None,
            }

    def add_song(self, song):
        if song not in self.attributes['songs']:
            self.attributes['songs'].append(song.attributes)

class itunes_searcher:
    def __init__(self):
        self.base_url = "https://itunes.apple.com/search"
        self.params = {
            "term": '',
            "entity": 'song',
            "limit": 1,
        }
    
    def get_res_json(self, title, artist):
        self.params['term'] = f'{title} {artist}'
        response = req.get(self.base_url, params=self.params)
        return response.json()['results'][0]
    
class billboard:
    def __init__(self):
        self.billboard = []

    def read_billboard(self, filename='billboard.json'):
        with open(filename, 'r') as f:
            self.billboard = json.load(f)['billboard']

    def save_billboard(self, filename='billboard.json'):
        with open(filename, 'w') as f:
            json.dump({'billboard': self.billboard}, f)

    def to_df(self):
        df_board = pd.DataFrame(self.billboard, columns=['Rank', 'Title', 'Artist', 'Last_Week', 'Peak_Pos', 'Weeks_on_Chart'])
        df_board = df_board.explode('Artist').reset_index(drop=True)
        df_board['score'] = 1 + 2 / (df_board['Rank'] + df_board['Peak_Pos']) + 0.005 * df_board['Weeks_on_Chart']
        return df_board

    def get_billboard(self, cache=True, save=False):
        if cache:
            self.read_billboard()
        else:
            url = 'https://www.billboard.com/charts/hot-100/'
            response = req.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            songs = soup.find_all('div', class_='o-chart-results-list-row-container')
            board = []
            separators = [' Featuring ', ', ', ' & ', ' With ', ' x ', ' / ', ' Duet With ', ' X ', ' + ', ' &amp; ', ' / ']
            for song in songs:
                rank = int(song.find('span', class_="c-label").text.strip())
                info = song.find('li', class_='lrv-u-width-100p')
                title = info.find('h3').text.strip()
                artist = re.split('|'.join(map(re.escape, separators)), info.find('span').text.strip())
                history = [int(item.text.strip()) if item.text.strip().isdigit() else 0 for item in info.find_all('span', class_='c-label')[1:4]]
                board.append([rank, title, artist]+history)
            self.billboard = board
            if save:
                self.save_billboard()

    #rank artist by song num in billboard
    def get_num_rank(self):
        df_board = self.to_df()
        return df_board.groupby('Artist')[['Title']].count().sort_values('Title', ascending=False).reset_index()

    #rank artist by score in billboard
    def get_score_rank(self):
        df_board = self.to_df()
        return df_board.groupby('Artist')['score'].sum().sort_values(ascending=False).reset_index()