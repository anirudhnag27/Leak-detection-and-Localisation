# Leak-detection-and-Localisation
This project was performed at CSIR-CEERI Pilani, as a part of Practice School 1 programme of BITS Pilani.

A water network was simulated using EPANET as the hydraulic simulation software. Leaks of different sizes were simulated for various time intervals using Extended Period Analysis. Leaks cause changes in the pressure of the water grid. This fact has been used to detect and localise leakages in the grid.

The generated data was stored in Excel sheets. The "pressure_data_preparation.py" file extracts the pressure data from the excel files and generates the train and test data for the leak-predicting neural network - "Leak_detection_using_DNN.ipynb" - data visualisation has shown that small leaks are harder to detect due to less changes in pressure. Leak localisation has been accomplished using the code in "leak_localization_1.py". The junction with maximum difference in pressure compared to the non-leak case has been identified as the node with the leak.

The data has to be organised in the same directory structure as in this repository for "pressure_data_preparation.py" and "leak_localization_1.py" to work appropriately.
