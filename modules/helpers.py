from modules.classes import Module

def get_edge_by_label(graph, label):
    """
    Find the edge in a graph given its label.

    :param graph: A NetworkX MultiDiGraph.
    :param label: The label of the edge to search for.
    :return: A tuple (u, v, key, data) representing the edge, or None if no match is found.
    """
    for u, v, key, data in graph.edges(keys=True, data=True):
        if data.get('label') == label:
            return u, v, key, data 
    return None

def find_paths_of_given_length_in_a_multigraph(graph, start_node, path_length):
    """
    Find all directed paths of a given length in a multigraph, considering different edges as separate paths.
    
    :param graph: A NetworkX directed multigraph.
    :param start_node: The starting node of the paths.
    :param path_length: The desired length of the paths.
    :return: A list of paths, where each path is a list of (source, edge_label, target) tuples.
    """
    paths = []

    def dfs(current_path, current_node):
        # If the path reaches the desired length, add it to the results
        if len(current_path) == path_length:
            paths.append(current_path[:])
            return

        # Get all outgoing edges from the current node
        for _, neighbor, key, data in graph.out_edges(current_node, keys=True, data=True):
            edge_label = data['label']  # Extract the edge label
            dfs(current_path + [(current_node, edge_label, neighbor)], neighbor)

    # Start DFS from the start_node
    dfs([], start_node)
    return paths

def string_from_modules(module_list):
    """
    Convert a list of modules to a readable string format.
    
    :param module_list: List of Module objects
    :return: String in format 'add(M(a,b) ⊕ M(c,d) ⊕ ...)'
    """
    if not module_list:
        return "add(0)"
    
    modules_str = " \u2295 ".join(f"M({m.a},{m.b})" for m in module_list)
    return f"add({modules_str})"

def parse_module_input(input_str, n=None, l=None):
    """
    Parse user input string into a list of modules.
    Supports two formats:
    - M(1,1) ⊕ M(1,2) ⊕ ...
    - M-1-1,M-1-2,...

    Validates that modules are valid for the given algebra parameters.

    :param input_str: User input string
    :param n: Number of vertices in the quiver
    :param l: Path length bound
    :return: List of Module objects
    """
    # Handle empty input or "0"
    if not input_str or input_str == "0":
        return []
        
    # Detect format and split accordingly
    if "-" in input_str:
        module_strs = input_str.split(',')
    else:
        module_strs = input_str.split('⊕')
    
    modules = []
    for module_str in module_strs:
        module_str = module_str.strip()
        try:
            if module_str.startswith('M(') and module_str.endswith(')'):
                nums = module_str[2:-1].split(',')
                if len(nums) == 2:
                    a = int(nums[0])
                    b = int(nums[1])
                    modules.append(Module(a, b, n, l))
            elif module_str.startswith('M-'):
                nums = module_str[2:].split('-')
                if len(nums) == 2:
                    a = int(nums[0])
                    b = int(nums[1])
                    modules.append(Module(a, b, n, l))
            else:            
                raise ValueError(f"Invalid module format: {module_str}")
        except ValueError as e:
            raise ValueError(f"Invalid module {module_str}: {str(e)}")
    
    return modules

def format_path(path):
    """
    Format a path with arrows and labels in a readable format.
    
    :param path: List of tuples (source, label, target)
    :return: Formatted string representation of the path
    """
    if not path:
        return ""
        
    path_segments = [path[0][0]]

    for source, label, target in path:
        path_segments.extend([f"---{label}--->", target])
        
    return " ".join(path_segments)