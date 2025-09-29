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
ContourAtts.defaultPalette.SetNumControlPoints(30)
ContourAtts.defaultPalette.GetControlPoints(0).colors = (255, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(0).position = 0
ContourAtts.defaultPalette.GetControlPoints(1).colors = (0, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(1).position = 0.034
ContourAtts.defaultPalette.GetControlPoints(2).colors = (0, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(2).position = 0.069
ContourAtts.defaultPalette.GetControlPoints(3).colors = (0, 255, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(3).position = 0.103
ContourAtts.defaultPalette.GetControlPoints(4).colors = (255, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(4).position = 0.138
ContourAtts.defaultPalette.GetControlPoints(5).colors = (255, 255, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(5).position = 0.172
ContourAtts.defaultPalette.GetControlPoints(6).colors = (255, 135, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(6).position = 0.207
ContourAtts.defaultPalette.GetControlPoints(7).colors = (255, 0, 135, 255)
ContourAtts.defaultPalette.GetControlPoints(7).position = 0.241
ContourAtts.defaultPalette.GetControlPoints(8).colors = (168, 168, 168, 255)
ContourAtts.defaultPalette.GetControlPoints(8).position = 0.276
ContourAtts.defaultPalette.GetControlPoints(9).colors = (255, 68, 68, 255)
ContourAtts.defaultPalette.GetControlPoints(9).position = 0.31
ContourAtts.defaultPalette.GetControlPoints(10).colors = (99, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(10).position = 0.345
ContourAtts.defaultPalette.GetControlPoints(11).colors = (99, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(11).position = 0.379
ContourAtts.defaultPalette.GetControlPoints(12).colors = (40, 165, 165, 255)
ContourAtts.defaultPalette.GetControlPoints(12).position = 0.414
ContourAtts.defaultPalette.GetControlPoints(13).colors = (255, 99, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(13).position = 0.448
ContourAtts.defaultPalette.GetControlPoints(14).colors = (255, 255, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(14).position = 0.483
ContourAtts.defaultPalette.GetControlPoints(15).colors = (255, 170, 99, 255)
ContourAtts.defaultPalette.GetControlPoints(15).position = 0.517
ContourAtts.defaultPalette.GetControlPoints(16).colors = (170, 79, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(16).position = 0.552
ContourAtts.defaultPalette.GetControlPoints(17).colors = (150, 0, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(17).position = 0.586
ContourAtts.defaultPalette.GetControlPoints(18).colors = (0, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(18).position = 0.621
ContourAtts.defaultPalette.GetControlPoints(19).colors = (0, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(19).position = 0.655
ContourAtts.defaultPalette.GetControlPoints(20).colors = (0, 109, 109, 255)
ContourAtts.defaultPalette.GetControlPoints(20).position = 0.69
ContourAtts.defaultPalette.GetControlPoints(21).colors = (150, 0, 150, 255)
ContourAtts.defaultPalette.GetControlPoints(21).position = 0.724
ContourAtts.defaultPalette.GetControlPoints(22).colors = (150, 150, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(22).position = 0.759
ContourAtts.defaultPalette.GetControlPoints(23).colors = (150, 84, 0, 255)
ContourAtts.defaultPalette.GetControlPoints(23).position = 0.793
ContourAtts.defaultPalette.GetControlPoints(24).colors = (160, 0, 79, 255)
ContourAtts.defaultPalette.GetControlPoints(24).position = 0.828
ContourAtts.defaultPalette.GetControlPoints(25).colors = (255, 104, 28, 255)
ContourAtts.defaultPalette.GetControlPoints(25).position = 0.862
ContourAtts.defaultPalette.GetControlPoints(26).colors = (0, 170, 81, 255)
ContourAtts.defaultPalette.GetControlPoints(26).position = 0.897
ContourAtts.defaultPalette.GetControlPoints(27).colors = (68, 255, 124, 255)
ContourAtts.defaultPalette.GetControlPoints(27).position = 0.931
ContourAtts.defaultPalette.GetControlPoints(28).colors = (0, 130, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(28).position = 0.966
ContourAtts.defaultPalette.GetControlPoints(29).colors = (130, 0, 255, 255)
ContourAtts.defaultPalette.GetControlPoints(29).position = 1
ContourAtts.defaultPalette.smoothing = ContourAtts.defaultPalette.NONE  # NONE, Linear, CubicSpline
ContourAtts.defaultPalette.equalSpacingFlag = 1
ContourAtts.defaultPalette.discreteFlag = 1
ContourAtts.defaultPalette.tagNames = ("Default", "Discrete")
ContourAtts.changedColors = ()
ContourAtts.colorType = ContourAtts.ColorByMultipleColors  # ColorBySingleColor, ColorByMultipleColors, ColorByColorTable
ContourAtts.colorTableName = "Default"
ContourAtts.invertColorTable = 0
ContourAtts.legendFlag = 1
ContourAtts.lineWidth = 0
ContourAtts.singleColor = (255, 0, 0, 255)
ContourAtts.contourMethod = ContourAtts.Value  # Level, Value, Percent
ContourAtts.contourNLevels = 10
ContourAtts.contourValue = (0.5)
ContourAtts.contourPercent = ()
ContourAtts.SetMultiColor(0, (255, 0, 0, 255))
ContourAtts.SetMultiColor(1, (0, 255, 0, 255))
ContourAtts.SetMultiColor(2, (0, 0, 255, 255))
ContourAtts.SetMultiColor(3, (0, 255, 255, 255))
ContourAtts.SetMultiColor(4, (255, 0, 255, 255))
ContourAtts.SetMultiColor(5, (255, 255, 0, 255))
ContourAtts.SetMultiColor(6, (255, 135, 0, 255))
ContourAtts.SetMultiColor(7, (255, 0, 135, 255))
ContourAtts.SetMultiColor(8, (168, 168, 168, 255))
ContourAtts.SetMultiColor(9, (255, 68, 68, 255))
ContourAtts.minFlag = 0
ContourAtts.maxFlag = 0
ContourAtts.min = 0
ContourAtts.max = 1
ContourAtts.scaling = ContourAtts.Linear  # Linear, Log
ContourAtts.wireframe = 0
SetPlotOptions(ContourAtts)
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

