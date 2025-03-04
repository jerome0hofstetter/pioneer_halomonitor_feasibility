# Data analysis for feasibility of halomonitor

#TODO

geo_files directory is the location for .json and .gdml files for future modeling

for now main interest plot is via running offshoot_data_analysis 

aim of the plotting is that rootfiles from a run are in a folder called output or specified, data is extracted in a certain way and plotted.

As a step between it first checks if the data is already is in a seperate file in the numpy_folder, if so load that, else import ROOT, set it up, grab the data from the root files, save it as a numpy file and then return