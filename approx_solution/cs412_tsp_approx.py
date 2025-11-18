"""
    name : Your name ( s ) here

    Honor Code and Acknowledgments :
    This work complies with the JMU Honor Code .
    Comments here on your code and submission
"""

import itertools

 # All modules for CS 412 must include a main method that allows it
 # to imported and invoked from other python scripts
def main ():

    # EXAMPLE INPUT:
    """
    3 3
    a b 3.0
    b c 4.2
    a c 5.4
    
    Solution is:
    12.6000
    a b c a
    
    Graph is undirected
    """
    # Store a dict of all nodes and weights, then 
    # to make greedy choices here should we start by going to the next node with the lowest weight
    # then continue on advoiding any nodes we have already visited
    
    # For the randomness aspect refer to the pictures I've taken earlier
    # basically due it being a complete graph if we have five options with weights of 10, 20, 30, 40, 50
    # total = 150, so 10/150 + 20/150 + 30/150 + 40/150 + 50/150 = 1
    # have randomness based off the odds but reverse the above fractions turning 10/150 into the highest chance
    # as thats the "usual" greediest pick
    
    # Gets the results from the input function; # of Vertixs & Nodes, then a list of both edges and nodes
    V, E, edges, nodes = read_graph_from_stdin();

    # from this now apply the greedy strategy to get the approx runtime 

    # your code here
    pass

# chat generated function that reads from stdin and returns the number of vertices and nodes
# as well as a list of nodes and edges
def read_graph_from_stdin():
    import sys

    data = sys.stdin.read().strip().splitlines()
    if not data:
        raise ValueError("Empty input!")

    # Parse first line: V E
    header = data[0].split()
    if len(header) < 2:
        raise ValueError("First line must contain: <num_vertices> <num_edges>")
    V = int(header[0])
    E = int(header[1])

    edges = []
    nodes = set()

    # Parse edges
    for line in data[1:1+E]:
        u, v, w = line.split()
        w = float(w)

        edges.append((u, v, w))
        nodes.add(u)
        nodes.add(v)

    return V, E, edges, nodes

if __name__ == " __main__ " :
    main ()