from modules.classes import Module
from modules.graph_builder import build_graph
from modules.functions import from_path_to_d_torsion_class, ext_d_projective_modules, maximal_projective, minimal_torsion_class, is_tau_d_rigid_pair, tau_d
from modules.helpers import find_paths_of_given_length_in_a_multigraph, string_from_modules, parse_module_input, format_path

class HigherTauTiltingTheoryHomogeneousLinearNakayamaCalculator:
    # Initialization methods    
    def __init__(self):
        self.d = None # d in d-cluster tilting
        self.l = None # l is the length of paths modded out
        self.p = None # p is the number of diagonals in the d-cluster tilting subcategory
        self.n = None # n is the number of vertices in the quiver
        self.simples = None # simples is the list of simple modules
        self.projectives = None # projectives is the list of projective modules
        self.cluster_tilting = None  # C is the d-cluster tilting subcategory
        self.G = None # G is the graph giving d-torsion classes
        self.odd_nodes = None # odd_nodes is the list of all nodes with odd subscript
        self.even_nodes = None # even_nodes is the list of all nodes with even subscript

    def _should_retry(self, error_msg=None):
        if error_msg:
            print(f"\nError: {error_msg}")
        retry = input("\nTry again? (y/n): ")
        return retry.lower() == 'y'
    
    def _get_validated_input(self, prompt, validator, error_msg):
        """Generic input validator"""
        while True:
            try:
                value = int(input(prompt))
                if validator(value):
                    return value
                print(f"Error: {error_msg}")    
            except ValueError:
                print("Please enter a valid number")

    def _get_user_input(self):
        """Get and validate user input for d, l, and p"""
        # Get l first
        while self.l is None:
            try:
                self.l = self._get_valid_l()
            except ValueError as e:
                print(f"Error: {str(e)}")

        # Get d next - rules depend on l
        while self.d is None:
            try:
                self.d = self._get_valid_d()
            except ValueError as e:
                print(f"Error: {str(e)}")
    
        # Get p last - rules depend on l
        while self.p is None:
            try:
                self.p = self._get_valid_p()
            except ValueError as e:
                print(f"Error: {str(e)}")
        
    def _get_valid_l(self):
        return self._get_validated_input(
            "\nEnter l (length of zero paths): ",
            lambda x: x >= 2,
            "l must be greater than or equal to 2"
        )

    def _get_valid_d(self):
        if self.l == 2:
            return self._get_validated_input(
                "Enter d (for d-cluster tilting subcategory): ",
                lambda x: x >= 2,
                "d must be greater than or equal to 2"
            )
        else:
            return self._get_validated_input(
                "Enter d (for d-cluster tilting subcategory): ",
                lambda x: x >= 2 and x % 2 == 0,
                "d must be an even number greater than or equal to 2 when l > 2"
            )    
        
    def _get_valid_p(self):
        if self.l == 2:
            return self._get_validated_input(
                "Enter p (number of diagonals): ",
                lambda x: x >= 2,
                "p must be greater than or equal to 2"
            )
        else:
            return self._get_validated_input(
                "Enter p (number of diagonals): ",
                lambda x: x >= 2 and x % 2 == 0,
                "p must be an even number greater than or equal to 2 when l > 2"
            )
        
    def _calculate_n(self):
        self.n = int((self.p-1) * (((self.d-1)/2)*self.l + 1) + self.l/2)
        
    def _calculate_simples(self):
        s = []
        for i in range(1, self.p + 1):
            if i % 2 == 1:
                value = int((i - 1) * ((self.d - 1) / 2) * self.l + i)
            else:
                value = int((i - 1) * (((self.d - 1) / 2) * self.l + 1) + self.l / 2)
            s.append(value)
        
        self.simples = [Module(i, i) for i in s]
        
    def _calculate_projectives(self):
        self.projectives = ([Module(1, j) for j in range(1, self.l)] + 
                          [Module(i, i + (self.l - 1)) for i in range(1, self.n - (self.l - 1) + 1)])
    
    def _calculate_d_cluster_tilting_subcategory(self):
        C = set(self.projectives)  # Start with projectives
        
        # Add injective non-projective modules
        last_diagonal = []
        for i in range(self.l - 1):
            last_diagonal.append(Module(self.n - i, self.n))
        C.update(last_diagonal)
        
        # Apply tau_d p-2 times
        current_modules = last_diagonal
        for _ in range(self.p - 2):
            next_modules = []
            for module in current_modules:
                tau_d_module = tau_d(module, self.d, self.l)
                next_modules.append(tau_d_module)
            C.update(next_modules)
            current_modules = next_modules
        
        # Convert set to sorted list for better display
        self.cluster_tilting = sorted(list(C), key=lambda m: (m.a, m.b))

    def _build_graph(self):
        self.G, _, _, self.odd_nodes, self.even_nodes = build_graph(self.l, self.d)

    def _reset_values(self):
        """Reset all values to None before reinitializing"""
        self.d = None
        self.l = None
        self.p = None
        self.n = None
        self.simples = None
        self.projectives = None
        self.cluster_tilting = None
        self.G = None
        self.odd_nodes = None
        self.even_nodes = None

    def initialize(self):
        print("\nWelcome to the calculator of higher tau-tilting theory for linear Nakayama algebras with homogeneous relations!")
        print("--------------------------------")
        # Reset all values before getting new input
        self._reset_values()  
        self._get_user_input()
        self._calculate_n()
        self._calculate_simples()
        self._calculate_projectives()
        self._calculate_d_cluster_tilting_subcategory()
        self._build_graph()

    # Helper methods    
    def _format_module_pair(self, M_U, P_U):
        M_str = '0' if not M_U else ' ⊕ '.join(f'M({m.a},{m.b})' for m in M_U)
        P_str = '0' if not P_U else ' ⊕ '.join(f'M({m.a},{m.b})' for m in P_U)
        return M_str, P_str

    def _get_basic_pair(self, M, P):
        M_basic = list(set(M))
        P_basic = list(set(P))
        is_basic = (len(M) == len(M_basic) and len(P) == len(P_basic))
        return M_basic, P_basic, is_basic   

    def get_all_torsion_classes(self):
        paths = sum([find_paths_of_given_length_in_a_multigraph(
            self.G, node, self.p - 1) for node in self.odd_nodes], [])
        return [(from_path_to_d_torsion_class(self.G, path, self.simples, self.l, self.d), path) 
                for path in paths]
    
    # Menu
    def display_menu(self):
        print("\nMenu Options:")
        print(f"1. Display information about the algebra kA_{self.n}/(paths of length {self.l})")
        print(f"2. Compute all {self.d}-torsion classes")
        print(f"3. Compute summand maximal tau_{self.d}-rigid pair from {self.d}-torsion class")
        print(f"4. Find minimal {self.d}-torsion class containing a tau_{self.d}-rigid pair")
        print(f"5. Check if a pair (M,P) is tau_{self.d}-rigid")
        print("6. Change initial data")
        print("7. Convert between module formats")
        print("8. Exit")
        return input("\nEnter your choice (1-8): ")

    # Menu option 1
    def display_info(self):
        print(f"\nComputations correspond to the algebra kA_{self.n}/(paths of length {self.l})")
        print(f"This algebra admits a {self.d}-cluster tilting subcategory with {self.p} diagonals")
        print(f"\nIndecomposable modules in the {self.d}-cluster tilting subcategory C:")
        cluster_str = ", ".join(f"M({m.a},{m.b})" for m in self.cluster_tilting)
        print(cluster_str)
        print(f"Number of indecomposable modules in C: {len(self.cluster_tilting)}")
        
        print("\nSimple modules:")
        simple_str = ", ".join(f"M({m.a},{m.b})" for m in self.simples)
        print(simple_str)
        
        print("\nProjective modules:")
        proj_str = ", ".join(f"M({m.a},{m.b})" for m in self.projectives)
        print(proj_str)

        # Display graph information
        print("\nInformation about the graph G=G(C):")
        print(f"Number of vertices: {self.G.number_of_nodes()}")
        print(f"Number of edges: {self.G.number_of_edges()}")
        
        print("\nOdd nodes:")
        print(", ".join(self.odd_nodes))
        
        print("\nEven nodes:")
        print(", ".join(self.even_nodes))
        
        print("\nEdges and their labels:")
        for u, v, key, data in self.G.edges(keys=True, data=True):
            print(f"{u} -> {v}: {data.get('label', '')}")

    # Menu option 2
    def display_torsion_classes(self):
        print(f"\nComputing all {self.d}-torsion classes...")
        torsion_classes = self.get_all_torsion_classes()
        
        print(f"\nFound {len(torsion_classes)} {self.d}-torsion classes:")
        for i, (tc, path) in enumerate(torsion_classes, 1):
            print(f"\n{self.d}-torsion Class {i}:")
            print(f"Subcategory: {string_from_modules(tc)}")
            print(f"Path in graph: {format_path(path)}")

    # Menu option 3
    def display_compute_summand_maximal_tau_d_rigid_pair_menu(self):
        print(f"\nChoose {self.d}-torsion class to compute a summand maximal tau_{self.d}-rigid pair from :")
        print(f"1. Choose from list of all {self.d}-torsion classes")
        print(f"2. Input a {self.d}-torsion class manually")
        print("3. Back to main menu")
        return input("\nEnter your choice (1-3): ")

    def handle_summand_maximal_tau_d_rigid_pair_computation(self):
        while True:
            choice = self.display_compute_summand_maximal_tau_d_rigid_pair_menu()
            
            if choice == '1':
                # Get all torsion classes
                torsion_classes = self.get_all_torsion_classes()
                
                # Display them with numbers
                print(f"\nComputing all {self.d}-torsion classes...")
                print(f"\nFound {len(torsion_classes)} torsion classes:")
                for i, (tc, path) in enumerate(torsion_classes, 1):
                    print(f"\nTorsion Class {i}:")
                    print(f"Subcategory: {string_from_modules(tc)}")
                    print(f"Path in graph: {format_path(path)}")
                
                # Ask user to choose one
                while True:
                    try:
                        choice = int(input(f"\nChoose a {self.d}-torsion class (1-{len(torsion_classes)}): "))
                        if 1 <= choice <= len(torsion_classes):
                            selected_class, selected_path = torsion_classes[choice - 1]
                            print(f"\nYou selected the following {self.d}-torsion class U:")
                            print(f"Subcategory: {string_from_modules(selected_class)}")
                            print(f"Path in graph: {format_path(selected_path)}")

                            M_U = ext_d_projective_modules(selected_class, self.simples, self.d, self.l, self.n)
                            P_U = maximal_projective(M_U, self.projectives)
                            
                            print(f"\nThe summand maximal tau_{self.d}-rigid pair (M^U, P^U) is:\n")
                            M_str, P_str = self._format_module_pair(M_U, P_U)
                            print(f"M^U = {M_str}")
                            print(f"P^U = {P_str}")
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(torsion_classes)}")
                    except ValueError:
                        print("Please enter a valid number")
                        
            elif choice == '2':                
                print(f"\nEnter an additive generator of the {self.d}-torsion class in one of these formats:")
                print("1. M(1,1) ⊕ M(1,2) ⊕ ...")
                print("2. M-1-1,M-1-2,...")
                
                while True:
                    try:
                        input_str = input("\nEnter torsion class: ")
                        modules = parse_module_input(input_str, self.n, self.l)
                        
                        # Check if this is a valid torsion class
                        torsion_classes = self.get_all_torsion_classes()
                        valid_torsion_class = False
                        for tc, path in torsion_classes:
                            if set(modules) == set(tc):
                                valid_torsion_class = True
                                selected_class = tc
                                selected_path = path
                                break
                        
                        if not valid_torsion_class:
                            if not self._should_retry(f"This is not a valid {self.d}-torsion class"):
                                break
                            continue
                        
                        # Valid torsion class found
                        print(f"\nValid {self.d}-torsion class:")
                        print(f"Subcategory: {string_from_modules(selected_class)}")
                        print(f"Path in graph: {format_path(selected_path)}")
                            
                        M_U = ext_d_projective_modules(selected_class, self.simples, self.d, self.l, self.n)
                        P_U = maximal_projective(M_U, self.projectives)
                            
                        # Show the complete pair
                        print(f"\nThe summand maximal tau_{self.d}-rigid pair (M^U, P^U) is:\n")
                        M_str, P_str = self._format_module_pair(M_U, P_U)
                        print(f"M^U = {M_str}")
                        print(f"P^U = {P_str}")
                        break                                
                    except ValueError as e:
                        if not self._should_retry(str(e)):
                            break
                        
            elif choice == '3':
                print("\nReturning to main menu...")
                break
            else:
                print("\nInvalid choice. Please select 1-3.")

    # Menu option 4
    def handle_minimal_torsion_class_computation(self):
        print(f"\nEnter a tau_{self.d}-rigid pair (M,P) in one of these formats:")
        print("1. M: M-1-1,M-1-2,...; P: M-2-3,M-3-4,...")
        print("2. M: M(1,1) ⊕ M(1,2) ⊕ ...; P: M(2,3) ⊕ M(3,4) ⊕ ...")
        print("(Use 0 or leave empty for no indecomposable modules)")
        
        while True:
            try:
                m_input = input("\nEnter M part: ").strip()
                M = parse_module_input(m_input, self.n, self.l)
                
                p_input = input("Enter P part: ").strip()
                P = parse_module_input(p_input, self.n, self.l)
                
                # Check if pair is basic
                M_basic, P_basic, is_basic = self._get_basic_pair(M, P)
                
                # First verify if the pair is tau_d-rigid
                is_valid, message = is_tau_d_rigid_pair(M_basic, P_basic, self.l, self.d)
                
                if not is_valid:
                    print("\nError: The pair you entered is not tau_d-rigid")
                    print(message)
                    if not self._should_retry():
                        break
                    continue
                
                # tau_d-rigid found                
                torsion_classes = self.get_all_torsion_classes()
                min_tc = minimal_torsion_class(M_basic, torsion_classes)
                
                if min_tc is not None:
                    min_path = None
                    for tc, path in torsion_classes:
                        if set(tc) == set(min_tc):
                            min_path = path
                            break
                            
                    print(f"\nMinimal {self.d}-torsion class containing (M,P):")
                    print(f"Subcategory: {string_from_modules(min_tc)}")
                    print(f"Path in graph: {format_path(min_path)}")
                    
                    retry = input("\nFind minimal torsion class for another pair? (y/n): ")
                    if retry.lower() != 'y':
                        break
                else:
                    print("\nError: Could not find a torsion class containing this pair")
                    if not self._should_retry():
                        break
            except ValueError as e:
                if not self._should_retry(str(e)):
                    break
                continue
    
    # Menu option 5
    def handle_check_tau_d_rigid_pair(self):
        print(f"\nEnter a pair (M,P) in one of these formats:")
        print("1. M: M-1-1,M-1-2,...; P: M-2-3,M-3-4,...")
        print("2. M: M(1,1) ⊕ M(1,2) ⊕ ...; P: M(2,3) ⊕ M(3,4) ⊕ ...")
        print("(Use 0 or leave empty for no indecomposable modules)")
        
        while True:
            try:
                m_input = input("\nEnter M part: ").strip()
                M = parse_module_input(m_input, self.n, self.l)
                
                p_input = input("Enter P part: ").strip()
                P = parse_module_input(p_input, self.n, self.l)
                
                # Get basic version of pair
                M_basic, P_basic, is_basic = self._get_basic_pair(M, P)
                
                # Check if pair is tau_d-rigid using the basic version
                is_valid, message = is_tau_d_rigid_pair(M_basic, P_basic, self.l, self.d)
                
                if is_valid:
                    if not is_basic:
                        print("\nNote: The pair you entered is not basic (contains repeated modules).")
                        print("The basic version of your pair is:")
                        M_str, P_str = self._format_module_pair(M_basic, P_basic)
                        print(f"M = {M_str}")
                        print(f"P = {P_str}")
                    
                    # Check if the basic version is summand maximal
                    total_modules = len(set(M_basic).union(set(P_basic)))
                    is_maximal = total_modules == self.n
                    
                    print("\nThis is a valid tau_d-rigid pair!")
                    if is_maximal:
                        if is_basic:
                            print(f"Moreover, it is summand maximal as it has {self.n} indecomposable summands.")
                        else:
                            print(f"Moreover, its basic version is summand maximal as it has {self.n} indecomposable summands.")
                    else:
                        if is_basic:
                            print(f"However, it is not summand maximal (has {total_modules} modules instead of {self.n}).")
                        else:
                            print(f"However, its basic version is not summand maximal (has {total_modules} modules instead of {self.n}).")
                else:
                    if not is_basic:
                        print("\nNote: The pair you entered is not basic (contains repeated modules).")
                        print("The basic version of your pair is:")
                        print(f"M = {string_from_modules(M_basic)}")
                        print(f"P = {string_from_modules(P_basic)}")
                    print(f"\nThis is not a tau_d-rigid pair:")
                    print(message)
                
                retry = input("\nCheck another pair? (y/n): ")
                if retry.lower() != 'y':
                    break
            except ValueError as e:
                if not self._should_retry(str(e)):
                    break
                continue
    
    # Menu option 7
    def handle_format_conversion(self):
        print("\nEnter a module in one of these formats:")
        print("1. Comma format: M-1-1,M-1-2,...")
        print("2. Direct sum format: M(1,1) ⊕ M(1,2) ⊕ ...")
        
        while True:
            try:
                input_str = input("\nEnter module: ")
                input_str = input_str.strip()
                
                # Detect input format and convert to the other
                if "-" in input_str:
                    # Input was in comma format (M-1-1,M-1-2)
                    modules = parse_module_input(input_str, self.n, self.l)
                    print("\nModule in direct sum format:")
                    print(f"{' ⊕ '.join(f'M({m.a},{m.b})' for m in modules)}")
                else:
                    # Input was in direct sum format (M(1,1)⊕M(1,2))
                    modules = parse_module_input(input_str, self.n, self.l)
                    print("\nModule in comma format:")
                    print(",".join(f"M-{m.a}-{m.b}" for m in modules))
                
                retry = input("\nConvert another module? (y/n): ")
                if retry.lower() != 'y':
                    break                 
            except ValueError as e:
                if not self._should_retry(str(e)):
                    break    
    
    # Main program flow
    def run(self):
        self.initialize()
        
        menu_actions = {
            '1': self.display_info,
            '2': self.display_torsion_classes,
            '3': self.handle_summand_maximal_tau_d_rigid_pair_computation,
            '4': self.handle_minimal_torsion_class_computation,
            '5': self.handle_check_tau_d_rigid_pair,
            '6': self.initialize,
            '7': self.handle_format_conversion,
            '8': lambda: print("\nThank you! Bye!")
        }
        
        while True:
            choice = self.display_menu()
            if choice == '8':
                menu_actions[choice]()
                break
            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("\nInvalid choice. Please select 1-8.")

if __name__ == "__main__":
    calculator = HigherTauTiltingTheoryHomogeneousLinearNakayamaCalculator()
    calculator.run()
