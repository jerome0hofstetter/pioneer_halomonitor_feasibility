import ROOT

PIONEER_FOLDER = "PIONEER"
ROOT.gSystem.Load(f"{PIONEER_FOLDER}/main/install/lib/libPiRootDict.so")
ROOT.gSystem.Load(f"{PIONEER_FOLDER}/main/install/lib/libPiRootDict.rootmap")

def create_root_tchain(run_id,key="run",treename="sim"):
    """
    given run id, potential key and potential treename return a root.TChain instance with all corresponding runfiles
    """
    root_files = get_root_files(run_id,key=key)
    chain = ROOT.TChain(treename)  
    for file_name in root_files:
        chain.Add(file_name)
    return chain