
import sys
import heapq
import queue
import numpy as np
import simplegraphs as sg

             

def shortestDirCycle(G):
    best_cost = np.Infinity #You should output this if you don't find any cycles
    best_node_list = [] #You should output this if you don't find any cycles
    distances = {}  # actual distances
    finalized = {}  # set of discovered nodes
    parents = {}  # lists parent of node in SP tree
    Q = []  # empty priority queue. Use heappush(Q, (priority, val)) to add. Use heappop(Q) to remove.
    for s in G["adj"]:
        distances[s] = 0
        parents[s] = None
    heapq.heappush(Q, (distances[s], s))
    while len(Q) > 0:  # Q not empty
        (d, u) = heapq.heappop(Q)
        if u not in finalized:  # if u was already finalized, ignore it.
            finalized[u] = True
            for v in G["adj"][u]:
                new_length = distances[u] + G["adj"][u][v]
                # update v's distance (and parent and priority queue) if
                # either this is the first path to v
                # or we have found a better path to v
                if ((v not in distances) or (new_length < distances[v])):
                    distances[v] = new_length
                    parents[v] = u
                    # add a copy of v to the queue with priority distances[v]
                    heapq.heappush(Q, (distances[v], v))
        else:
            while u != None:
                best_node_list = u + best_node_list
                best_cost = G["adj"][u][parents[u]] + best_cost
                u = parents[u]
    return best_cost, best_node_list


############################################################
# input/output code. You shouldn't have to modify this. 
############################################################

def writeOutput(output_file, cost, node_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n{}\n".format(float(cost), node_list))
    return

def main(args=[]):
    # Expects two command-line arguments:
    # 1) name of a file describing the graph
    # 3) name of a file where the output should be written
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 2.".format(len(args)))
        return
    graph_file = args[0]
    out_file = args[1]
    G = sg.readGraph(graph_file) # Read the graph from disk
    best_cost, best_node_list = shortestDirCycle(G) # Find the shortest hole!
    writeOutput(out_file, best_cost, best_node_list) # Write the output
    return     

if __name__ == "__main__":
    main(sys.argv[1:])    


