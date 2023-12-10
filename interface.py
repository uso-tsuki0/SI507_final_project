import data
import graph
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns

class Interface:
    def __init__(self) -> None:
        self.board = data.billboard()
        self.graph = graph.Graph()
        
    def get_content(self, cache=True, save=False):
        self.board.get_billboard(cache=cache, save=save)
        self.graph.get_artists(self.board, cache=cache, save=save)
        self.graph.get_articles(cache=cache, save=save)
        self.graph.get_influence_graph(cache=cache)

    def simplify_name(self,str):
        first_last = str.split(' ')
        simplified = ''
        if len(first_last) == 1:
            return first_last[0][:3]
        elif len(first_last) == 2:
            for name in first_last:
                simplified += name[:2]
            return simplified
        else:
            for name in first_last:
                simplified += name[0]
            return simplified

    def dist_to_influence(self, simplify=True):
        inversed_graph = {}
        if simplify:
            for key1 in self.graph.influence_graph.keys():
                inversed_graph[self.simplify_name(key1)] = {}
                for key2 in self.graph.influence_graph[key1].keys():
                    inversed_graph[self.simplify_name(key1)][self.simplify_name(key2)] = 1/self.graph.influence_graph[key1][key2]
            return inversed_graph
        else:
            for key1 in self.graph.influence_graph.keys():
                inversed_graph[key1] = {}
                for key2 in self.graph.influence_graph[key1].keys():
                    inversed_graph[key1][key2] = 1/self.graph.influence_graph[key1][key2]
            return inversed_graph

    def visualize(self):
        plt.figure(figsize=(10, 10))
        influence_graph = self.dist_to_influence()
        G = nx.DiGraph()
        for node, neighbors in influence_graph.items():
            for neighbor, weight in neighbors.items():
                if weight >= 4:
                    G.add_edge(node, neighbor, weight=weight)
        node_degrees = dict(G.degree())
        node_colors = [node_degrees[node] for node in G.nodes()]
        min_weight = min(weight['weight'] for _, _, weight in G.edges(data=True))
        max_weight = max(weight['weight'] for _, _, weight in G.edges(data=True))
        normalized_weights = [0+15*(weight['weight'] - min_weight) / (max_weight - min_weight) for _, _, weight in G.edges(data=True)]
        edge_colors = plt.cm.plasma(normalized_weights)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors,
                font_size=8, width=0.3, edge_color=edge_colors, alpha=0.5)
        plt.show()

    def influence_df(self, simplify=False):
        return pd.DataFrame(self.dist_to_influence(simplify))
    
    def active_rank(self):
        df = self.influence_df()
        influencial = df.sum(axis=0)
        influenced = df.sum(axis=1)
        active_df = (influencial+influenced).sort_values(ascending=False).reset_index().rename(columns={'index': 'Artist', 0: 'score'})
        return active_df

    def query_artist(self, artist_name):
        if artist_name not in self.graph.artists:
            print(f'No such artist {artist_name} in our database')
            return None
        df = self.influence_df()
        print(f'Works in billboard')
        board_df = self.board.to_df()
        artist_df = board_df[board_df['Artist'] == artist_name]
        print(artist_df)
        print(f'rank by score:')
        score_df = self.board.get_score_rank()
        print(score_df[score_df['Artist'] == artist_name])
        print(f'rank by number of songs:')
        num_df = self.board.get_num_rank()
        print(num_df[num_df['Artist'] == artist_name])
        print(f'rank by influence activity:')
        active_df = self.active_rank()
        print(active_df[active_df['Artist'] == artist_name])
        print('influence:')
        print(self.dist_to_influence(False)[artist_name])

    def query_billboard(self):
        df = pd.DataFrame(self.board.billboard, columns=['Rank', 'Title', 'Artist', 'Last_Week', 'Peak_Pos', 'Weeks_on_Chart']).set_index('Rank')
        print(df)

    def query_rank_score(self):
        df = self.board.get_score_rank()
        print(df)

    def query_rank_num(self):
        df = self.board.get_num_rank()
        print(df)

    def query_rank_active(self):
        df = self.active_rank()
        print(df)

    def query_shortest_path(self, start, end):
        if start not in self.graph.artists or end not in self.graph.artists:
            print(f'No such artist {start} or {end} in our database')
            return None
        distance, path = self.graph.dijkstra(start, end)
        print(f'The shortest path from {start} to {end} is {path} with distance {distance}')

    def query_graph(self):
        self.visualize()


if __name__ == '__main__':
    interface = Interface()
    interface.get_content(cache=True, save=False)
    interface.query_artist('Drake')