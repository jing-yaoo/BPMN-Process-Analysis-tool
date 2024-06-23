from xmlParser import tree, endElementName
import collections
from copy import deepcopy

#TODO implement logic for inclusive and exlusive gateways

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
                adj_list[str(node)+str(neighbor)] = adj_list.get(neighbor, [])
                nodes_between.remove(node)
                nodes_between.remove(neighbor)
                nodes_between.add(str(node)+str(neighbor))
                # Remap the nodes in the adjacency list
                for key in adj_list:
                    for value in adj_list[key]:
                        if value == node:
                            adj_list[key].append(str(node)+str(neighbor))
                            adj_list[key].remove(node)
                del adj_list[neighbor]
                del adj_list[node]

join_nodes()

print(adj_list.get('J',[]))

def temporalDependency(node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    if node == endElementName:
        return visited
    for neighbor in adj_list.get(node, []):
        if neighbor not in visited:
            temporalDependency(neighbor, visited)
    return visited

# Replace with your start node
list = temporalDependency('A')

for element in list:
    print(f"{element}\n")








    

