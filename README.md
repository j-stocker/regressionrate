Here’s a well-structured `README.md` for your GitHub project that explains what it does, how it works, and how users can run it:

---

# 🟡 Regression Rate Analyzer from VisIt `.xyz` Export

This project automates the visualization and analysis of regression (burn) rates using data exported from [VisIt](https://wci.llnl.gov/simulation/computer-codes/visit), a powerful open-source visualization tool. The code generates contour plots of a scalar field (`eta`) and calculates how far it propagates over time to compute **instantaneous** and **average regression rates**.

---

## 📌 Features

* 📈 **Contour Visualization**: Configures a multi-colored discrete contour plot of the `eta` field in VisIt.
* 💾 **Data Export**: Exports `.xyz` files for each timestep with time-tagged filenames.
* 📊 **Post-Processing**: Extracts spatial coordinate data (`x`) from `.xyz` files.
* 🔥 **Regression Rate Calculation**:

  * Computes maximum and average `x` positions over time.
  * Derives instantaneous regression rates using finite difference.
  * Calculates overall average burn rates (max and average-based).

---

## 🧠 How It Works

### 1. **Visualization Setup in VisIt**

A custom color palette is created with 30 discrete control points to visualize the `eta` field as a contour plot. For each timestep in the time slider:

* The contour plot is updated.
* The `eta` field is exported as an `.xyz` file.

### 2. **Data Extraction**

From each `.xyz` file:

* The **second column** (representing `x` coordinates) is extracted.
* For each file, it computes:

  * Maximum `x` position
  * Average `x` position

These are saved to `results.txt`.

### 3. **Regression Rate Computation**

Using `results.txt`:

* Instantaneous burn rate is calculated via forward difference.
* Overall average burn rate is calculated from first and last data points.

All results are saved to `burn_rates.txt`.

---

## 📂 Project Structure

```
├── eta_coords/              # Exported XYZ files (one per time step)
├── results.txt              # Time vs Max/Avg X values
├── burn_rates.txt           # Final regression rate results
├── export_eta_data.py       # VisIt script to generate plots & export data
├── analyze_regression.py    # Python script for post-processing
└── README.md
```

---

## 🛠 Requirements

* **VisIt** (for plot generation and export)
* **Python 3.6+**

  * No external libraries required (only uses `os` and `csv`)

---

## ▶️ How to Run

### Step 1: Export `.xyz` files from VisIt

Run the VisIt script (`export_eta_data.py`) from within the VisIt GUI or CLI.

This script:

* Adds a contour plot of the `eta` variable
* Applies a custom discrete color palette
* Iterates over all timesteps
* Exports `.xyz` files into `./eta_coords/`

### Step 2: Run the analysis

Once `.xyz` files are generated:

```bash
python analyze_regression.py
```

This will:

* Generate `results.txt` (max/avg x positions over time)
* Generate `burn_rates.txt` with burn rate calculations

---

## 📄 Output Files

### `results.txt`

| Time     | Max_X     | Avg_X     |
| -------- | --------- | --------- |
| 0.000000 | 0.0234254 | 0.0123456 |
| 0.050000 | 0.0468910 | 0.0267891 |
| ...      | ...       | ...       |

### `burn_rates.txt`

```
Overall Average Burn Rate (Avg X): 0.0145678900
Overall Average Burn Rate (Max X): 0.0298765400
Time, Instantaneous_Burn_Rate
0.050000, 0.0345678900
0.100000, 0.0283456000
...
```
