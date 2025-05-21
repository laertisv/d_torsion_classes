from main import HigherTauTiltingTheoryHomogeneousLinearNakayamaCalculator
from modules.functions import ext_d_projective_modules, maximal_projective, minimal_torsion_class, is_tau_d_rigid_pair
from modules.helpers import string_from_modules, format_path
from datetime import datetime
from io import StringIO

def validate_tau_d_pair_size(M, P, expected_n):
    """
    Validate that the basic form of M ⊕ P has exactly n modules.
    
    :param M: List of modules in M
    :param P: List of modules in P
    :param expected_n: Expected number of modules
    :return: tuple (bool, str) - (is_valid, error_message)
    """
    M_set = set(M) if M else set()
    P_set = set(P) if P else set()
    total_modules = len(M_set.union(P_set))
    
    if total_modules != expected_n:
        return (False, f"Expected {expected_n} modules, found {total_modules}")
    return (True, "Size requirement satisfied")

def validate_minimal_torsion_class(M_U, U, all_torsion_classes):
    """
    Validate that U is the minimal d-torsion class containing M^U.
    
    :param M_U: List of modules in M^U
    :param U: A d-torsion class
    :param all_torsion_classes: List of all d-torsion classes as tuples (torsion_class, path)
    :return: tuple (bool, str) - (is_valid, error_message)
    """
    # Convert M_U and U to sets for comparison
    U_set = set(U)
    
    # Find minimal torsion class containing M_U
    min_tc = minimal_torsion_class(M_U, all_torsion_classes)
    
    if min_tc is None:
        return (False, "Could not find a torsion class containing M^U")
    if set(min_tc) != U_set:
        return (False, f"Minimal torsion class containing M^U differs from U")
    return (True, "Minimal torsion class requirement satisfied")

def validate_torsion_class_count(d, l, p, n, actual_count):
    """
    Validate if the number of d-torsion classes matches the conjectured formula.
    
    :param d: The d parameter from the algebra
    :param l: The l parameter from the algebra
    :param p: The p parameter from the algebra
    :param n: The n parameter from the algebra
    :param actual_count: Actual number of d-torsion classes found
    :return: tuple (bool, str) - (matches_formula, message)
    """
    expected_count = None
    
    if p == 2:
        expected_count = n + l + 1
    elif p == 4 and d > 2 and l > 2:
        expected_count = int((35 * l * l + 10 * l * n + 39 * l + 2 * n * n + 30 * n - 18) / 18)
    elif p == 4 and d == 2 and l == 3:
        expected_count = int((35 * l * l + 10 * l * n + 39 * l + 2 * n * n + 30 * n - 18) / 18)
    
    if expected_count is None:
        return (True, "No formula to check for these parameters")
        
    if actual_count == expected_count:
        return (True, f"Number of {d}-torsion classes ({actual_count}) matches the formula")
    else:
        return (False, f"Conjectured {expected_count} {d}-torsion classes but found {actual_count}. Difference: {actual_count - expected_count}")

