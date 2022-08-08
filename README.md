# GeSn2N4_ML

This repository contains all the data and code needed to reproduce the results from the scientific article "Spinel nitride solid solutions: charting properties in the configurational space with explainable machine learning", written by Pablo Sánchez-Palencia, Said Hamad, Pablo Palacios, Ricardo Grau-Crespo and Keith T. Butler.

### repository_data/
The folder repository_data/ contains the crystal structure of all the configurations in the studied configurational space in POSCAR format, as well as the properties extracted from the DFT calculations carried out with VASP program, including bandgaps and total energies. It also includes the code where the correlation between GGA and HSE bandgap results is calculated (hse-data.ipynb), the .txt file with the CCFs descriptor generated with the CELL code [1] (correlation_matrix.txt) and the results from the thermodynamical analysis performed with SOD (inversion-analysis.xlsx).

The correspondence between GGA results in "vasp-energies.csv" and the POSCAR structures is read from the "gga_structures_list.txt". The info in the .csv file is organised in the following columns: tag, inversion degree, total energy and bandgap. 

The correspondence between HSE results in "vasp-hseenergies.csv" and the POSCAR structures is read from the first column of the .csv file itself, being the second column the bandgap results.

The output of the DFT calculations (OUTCAR files from VASP program) and the scripts to extract the properties in the presented format can be found in the zenodo repository: ....., in the folder "vasp_output_files/". The scripts to generate the CCFs can be found also there, in the folder "CCFs_generator/"

### figures/
The folder figures/ is used to reproduce all the main figures in the article with the exception of the predicted vs calculated values (figures 2a, 2b, 5a and 5b) and the SHAP analysis (figures 6c and 6d), which are directly in the code where the models are tested.

### descriptors/
The folder descriptors/ includes the code to generate the different descriptors tested from the structure files and to digest all the data from the repository into pikle format to pass it later to the machine learning models.

### ML_models/
The folder ML_models/ includes the code to train and score the different machine learning models, which use the .pkl files as input. The subfolder ensemble_weights/ saves the weights of the neural networks to be able to reproduce the same results by running the mlp.ipynb code in load mode.

### Version control
The version of this repository corresponding with the results presented in the work "Spinel nitride solid solutions: charting properties in the configurational space with explainable machine learning" can be accessed through its version number, by using: 
git checkout d2bd4a00f2a90f13f7c306e513235c22e26db014   


[1] https://sol.physik.hu-berlin.de/cell/
