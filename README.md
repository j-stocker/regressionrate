
# Regression Rate Analyzer from VisIt `.xyz` Export

This project automates the visualization and analysis of regression (burn) rates using data exported from VisIt. The code generates contour plots of a scalar field (`eta`) and calculates how far it propagates over time to compute **instantaneous** and **average regression rates**.

---

## How It Works

### 1. **Visualization Setup in VisIt**

A contour plot of the surface where eta = 0.5 is created and visualized.

### 2. **Data Extraction**

A .xyz file is created for each time step with coordinates of the created contour.
From each `.xyz` file:

* The **second column** (representing `x` coordinates) is extracted.
* For each file, it computes:

  * Maximum `x` position
  * Average `x` position

These are saved to `results.txt`.

### 3. **Regression Rate Computation**

Using `results.txt`:

* Instantaneous burn rate is calculated via central difference.
* Overall average burn rate is calculated from first and last data points.
* The average burn rate of the furthest x coordinate is calculated from first and last data points.

All results are saved to `burn_rates.txt`.

---

## Project Structure

```
├── eta_coords/              # Exported XYZ files (one per time step)
├── results.txt              # Time vs Max/Avg X values
├── burn_rates.txt           # Final regression rate results
├── export_eta_data.py       # VisIt script to generate plots & export data
├── analyze_regression.py    # Python script for post-processing
└── README.md
```

---

## How to Run

### Step 1: Export `.xyz` files from VisIt

Run the VisIt script (`xcoords.py`) from within the VisIt GUI or CLI.
(Copy and paste into the Command window.)

This script:

* Adds a contour plot of the `eta` variable
* Iterates over all timesteps
* Exports `.xyz` files into a folder `./eta_coords/`

### Step 2: Run the analysis

Once `.xyz` files are generated:

```bash
python reg_rate.py OR reg_rate_radial.py
```

This will:

* Generate `results.txt` (max/avg x or r positions over time)
* Generate `burn_rates.txt` with burn rate calculations
* Use reg_rate.py for standard x-y coordinate systems (burning left to right)
* Use reg_rate_radial.py for conversion into r distance from center

---

## Output Files

results.txt will be saved to the data directory variable at the top of the xcoords.py script. burn_rates.txt and the corresponding plot will be saved similarly, with the variable at the top of reg_rates.py.

The plot will be displayed upon running reg_rate.py. Once the plot is closed, messages will display the names of the output files. To disable this and just show the end message, comment out "plt.show()" in line 141.

### `results.txt`

| Time     | Max_X/R        | Avg_X/R        |
| -------- | ------------   | ------------   |
| 0.000000 | 0.0286306944   | 0.0095451160   |
| 0.020000 | 0.0426500291   | 0.0156722070   |
| ...      | ...            | ...            |

### `burn_rates.txt`

```
Overall Average Burn Rate (Avg X/R): 1.1964434558
Overall Average Burn Rate (Max X)/R: 0.6944771942
Time, Instantaneous_Burn_Rate
0.020000, 1.4019334700
0.030000, 1.2567777100
...
```
