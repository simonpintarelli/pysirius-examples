import numpy as np

from sirius import DFT_ground_state_find

from sirius import CoefficientArray, PwCoeffs
# from sirius.coefficient_array import PwCoeffs
from numpy import linspace

import h5py
from h5py import File
from mpi4py import MPI


def sirius_save_state(objs_dict, prefix):
    """
    Save SIRIUS CoefficientArrays to hdf5.

    Arguments:
    objs_dict -- dictionary(string: CoefficientArray), example: {'Z': Z, 'G': G}
    kset      -- SIRIUS kpointset
    prefix    --
    """
    rank = MPI.COMM_WORLD.rank

    with h5py.File(prefix + "%d.h5" % rank, "w") as fh5:
        for key in objs_dict:
            # assume it is a string
            name = key
            sirius_save_h5(fh5, name, objs_dict[key])

def sirius_load_state(prefix, name, dst):
    """
    Arguments:
    prefix  -- path/to/prefix*.hdf5 file
    name      -- name of the dataset to be loaded
    dst       -- obj of type CoefficientArray or PwCoeffs
    """
    import glob
    rank = MPI.COMM_WORLD.rank

    with h5py.File(prefix + "%d.h5" % rank, "r") as fh5:
        for key in fh5[name].keys():
            kp_index, spin_index = tuple(fh5[name][key].attrs["key"])
            dst[(kp_index, spin_index)] = dst.ctype(fh5[name][key])
    return dst


def sirius_save_h5(fh5, label, obj):
    """
    Arguments:
    fh5  -- h5py.File
    label -- name for the object
    obj  -- np.array like / CoefficientArray
    """

    if isinstance(obj, CoefficientArray):
        grp = fh5.create_group(label)
        for key, val in obj.items():
            dset = grp.create_dataset(
                name=",".join(map(str, key)), shape=val.shape, dtype=val.dtype, data=val
            )
            dset.attrs["key"] = key
    else:
        grp = fh5.create_dataset(name=label, data=obj)
    return grp


# get an initial guess by a single SCF iteration
scf_maxiter = 1
res = DFT_ground_state_find(scf_maxiter, config="sirius.json")
# extract wrappers from C++
density = res["density"]
potential = res["potential"]
kset = res["kpointset"]

C = kset.C
fn = kset.fn

sirius_save_state({"C": C, "fn": fn}, prefix="init")

C_from_disk = sirius_load_state("init", "C", dst=PwCoeffs(ctype=np.matrix, dtype=np.complex128))
fn_from_disk = sirius_load_state("init", "fn", dst=CoefficientArray(ctype=np.array, dtype=np.float64))
