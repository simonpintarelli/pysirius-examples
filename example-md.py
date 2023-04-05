import numpy as np

from sirius import DFT_ground_state_find
from sirius.coefficient_array import identity_like
from numpy import linspace
from sirius import atom_positions, set_atom_positions

# get an initial guess by a single SCF iteration
res = DFT_ground_state_find(num_dft_iter=100, config='sirius.json')
# extract wrappers from C++
kset = res['kpointset']
dft_obj = res['dft_gs']
ctx = kset.ctx()

uc = ctx.unit_cell()

# get lattice vectors
L = np.array(uc.lattice_vectors())
print(f'lattice vectors:\n {np.array(L)}')

for i in range(uc.num_atoms):
    atom = uc.atom(i)

    # relative coordinates
    rpos = atom.position()

    print(f'position of {atom.label}: {rpos}')

    # set new position
    atom.set_position(np.array(rpos)+0.01)

    print(f'updated position of {atom.label} {atom.position()}')

# uc.set_lattice_vectors(a1, a2, a3)
uc.set_lattice_vectors(*(L + 0.01*np.random.rand(*L.shape)))

# Update the parameters after the change of lattice vectors or atomic positions.
dft_obj.update()

# find new groundstate
dft_obj.find(density_tol=1e-10, energy_tol=1e-10, initial_tol=1e-4,
             num_dft_iter=10, write_state=False)

# get forces
forces = np.array(dft_obj.forces().calc_forces_total())

# occupation numbers
fn = kset.fn
