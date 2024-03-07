class Disjoint_Set:
    def __init__(self, graph_size):
        self.parent = list(range(graph_size))
        self.rank = [1] * graph_size
        self.max_rank = 1

    def find_root(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find_root(self.parent[node])
        return self.parent[node]

    def merge(self, node1, node2):
        root1 = self.find_root(node1)
        root2 = self.find_root(node2)

        if root1 != root2:
            if self.rank[root2] > self.rank[root1]:
                self.parent[root1] = root2
                self.rank[root2] += self.rank[root1]
                self.max_rank = max(self.max_rank, self.rank[root2])
            else:
                self.parent[root2] = root1
                self.rank[root1] += self.rank[root2]
                self.max_rank = max(self.max_rank, self.rank[root1])

    def get_biggest_component_current_ratio(self):
        return self.max_rank / float(len(self.rank))

    def get_rank(self, node):
        return self.rank[node]
