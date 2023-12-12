import data
import requests as req
import json
import re
import ast
import pandas as pd
from bs4 import BeautifulSoup
import time
import numpy as np

class Graph:
    def __init__(self):
        self.artists = {}
        self.articles = {}
        self.influence_graph = {}

    def save_artists(self, file_name='artists.json'):
        cache = {}
        for key in self.artists.keys():
            cache[key] = self.artists[key].attributes
        with open(file_name, 'w') as f:
            json.dump(cache, f)

    def read_artists(self, file_name='artists.json'):
        with open(file_name, 'r') as f:
            cache = json.load(f)
        result = {}
        for key in cache.keys():
            result[key] = data.Artist(json=cache[key])
        self.artists = result

    def save_articles(self, file_name='article_search_result.json'):
        cache = {}
        for key in self.articles.keys():
            newkey = str(list(key))
            cache[newkey] = self.articles[key]
        with open(file_name, 'w') as f:
            json.dump(cache, f)

    def read_articles(self, file_name='article_search_result.json'):
        with open(file_name, 'r') as f:
            cache = json.load(f)
        result = {}
        for key in cache.keys():
            newkey = frozenset(ast.literal_eval(key))
            result[newkey] = cache[key]
        self.articles = result

    def save_influence_graph(self, file_name='influence.json'):
        with open(file_name, 'w') as f:
            json.dump(self.influence_graph, f)
    
    def read_influence_graph(self, file_name='influence.json'):
        with open(file_name, 'r') as f:
            self.influence_graph = json.load(f)
        return self.influence_graph

    def get_artists(self, board, cache=True, save=False):
        if cache:
            self.read_artists()
        else:
            artists = {}
            search = data.itunes_searcher()
            i = 0
            for song_info in board.billboard:
                if i >= 10:
                    time.sleep(40)
                    i = 0
                represent_author = song_info[2][0]
                print(represent_author, song_info[1])
                res = search.get_res_json(song_info[1], represent_author)
                try:
                    song_temp = data.Song(title=song_info[1], author=represent_author ,json=res)
                except:
                    print(res)
                    break
                print(song_temp.attributes['release_date'])
                song_temp.get_rank(song_info[0], song_info[4], song_info[5])
                song_temp.get_score()
                i += 1
                for author_name in song_info[2]:
                    if author_name not in artists:
                        new_artist = data.Artist(author_name)
                        artists[author_name] = new_artist
                    artists[author_name].add_song(song_temp)
            self.artists = artists
            if save:
                self.save_artists()
    
    def get_articles(self, cache=True, save=False, headers=None):
        if cache:
            self.read_articles()
        else:
            article_search_result = {}
            for artist1 in self.artists.keys():
                for artist2 in self.artists.keys():
                    if artist1 != artist2 and frozenset([artist1, artist2]) not in article_search_result.keys():
                        search_query = f'{artist1} AND {artist2}'
                        api_url = 'https://en.wikipedia.org/w/api.php'
                        params = {
                            'action': 'query',
                            'list': 'search',
                            'format': 'json',
                            'srsearch': search_query,
                            'srlimit': 10,
                        }
                        if not headers:
                            headers = {
                                'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzOTc2Yzc2ZGI0ODMwODMwMzA0NDM4ZWU5ZWZmMWUyZCIsImp0aSI6IjcwN2ZmNDZjYjAyZWJlN2E0NjE2ODAzMTMyNDhjZjdmZjA0YWNmNzAyMDc4MWQxMmQ5ZGM2ZWNiOTc0MzZlNDM0ZjMzYWE1Yzc1Y2FkZDZmIiwiaWF0IjoxNzAxNjk1NDgxLjAyNzU2OSwibmJmIjoxNzAxNjk1NDgxLjAyNzU3MiwiZXhwIjozMzI1ODYwNDI4MS4wMjUzOSwic3ViIjoiNzQ0MzQ5MzYiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIl19.KfA44HXKVDH5SVN_Lh_4yPYaFmW71qkvTQspIH7t191V3-LXCxOt_f4HlQY_KjT-ENAGzn6G3XbQIa0xGStVKocYjOaap3j6_sw0D29mCS25Mt12Q1yo1uMFtESLGpIBy1aZIbnmnjghAqGFs3UdnB9OewYTe9bovzdLxo7rHiovmxSxbPt5AVuQMiEJUPY5ifIJD4wmfj0vtpb2UB1wEg74DVGiUPYHuR6W2hE-nsjFxsZcgopUWf3T992rHN8gOmDOA12x6IFRERTsz7VWstQJ8AsfVYcc6glBiX2AC4ux7v96bE8Phk_AXMna1UjVw992wT2fSOglezcU01_VofEEV913EXuoN77LDEdbx5v-RjvuneOd-5CUTdYsh3ulrYyqqcoE9zF1Uf1m1BGVeOb04ARIK0iuHvDn-Iz2mb5MfHklxRhFxBXl3B0IyQDNFYjI6AyJ5LWs4OHiN9bwLGEMK9UrB78JUDvidzRdO230UpdYVNWxOfmASaLbIiuRcEBR33ytwCPQSRK2ztrhRA6KdNn_RJcZ2JaG9yoxodkHuNJjXVlUZuoUeBSQi-CXIjPKo1GHD9P8wgD1kzF3pAlHQR49uiaoDQ8aqiZ2C8YJr3yJmgZjWttvRWyZy9AIizELChketvtVZAkLDK9d3Yh_QIQZp9vOXIAghgyjcfQ',
                                'User-Agent':'SI507_final_project'
                            }
                        response = req.get(api_url, params=params, headers=headers)
                        data = response.json()
                        search_results = data['query']['search']
                        key = frozenset([artist1, artist2])
                        print([item['title'] for item in search_results])
                        article_search_result[key] = [item['title'] for item in search_results]
            self.articles = article_search_result
            if save:
                self.save_articles()

    def get_view(self, article_name, timestamp):
        time_start = timestamp - 1000000
        time_end = timestamp
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        try:
            response = req.get(f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article_name}/monthly/{time_start}/{time_end}', headers=headers).json()
            view = np.mean([item['views'] for item in response['items']])
        except:
            view = None
        return view
    
    def get_influence(self, artist1, artist2):
        attribute1 = artist1.attributes
        attribute2 = artist2.attributes
        result_titles = self.articles[frozenset({attribute1['name'], attribute2['name']})]
        influence_of_songs = []
        for song in attribute2['songs']:
            views_of_articles = []
            for result in result_titles:
                pageview_response = self.get_view(result, timestamp=song['release_date'])
                if pageview_response:
                    views_of_articles.append(pageview_response)
            views_of_articles = [item for item in views_of_articles if item]
            if len(views_of_articles)!=0:
                influence_of_songs.append(np.mean(views_of_articles)*song['score'])
        try:
            songs_influence_sum = np.sum(influence_of_songs)
        except:
            print("exception in wikipedia search happens. The date exceed the limit of wikipedia api.")
            return float('inf')
        if songs_influence_sum == 0:
            return float('inf')
        else:
            return (10000/songs_influence_sum)
        
    def get_influence_graph(self, cache=True, save=False, resume=False):
        if cache:
            self.read_influence_graph()
        else:
            if resume:
                influence = self.read_influence_graph()
                for artist in self.artists.keys():
                    if artist not in influence.keys():
                        influence[artist] = {}
            else:
                influence = {}
                for artist in self.artists.keys():
                    influence[artist] = {}
            i = 0
            for artist1 in self.artists.keys():
                for artist2 in self.artists.keys():
                    if artist1 != artist2 and ((artist2 not in influence[artist1].keys()) or influence[artist1][artist2]==float('inf')):
                        try:
                            influence[artist1][artist2] = self.get_influence(self.artists[artist1], self.artists[artist2])
                        except:
                            print(f'network error occurred when searching {artist1}, {artist2}')
                            if save:
                                self.save_influence_graph()
                            return influence
                        i += 1
                        if i >= 100:
                            if save:
                                self.save_influence_graph()
                                print('cache automatically saved')
                            i = 0
                        print(artist1, artist2, influence[artist1][artist2])
            self.influence_graph = influence
            if save:
                self.save_influence_graph()
        return True

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.influence_graph}
        distances[start] = 0
        previous_nodes = {node: None for node in self.influence_graph}
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_node = min(priority_queue, key=lambda x: x[0])
            priority_queue.remove((current_distance, current_node))
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.influence_graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    priority_queue.append((distance, neighbor))
        path = []
        current = end
        while current is not None:
            path = [current] + path
            current = previous_nodes[current]
        return distances[end], path