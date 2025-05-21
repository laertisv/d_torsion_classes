from modules.classes import Module
from modules.helpers import get_edge_by_label

def compute_modules_for_node(node, position, simples, l):
    """
    Compute the list of modules for a given node based on its position in the path.

    :param node: The node name.
    :param position: The position of the node in the path.
    :param simples: List of simple modules.
    :param l: The l in the algegbra.
    :return: A list of Module objects.
    """
    modules = []
    base = simples[position-1].a # The base of the diagonal is the coordinate of the simple module

    # The case l=2 is special
    if l==2:
        if node.startswith("DFull"):
            modules.append(Module(base,base))
            return modules
        if node.startswith("DEmpty"):
            return modules

    if position % 2 == 1: # For odd diagonals, the first coordinate is constant
        if node.startswith("DOddOne"):
            modules.append(Module(base, base))
            return modules
        if node.startswith("DOddFull"):
            for h in range(0, l - 1):
                modules.append(Module(base, base + h))
            return modules
        for h in range(2,l):
            if node.startswith(f"DOdd{h}"):
                for offset in range(h-1, l-1):
                    modules.append(Module(base, base + offset))
                return modules
    else: # For even diagonals, the second coordinate is constant
        if node.startswith("DEvenFull"):
            for h in range(0,l-1):
                modules.append(Module(base-h,base))
            return modules
        for h in range(1,l-1):
            if node.startswith(f"DEven{h}"):
                for offset in range(0,h):
                    modules.append(Module(base-offset,base))
                return modules
    return modules

def compute_modules_for_edge(edge, position, simples, l, d):
    """
    Compute the list of modules for a given node based on its position in the path.

    :param edge: The edge name.
    :param position: The position of the edge in the path.
    :param simples: List of simple modules.
    :param l: The l in the algebra.
    :param d: The d in the d-cluster tilting.
    :return: A list of Module objects.
    """
    modules = []
    name = edge[3].get('name')
    starting_base = simples[position - 1].a # The base of the diagonal the edge starts at
    ending_base = simples[position].a # The base of the diagonal the edge ends at

    # The case l=2 is special
    if l==2:
        max_number = d # Total number of modules between the two diagonals
        if name == "e":
            for j in range(0, max_number):
                modules.append(Module(starting_base + j, starting_base + (l - 1) + j))
            return modules
        for h in range(0,d+1):
            if name == f"d{h}":
                for j in range(0,h):
                    modules.append(Module(ending_base - (l - 1) - j, ending_base - j))
                return modules

    if position % 2 == 1:
        max_number = int(((d - 2) / 2) * l + 2) # Total number of modules between the two diagonals
        for h in range(0, l):
            if name == f"e{h}":
                for j in range(0, max_number):
                    modules.append(Module(starting_base + j, starting_base + (l - 1) + j))
                return modules
        if name == "i":
            for j in range(0, max_number):
                modules.append(Module(starting_base + j, starting_base + (l - 1) + j))
        for h in range(0, max_number+1):
            if name == f"b{h}":
                for j in range(0, h):
                    modules.append(Module(ending_base - (l - 1) - j, ending_base - j))
                return modules
    else:
        max_number = int((d/2) *l) # Total number of modules between the two diagonals
        if name == "i-":
            for j in range(0, max_number):
                modules.append(Module(starting_base - (l - 1) + 1 + j, starting_base + 1 + j))
            return modules
        for h in range(0,max_number + 1):
            if name == f"k{h}":
                for j in range(0, h):
                    modules.append(Module(ending_base - 1 - j, ending_base-1 + (l - 1) - j))
                return modules
        for h in range(2,l):
            for k in range(0, l-h+1):
                if name == f"z{h}{k}":
                    for j in range(0,k):
                        modules.append(Module(ending_base - 1 - j, ending_base - 1 + (l - 1) - j))
                    return modules
        for h in range(1, l - 1):
            for k in range(0, l - h):
                if name == f"l{h}{k}":
                    for j in range(0,(max_number - (l - 1) + (h + k))): 
                        modules.append(Module(ending_base - 1 - j, ending_base - 1 + (l - 1) - j))
                    return modules
        if d == 2:
            for h in range(1, l - 2):
                for k in range(2, l - h):
                    for m in range(0, l - (h + k)):
                        if name == f"m{h}{m}{k}":
                            for j in range(0,max_number - (l - 1) + (h + m)): 
                                modules.append(Module(ending_base - 1 - j, ending_base - 1 + (l - 1) - j))
                            return modules
    return modules

