# Higher τ-tilting theory calculator for linear Nakayama algebras with homogeneous relations

A Python calculator for computations in higher $\tau$-tilting theory for linear Nakayama algebras with homogeneous relations based on the article [$\tau_d$-tilting theory for linear Nakayama algebras](https://arxiv.org/abs/2410.19505).

## Description

This calculator implements algorithms for working inside the $d$-cluster tilting subcategory of a linear Nakayama algebra with homogeneous relations. For such an algebra, it can
- compute all $d$-torsion classes,
- compute all summand maximal $\tau_d$-rigid pairs coming from $d$-torsion classes,
- check if a given pair is a summand maximal $\tau_d$-rigid pair, and if so, return the minimum $d$-torsion class containing it. 

## Prerequisites

- Python 3.8 or higher
- NetworkX library for graph operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TorsionClasses.git
cd TorsionClasses
```

2. Install networkx if not already installed:
```bash
pip install networkx
```

## Usage

Run the main program:
```bash
python main.py
```

The calculator first asks for the starting data $(l,d,p)$. Then it offers a menu with the following options:

1. Display information about the algebra
2. Compute all d-torsion classes
3. Compute summand maximal τ_d-rigid pair from d-torsion class
4. Find minimal d-torsion class containing a τ_d-rigid pair
5. Check if a pair (M,P) is τ_d-rigid
6. Change initial data
7. Convert between module formats
8. Exit

### Input Formats

Modules can be entered in two formats:
- comma format: `M-1-1,M-1-2,...`, or
- direct sum format: `M(1,1) ⊕ M(1,2) ⊕ ...`,

where $M(1,1)$ is the simple projective module and $M(n,n)$ is the simple injective module. For the zero module, use `0` or leave empty.

## Project Structure

```
HigherTauTiltingLinearNakayama/
├── modules/
│   ├── classes.py      # Module class definition
│   ├── functions.py    # Basic functions for computations
│   ├── graph_builder.py # Construction of graph G(C)
│   └── helpers.py      # Helper functions
├── tests/
│   └── test_tau_d_pairs.py  # Test suite
├── main.py            # Main program
└── README.md
```

## Testing

A test suite is available, mostly for double checking that the code gives correct results. It can be run with 

```bash
python -m tests.test_tau_d_pairs
```

The tests verify two things:
- That the summand maximal $\tau_d$-rigid pairs obtained from the $d$-torsion classes are correct.
- When there is a formula, that the number of $d$-torsion classes obtained agrees with the formula.

Test cases are hardcoded in the run_tests() function.

## Mathematical Background

For more details, definitions and notation refer to the article [$\tau_d$-tilting theory for linear Nakayama algebras](https://arxiv.org/abs/2410.19505).

This calculator implements algorithms for working inside the $d$-cluster tilting subcategory of a linear Nakayama algebra with homogeneous relations. Such an algebra has the form $kA_n/(\text{paths of length } l)$, where:

- $k$ is a field (irrelevant for the computations performed in this algorithm).
- $n \geq 1$ is an integer, corresponding to the number of vertices of a linearly oriented quiver of type $\mathbb{A}$: $n \rightarrow n-1 \rightarrow\cdots \rightarrow 2 \rightarrow 1$. We denote this quiver $A_n$. 
- $l \geq 2$ is an integer.

We write $\Lambda(n,l)$ for the algebra $kA_n/(\text{paths of length } l)$. Given $\Lambda(n,l)$ and an integer $d \geq 2$, there exists a $d$-cluster tilting subcategory of $\mathrm{mod}\Lambda(n,l)$ if and only if there exists an integer $p \geq 1$ such that
$$
n = (p − 1)\left(\frac{d-1}{2} l + 1\right) + \frac{l}{2}.
$$
and 
1. either $l=2$, or 
2. $l>2$, in which case both $d$ and $p$ must be even. 

The integer $p$ in the above equality corresponds to the number of simple modules in the $d$-cluster tilting subcategory. Equivalently, it corresponds to special collections of modules called "diagonals". 

By the above equality it becomes clear that choosing $l$, $d$ and $p$ gives rise to a unique $n$ for which the algebra $\Lambda(n,l)$ admits a $d$-cluster tilting subcategory. Thus the input to this calculator is the integers $l$, $d$ and $p$, subject to the parity condition when $l>2$.

Given the above input, the calculator has the following functions:

- Computes and displays information about the algebra and its $d$-cluster tilting subcategory $\mathcal{C}$. This includes the computation of the graph $G=G(\mathcal{C})$ which can be used to describe all $d$-torsion classes.
- Calculates all $d$-torsion classes and their corresponding path in $G$.
- Finds the summand maximal $\tau_d$-rigid pair coming from a $d$-torsion class $\mathcal{U}$ using the $\mathrm{Ext}^d$-projective generator of $\mathcal{U}$.
- Finds the minimal $d$-torsion class containing a given $\tau_d$-rigid pair (not necessarily summand maximal).
- Verifies if a given pair of modules is $\tau_d$-rigid and, if so, verifies if its basic form is summand maximal. 
- Converts between different module notation formats.

## Limitations

1. Only works for linearly oriented Nakayama algebras with homogeneous relations.
2. Formulas for the number of $d$-torsion classes exist only in the following cases:
    - $p=2$.
    - $p=4$, $l=3$, $d=2$.
    - $p=4$, $l>2$, $d>2$.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Authors

[Laertis Vaso](https://www.laertisvaso.com/)

## Acknowledgments

The mathematical background for this code is based on the article [τ_d-tilting theory for linear Nakayama algebras](https://arxiv.org/abs/2410.19505), co-authored with [Endre S. Rundsveen](https://endresr.github.io/).