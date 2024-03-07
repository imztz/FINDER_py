import networkx as nx
import numpy as np
import random
from graph import Graph

class MvcEnv:
    def __init__(self, norm=1.0):
        self.norm = norm
        self.graph = Graph()
        self.num_covered_edges = 0
        self.cc_num = 1.0
        self.state_seq = []
        self.act_seq = []
        self.action_list = []
        self.reward_seq = []
        self.sum_rewards = []
        self.covered_set = set()
        self.avail_list = []

    def s0(self, g):
        self.graph = g
        self.covered_set.clear()
        self.action_list.clear()
        self.num_covered_edges = 0
        self.cc_num = 1.0
        self.state_seq.clear()
        self.act_seq.clear()
        self.reward_seq.clear()
        self.sum_rewards.clear()

    def step(self, a):
        assert self.graph is not None
        assert a not in self.covered_set
        self.state_seq.append(list(self.action_list))
        self.act_seq.append(a)
        self.covered_set.add(a)
        self.action_list.append(a)

        for neigh in self.graph.adj_list[a]:
            if neigh not in self.covered_set:
                self.num_covered_edges += 1

        r_t = self.get_reward()
        self.reward_seq.append(r_t)
        self.sum_rewards.append(r_t)

        return r_t

    def step_without_reward(self, a):
        assert self.graph is not None
        assert a not in self.covered_set
        self.covered_set.add(a)
        self.action_list.append(a)

        for neigh in self.graph.adj_list[a]:
            if neigh not in self.covered_set:
                self.num_covered_edges += 1

    def random_action(self):
        assert self.graph is not None
        self.avail_list = [i for i in range(self.graph.num_nodes()) if i not in self.covered_set and any(
            neigh not in self.covered_set for neigh in self.graph.adj_list(i))]
        assert len(self.avail_list) > 0
        return random.choice(self.avail_list)

    def between_action(self):
        assert self.graph is not None
        G = self.nx_graph(self.graph)
        subgraph = G.subgraph([node for node in G.nodes if node not in self.covered_set])
        BC = self.betweenness(self.graph)
        max_bc_node = max(BC, key=BC.get)
        return max_bc_node

    def is_terminal(self):
        assert self.graph is not None
        return self.num_covered_edges == self.graph.num_edges()

    def get_reward(self):
        return -self.get_max_connected_nodes_num() / (self.graph.num_nodes ** 2)

    def print_graph(self):
        print("edge_list:")
        print([edge for edge in self.nx_graph(self.graph).edges()])
        print("\ncovered_set:")
        print(list(self.covered_set))

    def get_num_of_connected_components(self):
        num_connected_components = nx.number_connected_components(self.nx_graph(self.graph))
        return float(num_connected_components)

    def get_max_connected_nodes_num(self):
        largest_cc_size = len(max(nx.connected_components(self.nx_graph(self.graph)), key=len))
        return float(largest_cc_size)

    def betweenness(self, graph):
        G = self.nx_graph(graph)
        centrality = nx.betweenness_centrality(G, normalized=True)
        return centrality

    def nx_graph(self, graph):
        G = nx.Graph()
        n = len(graph.adj_list)
        for i in range(n):
            for j in range(n):
                if graph.adj_list[i][j] == 1:
                    G.add_edge(i, j)
        return G
