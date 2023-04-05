# pySIRUS examples #

+ [example-md.py](example-md.py)       Update atom positions, lattice vectors and update dependent objects (potential, density)
+ [example-linalg.py](example-linalg.py)   Basic linear algebra operations  plane-wave coefficients (wfc objects) and occupation numbers
+ [stiefel\_manifold.py]([stiefel\_manifold.py) Evaluate total energy along a geodesic

# Units #
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
