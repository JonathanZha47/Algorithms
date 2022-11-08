import sys
import queue
import simplegraphs as sg



def BFS(G, s):
    distance = {}
    parents = {}
    finalized = {}
    branch = {}
    branch_number = {}
    layers = [[] for d in range(G["n"])]
    Q = queue.Queue()
    distance[s] = 0
    parents[s] = None
    Q.put(s)
    i = 0
    for m in G["adj"][s]:
        branch[i] = []
        branch[i].append(m)
        branch_number[m] = i
        i += 1
    while not (Q.empty()):  # Q not empty
        u = Q.get()
        if u not in finalized:  # if u was already finalized, ignore it.
            finalized[u] = True
            layers[distance[u]].append(u)
            for v in G["adj"][u]:
                if v not in distance:
                    # record v's distance and parent and add v to the queue if
                    # this is the first path to v,
                    parents[v] = u
                    distance[v] = distance[u] + 1
                    Q.put(v)
                    if u != s:
                        branch_number[v] = branch_number[u]
                        branch[branch_number[u]].append(v)
    return distance, parents, layers, branch, branch_number

def shortestHole(G, s):
    found = False
    hole_length = -1  # Default value for when no hole is found
    hole_nodes = []  # Default value for when no hole is found

    ########################################
    # Write code that finds the shortest hole containing s if one exists
    # If one exists, set 'found' to True
    # Set hole_length to be the length of the shortest hole
    # Set hole_nodes to be a list of the nodes in the hole in order,
    #    starting from s (and not repeating s)
    ########################################

    # For example, maybe your first step would be to run the usual BFS
    d, parent, layer, branch, b_number = BFS(G, s)
    temp_length = -1
    for i in branch:
        for b in branch[i]:
            for c in G["adj"][b]:

                if c != s and b_number[b] < b_number[c]:
                    found = True
                    current_node = c
                    cycle = []
                    while(current_node!= s):
                        cycle.append(current_node)
                        current_node = parent[current_node]

                    cycle2 =[]
                    current_node2 = b
                    while (current_node2 != s):
                        cycle2.append(current_node2)
                        current_node2 = parent[current_node2]
                    list.reverse(cycle)
                    temp_nodes = [s] + cycle + cycle2
                    temp_length = len(temp_nodes)

                    if(hole_length == -1):
                        hole_nodes = temp_nodes
                        hole_length = temp_length
                    elif (hole_length > temp_length):
                        hole_nodes = temp_nodes
                        hole_length = temp_length
    # Return the output
    return found, hole_length, hole_nodes


#########################################################
# Don't modify the stuff below this line for submission
# (Of course you can change it while you're
#    doing your own testing if you want)
#########################################################


def readSource(start_file):
    # The source vertex is listed in its own file
    # It is an integer on a line by itself.
    with open(start_file, 'r') as f:
        raw_start = f.readline()
        s = int(raw_start)
    return s


def writeOutput(output_file, hole_found, hole_length, hole_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n".format(hole_found))
        f.write("{}\n".format(hole_length))
        f.write("{}\n".format(hole_list))
    return


def main(args=[]):
    # Expects three command-line arguments:
    # 1) name of a file describing the graph
    # 2) name of a file with the ID of the start node
    # 3) name of a file where the output should be written
    if len(args) != 3:
        print("Problem! There were {} arguments instead of 3.".format(len(args)))
        return
    graph_file = args[0]
    start_file = args[1]
    out_file = args[2]
    G = sg.readGraph(graph_file)  # Read the graph from disk
    s = readSource(start_file)  # Read the source from disk
    hole_found, hole_length, hole_list = shortestHole(G, s)  # Find the shortest hole!
    writeOutput(out_file, hole_found, hole_length, hole_list)  # Write the output
    return


if __name__ == "__main__":
    main(sys.argv[1:])