def from_path_to_d_torsion_class(G, path, simples, l, d):
    """
    Compute the d-torsion class corresponding to a path in the graph G. No check is done to ensure the path is of the correct length or that it starts in an odd diagonal.

    :param G: The graph.
    :param path: The path in the graph.
    :param simples: List of simple modules.
    :param l: The l in the algebra.
    :param d: The d in the d-cluster tilting.
    :return: List of modules forming the torsion class
    """
    modules = []
    for i in range(0, len(path)):
        modules = (modules + compute_modules_for_node(path[i][0], i+1, simples, l)
                  + compute_modules_for_edge(get_edge_by_label(G, path[i][1]), i+1, simples, l, d))
    modules = modules + compute_modules_for_node(path[-1][2], len(path)+1, simples, l)
    return modules

def minimal_torsion_class(modules_collection, torsion_classes):
    """
    Find the minimal torsion class containing a given collection of modules.

    :param modules_collection: A list of modules inside the d-cluster tilting subcategory.
    :param torsion_classes: A collection of d-torsion classes given as list of tuples (torsion_class, path).
    :return: The minimal torsion class containing modules_collection, or None if no such class exists.
    """

    # Special case: if modules_collection is empty, return empty torsion class
    if not modules_collection:
        return []

    minimal_tc = None

    for tc, path in torsion_classes:
        # Check if modules_collection is a subset of the current torsion_class
        if set(modules_collection).issubset(set(tc)):
            # Update minimal_tc if this one is smaller
            if minimal_tc is None or len(tc) < len(minimal_tc):
                minimal_tc = tc

    return minimal_tc

def tau_d(module, d, l):
    """
    Compute the tau_d of a module M = (a, b). As d is even or l is equal to 2, only one formula is needed. Note that this code does not work if d is odd and l > 2 as there is a different formula in that case.

    :param module: A Module object.
    :param l: The l in the algebra.
    :param d: The d in the d-cluster tilting.
    :return: A Module object given by tau_d(M) = (b - (d/2)*l, a - ((d-2)/2)*l - 2).
    """
    a, b = module 
    new_a = int(b - (d / 2) * l)
    new_b = int(a - ((d - 2) / 2) * l - 2)

    if new_a <= 0 or new_b <= 0 or new_b < new_a:
        return None  # Represent zero module

    return Module(new_a,new_b)

def is_projective(module, l):
    """
    Check if the module is projective.
    
    :param module: Module object to check.
    :param l: The l parameter from the algebra.
    :return: True if the module is projective, False otherwise.
    """
    return module.a == 1 or (module.b - module.a == l - 1)

def is_injective(module, n, l):
    """
    Check if the module is injective.
    
    :param module: Module object to check.
    :param n: The n parameter from the algebra.
    :param l: The l parameter from the algebra.
    :return: True if the module is injective, False otherwise.
    """
    return module.b == n or (module.b - module.a == l - 1)

def get_diagonal(module, simples):
    """
    Compute the diagonal in which the module lies.
    
    :param module: Module object to check.
    :param simples: List of simple modules.
    :return: Integer between 1 and p corresponding to the diagonal.
    """
    for i, simple in enumerate(simples):
        if module.a == simple.a or module.b == simple.a:
            return i + 1
    raise ValueError(f"Module {module} does not align with any diagonal")

