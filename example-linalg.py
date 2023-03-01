import numpy as np
from sirius.ot import Energy, ApplyHamiltonian

from sirius import DFT_ground_state_find
from sirius.coefficient_array import identity_like
from sirius.edft.ortho import loewdin
from numpy import linspace

# get an initial guess by a single SCF iteration
scf_maxiter = 1
res = DFT_ground_state_find(scf_maxiter, config='sirius.json')
# extract wrappers from C++
density = res['density']
potential = res['potential']
kset = res['kpointset']


H = ApplyHamiltonian(potential, kset)
E = Energy(kset, potential, density, H)

ctx = kset.ctx()

# wfct coefficients, type coefficient_array, behaves like a numpy ndarray
X = kset.C

# index by (kpoint_id, spin_id) -> numpy.ndarray
X_k0 = X[0, 0]

# occupation numbers
fn = kset.fn

# inner product
S = X.H @ X

# compute SVD of S
Us, ss, Vhs = S.svd()


# scale columns by occupation
Z = X*fn

# solve hermitian eigenvalue problem
w, Q = (Z.H@Z).eigh()

# rotate a wave-function vector by unitary matrix Q
_ = Z @ Q

#
Y = 2*X + Z

# identity
I = identity_like(Z)

# recompute KS-energy, Hamiltonian at (X', fn). Note density and potential are regenerated automatically.
# after completion kset.C, kset.fn will contain the values given to the routine
Etot, Hx = E.compute(loewdin(Y) @ Q, fn)
