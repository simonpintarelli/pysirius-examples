# pySIRUS examples #

+ [example-md.py](example-md.py)       Update atom positions, lattice vectors and update dependent objects (potential, density)
+ [example-linalg.py](example-linalg.py)   Basic linear algebra operations  plane-wave coefficients (wfc objects) and occupation numbers
+ [stiefel\_manifold.py]([stiefel\_manifold.py) Evaluate total energy along a geodesic

## Units ##
Unless otherwise specified, SIRIUS uses Hartree and Bohr. Atom positions are
specifed in relative coordinates to the unit cell.

## UPF to json conversion ##

SIRIUS parses pseudopotentials stored as json. A python script to convert from UPF to json is provided by SIRIUS [link](https://github.com/electronic-structure/SIRIUS/tree/master/apps/dft_loop):
```bash
python upf_to_json.py Xe.upf
```

UPF files can be found in the links below:
+ [pseudo-dojo](http://www.pseudo-dojo.org/)
+ [SSSP](http://www.pseudo-dojo.org/)
+ [QuantumESPRESSO](https://www.quantum-espresso.org/pseudopotentials/)


## Input file ##

The following is yaml (json doesn't support comments), however sirius only understands json, use `yq . example.yaml` to convert to json.

```yaml
# Schema: https://github.com/electronic-structure/SIRIUS/blob/develop/src/context/input_schema.json
control:
  # processing unit either `cpu` or `gpu`
  processing_unit: cpu
  # verbosity: 0: no output, 1: default output, 2: debug output
  verbosity: 1
parameters:
  # SIRIUS doesn't parse xc funcs from the PP-file, instead `xc_functionals` is used, if empty, no XC contribution is applied
  # for PBE use [XC_GGA_X_PBE, XC_GGA_C_PBE]
  # all available functionals: https://github.com/electronic-structure/SIRIUS/blob/develop/src/potential/xc_functional_base.hpp
  xc_functionals: [XC_LDA_X, XC_LDA_C_PZ]
  # smearing can be `gaussian`, `cold`, `fermi-dirac`
  smearing: gaussian
  # smearing witdh in Hartree
  smearing_width: 0.025
  use_symmetry: true
  # 0:
  num_mag_dims: 0
  # number of bands: -1 -> automatic
  num_fv_states: -1
  # wfc cutoff in Hartree
  gk_cutoff: 6
  # density cutoff in Hartree
  pw_cutoff: 20
  # SCF convergence thresholds
  energy_tol: 1.0e-08
  density_tol: 1.0e-08
  # maximum number of SCF iterations
  num_dft_iter: 100
  # k-point grid
  ngridk: [3, 3, 3]
unit_cell:
  # lattice vectors in Bohr
  lattice_vectors:
    - [5.397057814307557, 0, 0]
    - [2.698528907153779, 4.673989172883661, 0]
    - [2.698528907153779, 2.557996390961221, 4.406679252451386]
  atom_types:
    - Al
    - C
  atom_files:
    Al: Al.json
    C: C.json
  # atom positions in relative coordinates
  atoms:
    Al: [[0, 0, 0], [0.5, 0.5, 0.5]]
    C: [0.25, 0.25, 0.25]
  # optionally atom_coordinate_units can be specified,
  atom_coordinate_units: lattice # use `au` for Bohr, or `A` for Angstroms
```
