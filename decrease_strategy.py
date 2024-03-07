import disjoint_set

class Decrease_Component_Strategy:
    def decrease_component_num_if_add_node(self, backup_completed_adj_list_graph, current_all_vex, union_set, node):
        pass


class decrease_component_rank(Decrease_Component_Strategy):
    def decrease_component_num_if_add_node(self, backup_completed_adj_list_graph, current_all_vex, union_set, node):
        component_set = set()
        for neighbour_node in backup_completed_adj_list_graph[node]:
            if current_all_vex[neighbour_node]:
                component_set.add(union_set.find_root(neighbour_node))
        sum_rank = 1 + sum(union_set.get_rank(each_node) for each_node in component_set)
        return sum_rank

class decrease_component_count(Decrease_Component_Strategy):
    def decrease_component_num_if_add_node(self, backup_completed_adj_list_graph, current_all_vex, union_set, node):
        component_set = set(union_set.find_root(neighbour_node) for neighbour_node in backup_completed_adj_list_graph[node] if current_all_vex[neighbour_node])
        return len(component_set)

class decrease_component_multiple(Decrease_Component_Strategy):
    def decrease_component_num_if_add_node(self, backup_completed_adj_list_graph, current_all_vex, union_set, node):
        component_set = set()
        for neighbour_node in backup_completed_adj_list_graph[node]:
            if current_all_vex[neighbour_node]:
                component_set.add(union_set.find_root(neighbour_node))
        sum_rank = 1 + sum(union_set.get_rank(each_node) for each_node in component_set)
        sum_rank *= len(component_set)
        return sum_rank
