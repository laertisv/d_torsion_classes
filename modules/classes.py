# A class representing indecomposable modules over the algebra Λ(n,l)
class Module:
    def __init__(self, a, b, n=None, l=None):
        """
        Initialize a Module object, which is a tuple (a, b) where:
        - a and b are positive integers
        - 1 <= a <= b <= n
        - b - a + 1 <= l
        
        :param a: First coordinate
        :param b: Second coordinate
        :param n: Number of vertices in the quiver
        :param l: Path length bound
        """
        if not (isinstance(a, int) and isinstance(b, int)):
            raise TypeError("Both a and b must be integers.")
        if a <= 0 or b <= 0:
            raise ValueError("Both a and b must be positive integers.")
        if a > b:
            raise ValueError("a must be less than or equal to b.")

        # Algebra-specific validations
        if n is not None:
            if b > n:
                raise ValueError(f"b must be less than or equal to n={n}")
            
        if l is not None:
            length = b - a + 1
            if length > l:
                raise ValueError(f"Module length ({length}) cannot exceed l={l}")

        self.a = a
        self.b = b

    def __repr__(self):
        """Return a string representation of the Module."""
        return f"({self.a}, {self.b})"

    def __eq__(self, other):
        """Check equality of two Module objects based on coordinates."""
        if isinstance(other, Module):
            return self.a == other.a and self.b == other.b
        return False

    def __hash__(self):
        # Combine a and b for hashing
        return hash((self.a, self.b))

    def length(self):
        """Calculate and return the length of the module."""
        return self.b - self.a + 1

    def as_tuple(self):
        """Return the module as a tuple."""
        return self.a, self.b

    def __getitem__(self, index):
        """
        Allow indexing to access the coordinates of the module.

        :param index: 0 for the first coordinate (a), 1 for the second coordinate (b).
        :return: The corresponding coordinate.
        """
        if index == 0:
            return self.a
        elif index == 1:
            return self.b
        else:
            raise IndexError("Index out of range. Use 0 for 'a' or 1 for 'b'.")