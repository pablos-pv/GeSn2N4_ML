# GeSn2N4_ML

This repository contains all the data and code needed to reproduce the results from the scientific article "Spinel nitride solid solutions: charting properties in the configurational space with explainable machine learning", written by Pablo Sánchez-Palencia, Said Hamad, Pablo Palacios, Ricardo Grau-Crespo and Keith T. Butler.

### repository_data/
The folder repository_data/ contains the crystal structure of all the configurations in the studied configurational space in POSCAR format, as well as the results from the DFT calculations carried out with VASP program, including bandgaps and total energies. It also includes the code where the correlation between GGA and HSE bandgap results is calculated.

The correspondence between GGA results in "vasp-energies.csv" and the POSCAR structures is read from the "gga_structures_list.txt". The info in the .csv file is organised in the following columns: tag, inversion degree, total energy and bandgap. 

The correspondence between HSE results in "vasp-hseenergies.csv" and the POSCAR structures is read from the first column of the .csv file itselt, being the second column the bandgap results.

### figures/
The folder figures/ is used to reproduce all the main figures in the article with the exception of the predicted vs calculated values (figures 2a, 2b, 5a and 5b) and the SHAP analysis (figures 6c and 6d), which are directly in the code where the models are tested.

### descriptors/
The folder descriptors/ includes the code to generate the different descriptors tested from the structure files and to digest all the data from the repository into pikle format to pass it later to the machine learning models.

### ML_models/
The folder ML_models/ includes the code to train and score the different machine learning models, which use the .pkl files as input. The subfolder ensemble_weights/ saves the weights of the neural networks to be able to reproduce the same results by running the mlp.ipynb code in load mode.

### Version control
The version of this repository corresponding with the results presented in the work "Spinel nitride solid solutions: charting properties in the configurational space with explainable machine learning" can be accessed through its version number, by using: 
git checkout aba5aadb5fa60b8f12f5c7393af5ffea7ca750fc   