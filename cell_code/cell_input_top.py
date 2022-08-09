from ase.spacegroup import crystal
from clusterx.visualization import juview
from clusterx.super_cell import SuperCell
import numpy as np
from clusterx.structures_set import StructuresSet
from clusterx.structures_set import Structure
from clusterx.parent_lattice import ParentLattice
from ase import Atoms


###############################################################
a = 8.8529
wyckoff = [
(0.12500,-0.37500,0.62500) , (0.00000,-0.50000 ,0.00000) 
]
pri  = crystal(['Sn','Sn'], wyckoff, spacegroup=227, cellpar=[a, a, a, 90, 90, 90])
sub1 = crystal(['Sn','Sn'], wyckoff, spacegroup=227, cellpar=[a, a, a, 90, 90, 90])
sub2 = crystal(['Ge','Ge'], wyckoff, spacegroup=227, cellpar=[a, a, a, 90, 90, 90])

plat = ParentLattice(atoms=pri,substitutions=[sub1,sub2])
plat.serialize(fname="plat.json")
juview(plat)

# Information about sublattices
print("{0:<19s}|{1:<19s}|{2:<19s}|{3:<19s}|{4:<19s}".format("Atom index","Chemical symbol","x coordinate","y coordinate","z coordinate"))

# Information about atoms in the parent structure
for i, (symbol, x_coord, y_coord, z_coord) in enumerate(zip(pri.get_chemical_symbols(),pri.get_positions()[:,0],pri.get_positions()[:,1],pri.get_positions()[:,2])):
	print("{0:<19d}|{1:<19s}|{2:<19.3f}|{3:<19.3f}|{4:<19.3f}".format(i,symbol,x_coord,y_coord,z_coord))

print("")
###############################################################


###############################################################
# Supercell
scell = SuperCell(plat,[1,1,1])
scell.serialize(fname="scell.json")
juview(scell)
###############################################################


###############################################################
# Create clusters
from clusterx.clusters.clusters_pool import ClustersPool

import math
cpool = ClustersPool(plat, npoints=[0,1,2,3],super_cell=scell)

print(len(cpool), " clusters were created.")
juview(cpool)
cpool.write_clusters_db()
###############################################################


###############################################################
# Decorate supercell
strset = StructuresSet(scell, filename="test_cluster_expansion_structures_set.json")
