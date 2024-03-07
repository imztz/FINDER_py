import networkx as nx
import graph
import disjoint_set
import graph_utils
import decrease_strategy

class Utils:
    def __init__(self):
        self.max_wcc_sz_list = []

    def re_insert(self, g_graph, solution, all_vex, decrease_strategy_id, reinsert_each_step):
        if decrease_strategy_id == 1:
            d_decrease_strategy = decrease_strategy.decrease_component_count()
        elif decrease_strategy_id == 2:
            d_decrease_strategy = decrease_strategy.decrease_component_rank()
        elif decrease_strategy_id == 3:
            d_decrease_strategy = decrease_strategy.decrease_component_multiple()
        else:
            d_decrease_strategy = decrease_strategy.decrease_component_rank()

        return self.re_insert_inner(solution, g_graph, all_vex, d_decrease_strategy, reinsert_each_step)

    def re_insert_inner(self, before_output, g_graph, all_vex, d_decrease_strategy, reinsert_each_step):
        current_adj_list_graph = []
        backup_completed_adj_list_graph = g_graph.adj_list
        current_all_vex = [False] * g_graph.num_nodes
        for v in all_vex:
            current_all_vex[v] = True

        left_output = set(before_output)
        final_output = []

        d_disjoint_set = disjoint_set.Disjoint_Set(g_graph.num_nodes)

        while left_output:
            batch_list = []

            for each_node in left_output:
                decrease_value = d_decrease_strategy.decrease_component_num_if_add_node(current_adj_list_graph, current_all_vex, d_disjoint_set, each_node)
                batch_list.append((decrease_value, each_node))

            if reinsert_each_step >= len(batch_list):
                reinsert_each_step = len(batch_list)
            else:
                batch_list.sort(key=lambda x: x[0])
                batch_list = batch_list[:reinsert_each_step]

            for _, each_node in batch_list:
                final_output.append(each_node)
                left_output.remove(each_node)
                graph_utils.Graph_Util.recover_add_node(backup_completed_adj_list_graph, current_all_vex, current_adj_list_graph, each_node, d_disjoint_set)

        final_output.reverse()
        return final_output

    def get_robustness(self, g_graph, solution):
        self.max_wcc_sz_list.clear()
        current_adj_list_graph = []
        backup_completed_adj_list_graph = g_graph.adj_list
        d_disjoint_set = disjoint_set.Disjoint_Set(g_graph.num_nodes)
        total_max_num = 0.0
        current_all_vex = [False] * g_graph.num_nodes
        for node in reversed(solution):
            graph_utils.Graph_Util.recover_add_node(backup_completed_adj_list_graph, current_all_vex,
                                                    current_adj_list_graph, node, d_disjoint_set)
            total_max_num += float(d_disjoint_set.max_rank)
            self.max_wcc_sz_list.append(float(d_disjoint_set.max_rank) / float(g_graph.num_nodes))
        total_max_num -= d_disjoint_set.max_rank
        self.max_wcc_sz_list.reverse()

        return total_max_num / float(len(g_graph.num_nodes) ** 2)

    def get_mx_wcc_sz(self, g_graph):
        assert graph is not None
        d_disjoint_set = disjoint_set.Disjoint_Set(g_graph.num_nodes)
        for i in range(len(g_graph.adj_list)):
            for j in range(len(g_graph.adj_list[i])):
                d_disjoint_set.merge(i, g_graph.adj_list[i][j])

        return d_disjoint_set.max_rank

    def betweenness(self, g_graph):
        G = self.nx_graph(g_graph)
        centrality = nx.betweenness_centrality(G, normalized=True)
        return centrality

    def nx_graph(self, g_graph):
        G = nx.Graph()
        n = len(g_graph.adj_list)
        for i in range(n):
            for j in range(n):
                if g_graph.adj_list[i][j] == 1:
                    G.add_edge(i, j)
        return G
