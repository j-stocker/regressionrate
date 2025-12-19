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
visit
print(f"Opening database: {db_path}")
OpenDatabase(db_path, 0)

datadir = "./eta_coords"
if not os.path.exists(datadir):
    os.makedirs(datadir)

min_temp = 400.0 #change as desired

for n in range(3):
    print('--------------------------------')

DeleteAllPlots()

# Add contour plot
AddPlot("Contour", "eta", 1, 1)
ContourAtts = ContourAttributes()
ContourAtts.contourMethod = ContourAtts.Value  # Explicitly set method
ContourAtts.contourValue = (0.5,)  # Must be a tuple with trailing comma
ContourAtts.minFlag = 0
ContourAtts.maxFlag = 0
SetPlotOptions(ContourAtts)

# Add threshold operator
AddOperator("Threshold", 1)
ThresholdAtts = ThresholdAttributes()
ThresholdAtts.outputMeshType = 0  # 0 for original mesh type
ThresholdAtts.listedVarNames = ("temp",)  # Only list the variable you're thresholding
ThresholdAtts.lowerBounds = (min_temp,)  # Must be tuple
ThresholdAtts.upperBounds = (1e+37,)  # Must be tuple
ThresholdAtts.zonePortions = (1,)  # Include zones where condition is met
SetOperatorOptions(ThresholdAtts, 1)

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