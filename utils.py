import ROOT
import numpy as np
from lmfit import Model
import glob
import os
from scipy.signal import savgol_filter

PIONEER_FOLDER = "/home/akumashisen/PIONEER"

ROOT.gSystem.Load(f"{PIONEER_FOLDER}/main/install/lib/libPiRootDict.so")
ROOT.gSystem.Load(f"{PIONEER_FOLDER}/main/install/lib/libPiRootDict.rootmap")

def get_pdid_color_map():
    """
    returns a dictionary mapping particle ids used in pioneer to tuple for color and particle name
    """
    colormap = dict()
    colormap[-13] = ("magenta","antimuon")  #antimuon
    colormap[-11] =  ("orange","antielectron") #antielectron
    colormap[11] = ("blue","electron") #electron
    colormap[211] = ("green","pion+")  #pion +
    colormap[2212] =  ("red","proton")   #proton
    return colormap

def get_outline_histo(data,bincount,weights =None,smooth=False):
    """
    create outline histogram from data with weights and possible smoothing
    returns bin_edges,counts,sum of the counts
    bin_edges,counts are plottable such that for each bin bin_edges contains start and end of the bin -> except start,end each value is double
    and corresponding counts is the same
    """
    counts, bin_edges = np.histogram(data, bins=bincount,weights=weights)
    bin_center = (bin_edges[1:]+ bin_edges[:-1])/2
    if smooth:
        smoothed = savgol_filter(counts, window_length=5, polyorder=2)
        return bin_center,smoothed,np.sum(smoothed)
    count_sum = np.sum(counts)
    counts = np.repeat(counts, 2)
    bin_edges = np.repeat(bin_edges,2)[1:-1]
    return bin_edges,counts,count_sum

def get_outline_histo2d(xdata,ydata,xbins,ybins,weights=None):
    """
    create 2d histogram data
    returns data ready to be plot with meshgrid + pcolormes
    """
    counts, xedges, yedges = np.histogram2d(xdata, ydata, bins=[xbins, ybins],weights=None)
    counts = counts.T #account for quirk of above func

    total_sum = np.sum(counts)
    return xedges,yedges,counts,total_sum

def glue_dict(list,keys):
    return {key:e for key,e in zip(keys,list)}

def extract_from_dict(dict, keys):
    result = [dict[key] for key in keys]
    return result

NUMPY_FOLDER = "numpy_folder"
def load_data_from_numpy_file(filename,folder=NUMPY_FOLDER):
    """
    checks if file exists, if so returns the data
    """
    filepath = f"{folder}/{filename}.npz"
    if os.path.exists(filepath):
        data = np.load(filepath)
        return data
    return None

def save_data_to_numpy_file(data,keys,filename,folder=NUMPY_FOLDER):
    if not os.path.exists(folder):  # Check if folder exists
        os.makedirs(folder) 
    filepath = f"{folder}/{filename}.npz"
    np.savez(filepath, **glue_dict(data,keys))


### collection data
def get_file_pattern(run_id,key="run", folder='output'):
    pattern = f'{key}{run_id:05d}-*.root'
    file_pattern = os.path.join(folder, pattern) 
    return file_pattern
def get_root_files(run_id,key="run", folder='output'):
    # Find all ROOT files in the folder matching the run ID
    pattern = get_file_pattern(run_id,key=key,folder=folder)
    return glob.glob(pattern)

def create_root_tchain(run_id,key="run",treename="sim"):
    """
    given run id, potential key and potential treename return a root.TChain instance with all corresponding runfiles
    """
    root_files = get_root_files(run_id,key=key)
    chain = ROOT.TChain(treename)  
    for file_name in root_files:
        chain.Add(file_name)
    return chain
#fitting cone
def cone_model(x, y, a, x0,y0,z0):
    return a * np.sqrt((x-x0)**2 + (y-y0)**2) + z0
def cone_fit_extract_angle(fitresult):
    """
    from fitresult from parameter "a" of the model return the coneopening in angle
    """
    return 90+np.arctan(fitresult.best_values['a'])/np.pi*180
def fit_cone(xpos,ypos,zpos,supposed_angle=40):
    """
    fits the data to a cone with symmetryaxis paralell to z axis,x,y fixed at 0,0
    "supposed_angle" : supposed opening in degrees of the cone
    """
    # setup model
    model = Model(cone_model, independent_vars=['x', 'y'])
    params = model.make_params(a=-np.tan(np.pi/2 - np.pi/180*supposed_angle), x0=0,y0=0,z0=0) 
    params['x0'].set(vary=False)
    params['y0'].set(vary=False)
    # fit the model
    result = model.fit(zpos, params, x=xpos, y=ypos)
    print(cone_fit_extract_angle(result))
    print(result.fit_report())
    return result



