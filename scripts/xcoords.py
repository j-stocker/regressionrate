import os
import sys
#make folder for x coords

default_db = "celloutput.visit"

if len(sys.argv) > 1:
    db_path = sys.argv[1]
    if not db_path.endswith(default_db):
        db_path = os.path.join(db_path, default_db)
else:
    db_path = os.path.join(os.getcwd(), default_db)

db_path = os.path.abspath(db_path)

if not os.path.exists(db_path):
    print("ERROR: Could not find celloutput.visit at:")
    print("   " + db_path)
    sys.exit(1)

print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

datadir = "./eta_coords"
if not os.path.exists(datadir):
    os.makedirs(datadir)

min_temp = 300 #change as desired

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
ThresholdAtts.lowerBounds = (-1e+37, min_temp)
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

sys.exit(0)