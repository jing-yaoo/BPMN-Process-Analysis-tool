from src.xmlParser import tree
import collections
from copy import deepcopy

#TODO implement logic for inclusive and exlusive gateways
#  if gateway.getAttribute('name').contains("exclusive"):
# elif gateway.getAttribute('name').contains("inclusive"):


graph = tree


def get_edge_set(start_node, graph):
    result = set()
    def dfs(cur):
        if not cur:
            return 

        for child in graph[cur]:
            result.add((cur, child))
            dfs(child)
    
    dfs(start_node)
    return result 
    
def get_all_nodes_between_inclusive_gtws(inc_gtw_1, inc_gtw_2, graph):
    result = set()
    def dfs(cur):
        if not cur:
            return False 

        if cur == inc_gtw_2:
            return True
        
        res = False 

        for child in graph[cur]:
            if dfs(child):
                result.add(cur)
                res = True
        return res
    dfs(inc_gtw_1)
    result.remove(inc_gtw_1)
    return list(result)

def find_next_inclusive_gtws(inc_gtw_1, graph):
    result = set()

    def dfs(cur):
        if not cur:
            return 
        
        if cur.startswith("inclusiveGateway") and cur != inc_gtw_1:
            result.add(cur)
            return

        for child in graph[cur]:
            dfs(child)
        
    dfs(inc_gtw_1)

    return list(result)


def get_start_node(graph):
    counts = collections.defaultdict(int)

    for key in graph:
        counts[key] = 0

    for children in graph.values():
        for child in children:
            counts[child] += 1
    
    return min(counts, key = lambda x : counts[x])

def gen_new_links(graph):
    start_node = get_start_node(graph)
    edge_set = get_edge_set(start_node, graph)
    graph_copy = deepcopy(graph)

    def dfs(cur):
        if not cur:
            return 

        if cur.startswith("inclusiveGateway"):
            start_gtw = cur
            end_gtws = find_next_inclusive_gtws(cur, graph)
            
            for end_gtw in end_gtws:
                nodes_between = get_all_nodes_between_inclusive_gtws(start_gtw, end_gtw, graph)

                for node in nodes_between:
                    for other_node in set(nodes_between) - set(node):
                        if (node, other_node) not in edge_set and (other_node, node) not in edge_set:
                            print(node, other_node)
                            graph_copy[node].append(other_node)

        for child in graph[cur]:
            dfs(child)

    dfs(start_node)
    return graph_copy

print(gen_new_links(graph))


def add_inclusive_paths(adj_list):
    # Identify the inclusive gateways
    inclusive_gateways = [node for node in adj_list if 'inclusive' in node]
    
    # Create a new adjacency list to store the modified paths
    new_adj_list = {key: value[:] for key, value in adj_list.items()}

    for i in range(len(inclusive_gateways) - 1):
        start_gateway = inclusive_gateways[i]
        end_gateway = inclusive_gateways[i + 1]

        # Get all nodes between the start_gateway and end_gateway
        between_nodes = []
        queue = adj_list[start_gateway][:]
        visited = set(queue)
        while queue:
            node = queue.pop(0)
            if node == end_gateway:
                continue
            if 'inclusive' in node:
                continue
            between_nodes.append(node)
            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        # Add the paths to the new adjacency list
        for node in between_nodes:
            new_adj_list[node] = new_adj_list.get(node, []) + [n for n in between_nodes if n != node and n not in new_adj_list[node]]

    return new_adj_list

# Adding the new paths
new_adj_list = add_inclusive_paths(tree)

# Printing the new adjacency list
for key, value in new_adj_list.items():
    print(f"'{key}': {value}")



    

