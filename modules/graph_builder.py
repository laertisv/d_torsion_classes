import networkx as nx

def build_graph(l, d):
    """
    Build the directed multigraph G=G(C) of d-torsion classes.
    
    Vertices: they correspond to which modules in the diagonals are included in the d-torsion class. They are labelled by
        1. Odd or Even, for the position of the diagonal,
        2. l, for the number of modules in the diagonal,
        3. up or down arrows, for the orientation of the modules in the diagonal
    
    Edges: they are directed between two vertices, with a label indicating the amount of such edges. The label corresponds to the collection of modules between the two diagonals corresponding to the start and end of the directed edge which is included in the d-torsion class.
    
    :param l: The l in A(n,l).
    :param d: The d in the d-cluster tilting subcategory.
    :return: A NetworkX MultiDiGraph object representing the directed multigraph which describes the d-torsion classes.
    """
    # Create the graph
    G = nx.MultiDiGraph()

    # Lists to store node names
    odd_nodes_list = []
    even_nodes_list = []

    # The case l==2 is special
    if l==2:
        G.add_node("DEmpty", label="$\\mathcal{D}^{\\downarrow}(0)$")
        even_nodes_list.append("DEmpty")
        odd_nodes_list.append("DEmpty")
        G.add_node("DFull", label="$\\mathcal{D}$")
        even_nodes_list.append("DFull")
        odd_nodes_list.append("DFull")

        G.add_edge("DEmpty", "DEmpty", label="$\\gamma$", name="g")
        G.add_edge("DFull", "DFull", label="$\\epsilon$", name="e")
        G.add_edge("DFull", "DEmpty", label="$\\beta$", name="b")
        for h in range(0,d+1):
            G.add_edge("DEmpty", "DFull", label=f"$\\delta_{{{h}}}$", name=f"d{h}")
    else:
        G.add_node("DEvenFull", label="$\\mathcal{D}_{2t}$")
        even_nodes_list.append("DEvenFull")
        G.add_node("DEvenEmpty", label="$\\mathcal{D}_{2t}^{\\downarrow}(0)$")
        even_nodes_list.append("DEvenEmpty")
        for h in range(1, l - 1):
            G.add_node(f"DEven{h}", label=f"$\\mathcal{{D}}^{{\\downarrow}}_{{2t}}({h})$")
            even_nodes_list.append(f"DEven{h}")
        G.add_node("DOddFull", label="$\\mathcal{D}_{2t+1}$")
        odd_nodes_list.append("DOddFull")
        G.add_node("DOddOne", label="$\\mathcal{D}_{2t+1}^{\\downarrow}(1)$")
        odd_nodes_list.append("DOddOne")
        G.add_node("DOddEmpty", label="$\\mathcal{D}_{2t+1}^{\\downarrow}(0)$")
        odd_nodes_list.append("DOddEmpty")
        for h in range(2, l):
            G.add_node(f"DOdd{h}", label=f"$\\mathcal{{D}}_{{2t+1}}({h})$")
            odd_nodes_list.append(f"DOdd{h}")

        G.add_edge("DEvenFull", "DOddFull", label="$\\iota^{-}$", name="i-")
        G.add_edge("DEvenFull", "DOddEmpty", label="$\\beta^{-}$", name="b-")
        G.add_edge("DEvenEmpty", "DOddEmpty", label="$\\gamma^{-}$", name="g-")
        G.add_edge("DEvenEmpty", "DOddOne", label="$\\eta^{-}$", name="h-")
        for h in range(0, int((d / 2) * l + 1)):
            G.add_edge("DEvenEmpty", "DOddFull", label=f"$\\kappa_{h}$", name=f"k{h}")
        for h in range(2, l):
            G.add_edge(f"DOdd{h}", "DEvenFull", label=f"$\\epsilon_{h}$", name=f"e{h}")
            for k in range(0, l - h + 1):
                G.add_edge("DEvenEmpty", f"DOdd{h}", label=f"$\\zeta_{{{h},{k}}}$", name=f"z{h}{k}")
        for h in range(1, l - 1):
            G.add_edge(f"DEven{h}", "DOddOne", label=f"$\\theta_{h}$", name=f"8{h}")
            G.add_edge(f"DEven{h}", "DOddEmpty", label=f"$\\delta^{{-}}_{h}$", name=f"d-{h}")
            G.add_edge("DOddEmpty", f"DEven{h}", label=f"$\\delta_{h}$", name=f"d{h}")
            for k in range(0, l - h):
                G.add_edge(f"DEven{h}", "DOddFull", label=f"$\\lambda_{{{h},{k}}}$", name=f"l{h}{k}")
        G.add_edge("DOddOne", "DEvenEmpty", label="$\\eta$", name="h")
        G.add_edge("DOddFull", "DEvenFull", label="$\\iota$", name="i")
        G.add_edge("DOddEmpty", "DEvenEmpty", label="$\\gamma$", name="g")
        for h in range(0, int(((d - 2) / 2 * l) + 3)):
            G.add_edge("DOddEmpty", "DEvenFull", label=f"$\\beta_{h}$", name=f"b{h}")
        if d==2:
            for h in range(1, l-2):
                for k in range(2, l-h):
                    for m in range(0, l-(h+k)):
                        G.add_edge(f"DEven{h}", f"DOdd{k}", label=f"$\\mu_{{{h},{m}}}^{{{k}}}$", name=f"m{h}{m}{k}")

    # Get the list of nodes with their attributes
    nodes = [(node, data) for node, data in G.nodes(data=True)]

    # Get the list of edges with attributes
    edges = [(u, v, key, data) for u, v, key, data in G.edges(keys=True, data=True)]

    return G, nodes, edges, odd_nodes_list, even_nodes_list