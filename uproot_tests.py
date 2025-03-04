import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons,TextBox,Button
from mpl_toolkits.mplot3d import Axes3D
import glob
import os
import uproot
import awkward as ak

ROOT.gSystem.Load("/home/akumashisen/PIONEER/main/install/lib/libPiRootDict.so")
ROOT.gSystem.Load("/home/akumashisen/PIONEER/main/install/lib/libPiRootDict.rootmap")

##### nonfunctioning stuff
def create_root_dataframe(run_id):
    chain = create_root_tchain(run_id)
    df = ROOT.RDataFrame(chain)
    return df
def create_uproot_chain(run_id,treename="sim"):
    root_files = get_root_files(run_id)
    chain = uproot.concatenate(get_file_pattern(run_id))

def roughplot_with_uproot(run_id):
    chain = create_uproot_chain(run_id)
    xpos = chain["upstream.xpos"]  
    ypos = chain["upstream.ypos"]
    zpos = chain["upstream.zpos"]

    xpos = np.hstack(xpos)
    ypos = np.hstack(ypos)
    zpos = np.hstack(zpos)
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xpos, ypos, zpos, c='r', marker='o')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')

    ax.set_title('Detector Positions in 3D Space')
    plt.show()
####### end of nonfunctioning stuff