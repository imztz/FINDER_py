from disjoint_set import Disjoint_Set

class Graph_Util:
    def __init__(self):
        pass

    def delete_node(self, adj_list_graph, node):
        for neighbour in adj_list_graph[node]:
            adj_list_graph[neighbour].remove(node)
        adj_list_graph[node].clear()

    def recover_add_node(self, backup_completed_adj_list_graph, backup_all_vex, adj_list_graph, node,union_set=Disjoint_Set(0)):
        for neighbour_node in backup_completed_adj_list_graph[node]:
            if backup_all_vex[neighbour_node]:
                self.add_edge(adj_list_graph, node, neighbour_node)
                union_set.merge(node, neighbour_node)
        backup_all_vex[node] = True

    def add_edge(self, adj_list_graph, node0, node1):
        max_index = max(node0, node1)
        while len(adj_list_graph) <= max_index:
            adj_list_graph.append([])
        adj_list_graph[node0].append(node1)
        adj_list_graph[node1].append(node0)