def test_algebra(d, l, p, write_output):
    """
    Given an algebra with parameters (d,l,p), two tests are performed.

    First it is tested whether the number of d-torsion classes agrees with the formula of Remark 4.23 from https://arxiv.org/pdf/2410.19505.
     
    Second for each d-torsion class U it is tested whether the summand maximal tau_d-rigid pair (M^U, P^U) obtained by taking M^U to be the Ext^d-projective generator of U is computed correctly. This is done by checking three conditions: that the pair (M^U, P^U) has the correct number of indecomposable summands, that the minimal d-torsion class containing M^U is U, and that (M^U, P^U) is a tau_d-rigid pair.
    """
    write_output(f"\nTesting algebra with d={d}, l={l}, p={p}")
    
    # Initialize calculator with given parameters
    calc = HigherTauTiltingTheoryHomogeneousLinearNakayamaCalculator()
    calc.d = d
    calc.l = l
    calc.p = p
    calc._calculate_n()
    calc._calculate_simples()
    calc._calculate_projectives()
    calc._calculate_d_cluster_tilting_subcategory()
    calc._build_graph()
    
    # Get all d-torsion classes
    torsion_classes = calc.get_all_torsion_classes()
    actual_count = len(torsion_classes)
    write_output(f"Found {actual_count} {d}-torsion classes")

    # Check conjectured formula
    formula_valid, formula_message = validate_torsion_class_count(d, l, p, calc.n, actual_count)
    if not formula_valid:
        write_output(f"\nFormula validation failed: {formula_message}")
    else:
        write_output(f"\nFormula validation: {formula_message}")
    
    # Test each d-torsion class
    failed_tests = []
    for i, (tc, path) in enumerate(torsion_classes, 1):
        # Show progress (only to terminal, not to log)
        print(f"\rChecking {d}-torsion class {i}/{actual_count}", end='')

        # Compute tau_d-rigid pair
        M_U = ext_d_projective_modules(tc, calc.simples, calc.d, calc.l, calc.n)
        P_U = maximal_projective(M_U, calc.projectives)
        
        # Validate size
        size_valid, size_message = validate_tau_d_pair_size(M_U, P_U, calc.n)
        
        # Validate minimal torsion class
        min_tc_valid, min_tc_message = validate_minimal_torsion_class(M_U, tc, torsion_classes)
        
        # Validate tau_d-rigid pair
        rigid_valid, rigid_message = is_tau_d_rigid_pair(M_U, P_U, calc.l, calc.d)
        
        if not size_valid or not min_tc_valid or not rigid_valid:
            failed_tests.append((i, tc, path, M_U, P_U, size_message, min_tc_message, rigid_message))
    
    print()

    # Report results
    if failed_tests:
        write_output("\nFailed tests:")
        for test_num, tc, path, M_U, P_U, size_msg, min_tc_msg, rigid_msg in failed_tests:
            write_output(f"\nTorsion class {test_num}:")
            write_output(f"U = {string_from_modules(tc)}")
            write_output(f"Path: {format_path(path)}")
            write_output(f"M^U = {string_from_modules(M_U)}")
            write_output(f"P^U = {string_from_modules(P_U)}")
            if not size_msg.startswith("Size requirement satisfied"):
                write_output(f"Size Error: {size_msg}")
            if not min_tc_msg.startswith("Minimal torsion class requirement satisfied"):
                write_output(f"Minimal TC Error: {min_tc_msg}")
            if not rigid_msg.startswith("Valid"):
                write_output(f"Rigid Pair Error: {rigid_msg}")
        return False
    else:
        write_output("\nAll tau_d-rigid pairs satisfy all three conditions!")
        return True

def run_tests():
    """Run tests for several parameter combinations and save output to log file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"test_results_{timestamp}.txt"
    string_buffer = StringIO()

    test_cases = [
        #(d, l, p),
        (2, 2, 2), 
        (2, 2, 3), 
        (2, 2, 4),
        (2, 2, 5),
        (2, 2, 6),
        (2, 3, 2),
        (2, 3, 4),
        (2, 3, 6),
        (2, 4, 2),
        (2, 4, 4),
        (2, 4, 6),
        (2, 6, 2),
        (2, 6, 4),
        (2, 6, 6),
        (3, 2, 2),
        (3, 2, 3),
        (3, 2, 4),
        (3, 2, 5),
        (3, 2, 6),
        (4, 2, 2),
        (4, 2, 3),
        (4, 2, 4),
        (4, 2, 5),
        (4, 2, 6),
        (4, 3, 2),
        (4, 3, 4),
        (4, 3, 6),
        (4, 4, 2),
        (4, 4, 4),
        (4, 4, 6),
        (4, 5, 2),
        (4, 5, 4),
        (4, 5, 6),
        (4, 6, 2),
        (4, 6, 4),
        (4, 6, 6),
        (6, 2, 2),
        (6, 2, 3),
        (6, 2, 4),
        (6, 2, 5),
        (6, 2, 6),
        (6, 3, 2),
        (6, 3, 4),
        (6, 3, 6),
        (6, 4, 2),
        (6, 4, 4),
        (6, 4, 6),
        (6, 5, 2),
        (6, 5, 4),
        (6, 5, 6),
        (6, 6, 2),
        (6, 6, 4),
        (6, 6, 6),
    ]
    
    total_cases = len(test_cases)
    all_passed = True
    
    def write_output(message):
        print(message)  # Print to console
        print(message, file=string_buffer)  # Write to buffer
    
    write_output("Starting tests...")
    
    for case_num, (d, l, p) in enumerate(test_cases, 1):
        write_output(f"\nRunning test case {case_num}/{total_cases}")
        if not test_algebra(d, l, p, write_output):
            all_passed = False
    
    if all_passed:
        write_output("\nAll tests passed successfully!")
    else:
        write_output("\nSome tests failed. Check the output above for details.")
    
    # Save buffer to file
    with open(log_file, 'w') as f:
        f.write(string_buffer.getvalue())
    
    string_buffer.close()
    print(f"\nTest results have been saved to: {log_file}")

if __name__ == "__main__":
    run_tests()


# - Include README.md.
# - Upload to github.