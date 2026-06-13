import networkx as nx
import random

# Variables
file = "p2p-Gnutella08-mod.txt"
G = nx.read_adjlist("files/"+file, create_using=nx.DiGraph(), nodetype=int)
m = 0.15 #Damping factor (Probability that user will follow random link from actual website. So there is 1-m probability that user will jump to other random page)
tolerance = 0.000001 #This value used to decide if stable state or not.
steps = 100  #number of max steps
nodes = list(G.nodes())    #[0, 1, 2, 3]
number_of_nodes = G.number_of_nodes() #get number of nodes


def random_suffer(graph, m, steps): #function random_suffer takes args - graph: G, m: damping factor, steps: max. number of iterations

    visit = {}  #Create empty dict. Here I will save node and number of visits
    for node in nodes:  #Iterate through all nodes
        visit[node] = 0  #add nodes and value 0 for visits into dict. 

    actual_node = random.choice(nodes)  #choose starting node randomly from list of nodes

    for _ in range(steps):
        if random.random() < m or graph.out_degree(actual_node) == 0:  #if random number < m or dangling node
            actual_node = random.choice(nodes)  #jump to random node from all nodes
        else:
            neighbors = list(graph.neighbors(actual_node))  #Get all nodes, that are connected to actual_node 
            actual_node = random.choice(neighbors)   #jump to random node that is connected to node

        visit[actual_node] += 1 #And add +1 to node visit count dict. (tracking number of visits of each node)

    #sort dictionary with nodes and number of visits. I dont know what is lambda function, I found it on the internet.
    sorted_dict_visit = dict(sorted(visit.items(), key=lambda item: item[1], reverse=True))
    
    return dict(list(sorted_dict_visit.items())[:10])  #return first 10 most visited nodes




def pagerank(graph, m, steps):
    visit = {}  #Create empty dict. Here I will save node and number of visits
    for node in nodes:  #Iterate through all nodes
        visit[node] = 1 / number_of_nodes  #add nodes and value 1/n for each node. n = number of nodes

    for _ in range(steps):
        visit_copy = visit.copy()  #copy of current PageRank values for stable state check

        # Update PageRank values for each node
        for node in graph.nodes:
            sum_pr = 0
            for neighbor in graph.predecessors(node):   #iterate neighbors
                sum_pr += visit_copy[neighbor] / len(list(graph.neighbors(neighbor))) 
                '''
                step = iterating through number of steps [1,2,3,4...]
                    nodes = iterating through number of nodes. [1,2,3,4...]
                        neighbor in graph.predecessors(node) = iterating through neighbors of (node). [0,2,1,4] (number. neighbors)
                            in sum_pr:   a) visit_copy[neighbor] = pagerank of neighbor pointing on iterated node [0.25] at the start if 4 nodes
                                         b) len(list(graph.neighbors(neighbor))) = number of elements in list that contains number of outcomes from neighbor that pagerank am I using
                '''             
            visit[node] = (1 - m) + m * sum_pr  

        # STABLE STATE CHECK
        max_diff = 0
        for node in graph.nodes:  #iterate nodes
            current_diff = abs(visit[node] - visit_copy[node])   #calculate abs (difference between currect and previous pagerank value). 
            max_diff = max(max_diff, current_diff)  #max() will return me always higher value,

            if max_diff < tolerance:    #check if max_diff is under tolerance. This will never be true in first run, so else:
                needed_iterations -= 1     #if stable state, needed_iterations - 1. (to ensure 10x success)
            else:  #set needed_iterations to 10. (I need 10 iterations where max_diff < tolerance to get stable state)
                needed_iterations = 10  # reset 
            if needed_iterations == 0:    #if 10x in the row stable state
                print("Approx number of iterations to get stable state in pagerank: {}".format(_))
                print("\n")
                break

    sorted_dict_visit = dict(sorted(visit.items(), key=lambda item: item[1], reverse=True)) #sorted_dict_visit 

    #return just first 10 highest values
    return dict(list(sorted_dict_visit.items())[:10])



### RUN THE PROGRAM
print("\n")
print("running file: {}, with steps: {}".format(file,steps))
print("\n")
print("First 10 most visited nodes in random suffer: {}".format(random_suffer(G,m,steps).keys()))
print("--------------------------------")
print("First 10 most visited nodes in page rank: {}".format(pagerank(G,m,steps)))
print("\n")