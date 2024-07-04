from xmlParser import tree, endElementName
from copy import deepcopy

adj_list = tree

# Identify the inclusive gateways
inclusive_gateways = [node for node in adj_list if 'inclusive' in node]
exclusive_gateways = [node for node in adj_list if 'exclusive' in node]

# Retrieve the nodes in between the gateway
nodes_between = set()


def getNodesBetween(node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in adj_list.get(node, []):
        if neighbor == inclusive_gateways[1]:
            break
        if neighbor not in visited:
            getNodesBetween(neighbor, visited)
    return visited

nodes_between = getNodesBetween(inclusive_gateways[0])
nodes_between.remove(inclusive_gateways[0])


# Join nodes that are directly connected to each other
def join_nodes():
    temp = deepcopy(nodes_between)
    for node in temp:
        for neighbor in adj_list.get(node, []):
            if neighbor in temp:
                adj_list[str(node) + str(neighbor)] = adj_list.get(neighbor, [])
                nodes_between.remove(node)
                nodes_between.remove(neighbor)
                nodes_between.add(str(node) + str(neighbor))
                # Remap the nodes in the adjacency list
                for key in adj_list:
                    for value in adj_list[key]:
                        if value == node:
                            adj_list[key].append(str(node) + str(neighbor))
                            adj_list[key].remove(node)
                del adj_list[neighbor]
                del adj_list[node]


join_nodes()


# Implementing paths for node between inclusive gateways
def remapNodes():
    for node in nodes_between:
        temp = deepcopy(nodes_between)
        temp.remove(node)
        for element in temp:
            adj_list[node].append(element)


remapNodes()



def temporalDependency(node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for neighbor in adj_list.get(node, []):
        if neighbor not in visited:
            temporalDependency(neighbor, visited)
    return visited


# Replace with your start node
temporalList = temporalDependency('A')

# Path finder
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]

    # If the start node is the end node, we've found a path
    if start == end:
        return [path]

    # If the start node is not in the graph, there are no paths
    if start not in graph:
        return []

    paths = []

    # Recursively explore each adjacent node
    for node in graph[start]:
        if node not in path:  # Avoid cycles
            new_paths = find_all_paths(graph, node, end, path)
            for p in new_paths:
                paths.append(p)

    return paths

# Start and end nodes
start_node = 'A'
end_node = 'J'

# Find all paths
all_paths = find_all_paths(adj_list, start_node, end_node)

print('\n')
for path in all_paths:
    print(" -> ".join(path))