def ext_d_is_zero(module_a, module_b, simples, d, l, n):
    """
    Check if Ext^d(A,B) = 0 for two modules A and B in the d-cluster tilting subcategory.
    This is done by checking three cases:
    1. If A is projective or B is injective, then Ext^d(A,B) = 0
    2. If A and B are not in consecutive diagonals, then Ext^d(A,B) = 0
    3. If A and B are in consecutive diagonals, then Ext^d(A,B) = 0 if and only if
       τ_d(A) does not overlap with B in the appropriate coordinate
    
    :param module_a: First Module object (A).
    :param module_b: Second Module object (B).
    :param simples: List of simple modules to compute diagonals.
    :param d: The d parameter from the algebra.
    :param l: The l parameter from the algebra.
    :param n: The n parameter from the algebra.
    :return: True if Ext^d(A,B) = 0, False otherwise.
    """
    if module_a is None or module_b is None:
        return True # Represents zero module

    if is_projective(module_a, l) or is_injective(module_b, n, l):
        return True
        
    diagonal_a = get_diagonal(module_a, simples)
    diagonal_b = get_diagonal(module_b, simples)
    
    if diagonal_a == diagonal_b + 1:
        tau_d_module_a = tau_d(module_a, d, l)
        if diagonal_a % 2 == 1:
            if tau_d_module_a.a >= module_b.a:
                return False
            return True
        else:
            if tau_d_module_a.b >= module_b.b:
                return False
            return True
    else:
        return True

def ext_d_projective_modules(U, simples, d, l, n):
    """
    Find all Ext^d-projective modules in the subcategory U of C.
    
    :param U: A collection (list) of modules inside.
    :param simples: List of simple modules.
    :param l: The l parameter from the algebra.
    :param n: The n parameter from the algebra.
    :return: A list of all Ext^d-projective modules.
    """
    ext_d_projective_modules = []

    for module_a in U:
        is_projective = all(
            ext_d_is_zero(module_a, module_b, simples, d, l, n) 
            for module_b in U if module_b != module_a
        )
        if is_projective:
            ext_d_projective_modules.append(module_a)
    return ext_d_projective_modules

def hom_is_zero(module_a, module_b):
    """
    Check if Hom(A,B) = 0 for two modules A and B in the d-cluster tilting subcategory.
    
    :param module_a: First Module object (A) with coordinates (a,b).
    :param module_b: Second Module object (B) with coordinates (c,d).
    :return: True if Hom(A,B) = 0, False otherwise.
    """
    if module_a is None or module_b is None:
        return True # Represents one of the modules being the zero module

    a = module_a.a
    b = module_a.b
    c = module_b.a
    d = module_b.b
    if c <= b and b <= d and a <= c and c <= b:
        return False
    return True

def maximal_projective(M, projectives):
    """"
    Find the maximal collection (list) of projective modules which have no Hom to the collection (list) of modules M.

    :param M: A collection (list) of modules.
    :param projectives: A collection (list) of projective modules.
    :return: A list of all projective modules with no Hom to M.
    """
    P_M = []
    for projective in projectives:
        has_no_hom = all(
            hom_is_zero(projective, module) for module in M
        )
        if has_no_hom:
            P_M.append(projective)
    return P_M

def is_tau_d_rigid_pair(M_U, P_U, l, d):
    """
    Check if (M^U, P^U) is a τ_d-rigid pair by verifying three conditions:
    1. Hom(M_1, τ_d(M_2)) = 0 for all M_1, M_2 in M^U
    2. All modules in P^U are projective
    3. Hom(P, M) = 0 for all P in P^U and M in M^U
    
    :param M_U: List of modules in M^U.
    :param P_U: List of modules in P^U.
    :param l: The l parameter from the algebra.
    :param d: The d parameter from the algebra.
    :return: tuple (bool, str) - (is_valid, error_message).
    """
    # Check condition 1: Hom(M_1, τ_d(M_2)) = 0 for all M_1, M_2 in M^U
    for M1 in M_U:
        for M2 in M_U:
            tau_d_M2 = tau_d(M2, d, l)  
            if not hom_is_zero(M1, tau_d_M2):
                return (False, f"Condition 1 failed: Hom(M({M1.a},{M1.b}), τ_d(M({M2.a},{M2.b}))) ≠ 0")

    # Check condition 2: All modules in P^U are projective
    for P in P_U:
        if not is_projective(P, l):
            return (False, f"Condition 2 failed: M({P.a},{P.b}) is not projective")

    # Check condition 3: Hom(P, M) = 0 for all P in P^U and M in M^U
    for P in P_U:
        for M in M_U:
            if not hom_is_zero(P, M):
                return (False, f"Condition 3 failed: Hom(M({P.a},{P.b}), M({M.a},{M.b})) ≠ 0")

    return (True, "Valid τ_d-rigid pair: All conditions satisfied")