import numpy as np

from utils_math import *
from plotting_helper import *


def get_hit_data(run_id,key="run"):
    # Initialize lists to store xpos, ypos, zpos values
    filename = f"default_test_{key}_{run_id:05d}"

    keys = ["x","y","z","id"]
    data_list=[[] for i in range(4)]

    data = load_data_from_numpy_file(filename)
    if data:
        data_list = extract_from_dict(data,keys)
        return data_list

    print("generating numpy array from root files")
    
    from utils_root import create_root_tchain
    chain = create_root_tchain(run_id,key=key)
    xpos,ypos,zpos,id = data_list
    for entry in chain:
        for hit in entry.upstream:
            if hit.GetUpstreamID()==600_000:
                xpos.extend(hit.GetXpos())
                ypos.extend(hit.GetYpos())
                zpos.extend(hit.GetZpos())
                id.extend(hit.GetPDGID())

    data_list = [np.array(col) for col in data_list]
    save_data_to_numpy_file(data_list,keys,filename)
    return data_list



xpos,ypos,zpos,id= get_hit_data(2)


#result = fit_cone(xpos,ypos,zpos)
result=None
#plot_rough_3d(xpos,ypos,zpos,result)
show_3d = False
plot_with_filter(xpos,ypos,zpos,id,True,show_3d)
#plot_by_radius_corrected(xpos,ypos,zpos,id)
