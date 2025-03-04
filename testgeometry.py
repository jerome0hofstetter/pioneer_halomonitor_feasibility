import ROOT

geom = ROOT.TGeoManager("geom", "Test Geometry")

mat = ROOT.TGeoMaterial("Vacuum")
med = ROOT.TGeoMedium("Air", 1, mat)

shape = ROOT.TGeoPcon(0, 360, 4)
shape.DefineSection(0, 10, 5, 5)
shape.DefineSection(1, 5, 5, 7)
shape.DefineSection(2, 0, 6, 8)
shape.DefineSection(3, -5, 7, 7)

vol = ROOT.TGeoVolume("MyPcon", shape, med)
vol.SetLineColor(ROOT.kRed)

geom.SetTopVolume(vol)
geom.CloseGeometry()

ROOT.SetOwnership(geom, False)  # Prevent Python from deleting it

vol.Draw("ogl")  # OpenGL viewer

ROOT.gApplication.Run()  # Keep GUI alive
