import os
#make folder for x coords
datadir = "./eta_coords"
if not os.path.exists(datadir):
    os.makedirs(datadir)



for n in range(3):
    print('--------------------------------')

DeleteAllPlots()
AddPlot("Contour", "eta", 1, 1)
ContourAtts = ContourAttributes()
ContourAtts.contourValue = (0.5)
SetPlotOptions(ContourAtts)
AddOperator("Threshold", 1)
ThresholdAtts = ThresholdAttributes()
ThresholdAtts.listedVarNames = ("default", "temp")
ThresholdAtts.lowerBounds = (-1e+37, min_temp)\
ThresholdAtts.upperBounds = (1e+37, 1e+37)
DrawPlots()

    
nStates = TimeSliderGetNStates()
for i in range(nStates):
    #if i == 0:
    #    continue
    SetTimeSliderState(i)

    #get the time
    Query("Time")
    time = GetQueryOutputValue()
    #format time for filename
    time_str = f"{time:.3f}"
    e = ExportDBAttributes()
    e .allTimes = 0
    e.dirname =datadir
    e.filename = f"eta_coords_{time_str}"
    e.db_type = "XYZ"
    e.db_type_fullname = ""
    e.variables = ("eta",)
    ExportDatabase(e)

