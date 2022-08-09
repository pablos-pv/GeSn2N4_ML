
juview(strset)

##################################################################################################
###############################################################
# Calculate the correlation
from clusterx.clusters.clusters_pool import ClustersPool
from clusterx.correlations import CorrelationsCalculator
#juview(cpool.get_cpool_atoms(),n=3)

corrcal = CorrelationsCalculator("binary-linear", plat, cpool)

print('The number of configurations is ',len(strset))

fmatrix    = open('correlationmatrix.txt', "wt")

for iconf in range(len(strset)):
	print('doing configuration ',iconf)

	structure = strset.get_structure(iconf)
	juview(structure.get_atoms())
	
	mult = cpool.get_multiplicities()
	corrs = corrcal.get_cluster_correlations(structure, multiplicities=mult)
	fmatrix.write(str(iconf))

	for i in range(len(cpool)):
	    print ("Cluster: ",i,"|   Correlation: ", corrs[i], "|   Multiplicity: ", mult[i])
	    fmatrix.write(' '+str(int(round(corrs[i]*mult[i]))))
        
        
	fmatrix.write('\n')


