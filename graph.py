import numpy as np
import networkx as nx
import random


class Graph:
    def __init__(self, num_nodes=0, num_edges=0, edges_from=None, edges_to=None):
        self.num_nodes = num_nodes
        self.num_edges = num_edges
        self.edge_list = []
        self.adj_list = [[] for _ in range(num_nodes)]
        if edges_from is not None and edges_to is not None:
            for x, y in zip(edges_from, edges_to):
                self.adj_list[x].append(y)
                self.adj_list[y].append(x)
                self.edge_list.append((x, y))


    def get_two_rank_neighbors_ratio(self, covered):
        covered_set = set(covered)
        sum = 0.0
        for i in range(self.num_nodes):
            if i not in covered_set:
                for j in range(i + 1, self.num_nodes):
                    if j not in covered_set:
                        intersection = set(self.adj_list[i]) & set(self.adj_list[j])
                        if intersection:
                            sum += 1.0
        return sum

class GSet:
    def __init__(self):
        self.graph_pool = {}

    def clear(self):
        self.graph_pool.clear()

    def insert_graph(self, gid, graph):
        assert gid not in self.graph_pool
        self.graph_pool[gid] = graph

    def get(self, gid):
        assert gid in self.graph_pool
        return self.graph_pool[gid]

    def sample(self):
        assert len(self.graph_pool) > 0
        gid = random.choice(list(self.graph_pool))
