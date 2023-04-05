# pySIIRUS examples #

# Units #
Unless otherwise specified, SIRIUS uses Hartree and Bohr. Atom positions are
specifed in relative coordinates to the unit cell.

## UPF to json conversion ##

SIRIUS parses pseudopotentials stored as json. A python script to convert from UPF to json is provided by SIRIUS [link](https://github.com/electronic-structure/SIRIUS/tree/master/apps/dft_loop):
```bash
python upf_to_json.py Xe.upf
```
