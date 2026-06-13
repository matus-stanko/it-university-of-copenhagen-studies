import numpy as np

file_edgelist = "data/tiny_edgelist.txt"
file_matrix = "data/tiny_adjmatrix.txt"
node = 4    ##################   HERE SET NODE_ID      ###################


def readfile(filepath):  #I made function to readfile, because function coefficient_from_edgelist will be also used in function coefficient_from_matrix
    with open(filepath, "r") as file:
        edge_list = []
        for line in file.readlines():   #iterate each line
                line = line.strip()         #remove newline char
                start_node = int(line[0])   #get start node
                edge_node = int(line[-1])   #get neighbour
                edge_list.append((start_node, edge_node))  #add them to list as a tuples
    return edge_list

def coefficient_from_edgelist(edgefile, node_id):
    if type(edgefile) == str:  #if file is string, so "data/xxx.txt"
        edge_list = readfile(edgefile)   #then call function to read file
    else:
        edge_list = edgefile  #otherwise program will assume that you will provide list of tuples

    number_edges = len(edge_list)  #get number of edges

    nodes = set()  #create set
    for edge in edge_list:
        nodes.update(edge)  #add elemtents to the set
    
    number_nodes = len(nodes)

#### Create Adjacency dictionary with nodes as keys and paths to edges as a values
    adj_list = {}

    for node_i, node_j in edge_list:
        if node_i not in adj_list:
            adj_list[node_i] = set() # 'set' is used to prevent accidental multiple edges
    
        adj_list[node_i].add(node_j)
    
    # Manually add the opposite direction edge
        if node_j not in adj_list:
            adj_list[node_j] = set()
    
        adj_list[node_j].add(node_i)
    #print("File: {} \n No. of nodes: {} \n No. of edges {} \n Nodes: {} \n Adj list: {}".format(edge_list, number_nodes, number_edges,nodes,adj_list))

#

#Get number of neighbours
    selected_node = node_id
    values_of_neighbour = adj_list[selected_node]
    number_of_values = len(values_of_neighbour)

    '''
    So I was deviding by number of neighbours of desired nodes - it was wrong. Instead I need to devide by
    max routes between neighbours of desired node :)
    So I will use formula where n = number of neighbours  n(n-1)/2 (so I will get count of all possible ways how to connect n nodes)
    '''
    max_connections = (number_of_values * (number_of_values - 1))/2

    selected_node_neighbors = adj_list[selected_node]   #add values of selected node from dictionary. (neighbours)
    connections_count = 0  #set counter 
    for neighbor1 in selected_node_neighbors:   #now I am iterating through dictionary
        for neighbor2 in selected_node_neighbors: #iterating again to compare values, so I wont have duplicity
            if neighbor1 < neighbor2 and neighbor2 in adj_list[neighbor1]:  #check if pairs are unique, check if neighbour2 is connected with neigbor 1 
                connections_count += 1
  
    number_of_friends = connections_count
    
    print("Number of connection between friends of node {} is: {} \nMax ways between friends of node: {} is: {}".format(selected_node, number_of_friends, selected_node, max_connections))
    return round(number_of_friends/max_connections,3)



def coefficient_from_adjmatrix(matrixfile, node_id):
    matrix = np.loadtxt(matrixfile, dtype=int)   #load file as matrix using numpy
    edge_list = []  #create empty list
    for row in matrix:  #iterate rows in matrix
        tuple_row = tuple(row)  #and add them to the tuple
        edge_list.append(tuple_row)  #add tuple to list, so I will have list of tuples
    return coefficient_from_edgelist(edge_list, node)  #call first function, since its already made to work wil list of tuple


### CALLING FUNCTIONS :)

print(coefficient_from_edgelist(file_edgelist, node))
print(coefficient_from_adjmatrix(file_edgelist,node))
