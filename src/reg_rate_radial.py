#!/usr/bin/env python

import os
import csv
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <data_directory>")
    sys.exit(1)

datadir = sys.argv[1]
output_file = "results.txt"

#assumes centered on x/y axes, change to wherever your origin is locatied
central_x_coord = 0
central_y_coord = 0

#functions similar to reg_rate.py, but for circular 2D regression


def extract_second_column(filename):
    '''Extracts second column (x coords) from XYZ file'''
    second_column_values = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("UNKNOWN_ATOMIC_ELEMENT"):
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        value = float(parts[1])
                        second_column_values.append(value)
                    except ValueError:
                        continue  # Skip lines with invalid float conversion

    return second_column_values

def extract_third_column(filename):
    '''Extracts third column (y values) from XYZ file'''
    third_column_values = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("UNKNOWN_ATOMIC_ELEMENT"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        value = float(parts[2])
                        third_column_values.append(value)
                    except ValueError:
                        continue  # Skip lines with invalid float conversion

    return third_column_values


def append_result_to_file(time, max_val, avg_val, output_filename):
    """Append the time, max r, and avg r to a results file."""
    with open(output_filename, 'a') as f:
        f.write(f"{time:.6f}, {max_val:.10f}, {avg_val:.10f}\n")


# Get list of XYZ files
files = sorted([
    f for f in os.listdir(datadir)
    if os.path.isfile(os.path.join(datadir, f)) and f.endswith(".xyz")
])

# Clear output file at start
with open(output_file, 'w') as f:
    f.write("Time, Max_r, Avg_r\n")

# Loop over each file
for filename in files:
    filepath = os.path.join(datadir, filename)

    # Try to extract time from filename, e.g., "eta_coords_005_t0.123456.xyz"
    try:
        #extract part after eta_coords_ and before .xyz
        time_part = filename.replace("eta_coords_","").replace(".xyz","")
        time_val = float(time_part)
    except ValueError:
        print(f"Warning: could not extract time from filename: {filename}")
        continue

    # Extract x and y values (second and third column)
    x_data = extract_second_column(filepath)
    y_data = extract_third_column(filepath)
    r_data = []

    if not x_data or not y_data:
        print(f"Warning: No data in file: {filename}")
        continue
    
    r_data = [(x**2 + y**2)**(1/2) for x, y in zip(x_data, y_data)]

    max_r = max(r_data)
    avg_r = sum(r_data) / len(r_data)

    # Append result
    append_result_to_file(time_val, max_r, avg_r, output_file)
#THIS ALL WORKS!!

#make a plot of all the contours 
def extract_xy_coords(filename):
    '''Extracts x and y coords from XYZ file and calculates r'''
    x_coords = []
    y_coords = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("UNKNOWN_ATOMIC_ELEMENT"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        x_coords.append(x)
                        y_coords.append(y)
                        
                    except ValueError:
                        continue  # Skip lines with invalid float conversion
    return x_coords, y_coords


def contour_plot():
    plt.figure(figsize=(10, 6))
    '''pul data from eta_coords (first and second column for x and y)'''

    times_for_color = [] #use to make contour gradient
    xy_data_list = [] #for plotting later

    for filename in files:
        filepath = os.path.join(datadir, filename)
        #get time from filename for labeling
        try:
            time_part = filename.replace("eta_coords_","").replace(".xyz","")
            time_val = float(time_part)
        except ValueError:
            print(f"Warning: could not extract time from filename: {filename}")
            continue
        x_data, y_data = extract_xy_coords(filepath)
        if x_data and y_data:
            times_for_color.append(time_val)
            xy_data_list.append((x_data, y_data))  
    norm = plt.Normalize(min(times_for_color), max(times_for_color))
    cmap = plt.get_cmap('viridis')
    for (x_data, y_data), time_val in zip(xy_data_list, times_for_color):
        color = cmap(norm(time_val))
        plt.scatter(x_data, y_data, color=cmap(norm(time_val)), alpha=0.6, s=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    plt.colorbar(sm, label='Time')
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Contour Plot of All Time Steps")
    plt.grid(True)
    plt.savefig("contour_plot.png")
    plt.show() #if you don't want to see it, comment this out

def contourf_plot():
    plt.figure(figsize=(10, 6))

    all_x = []
    all_y = []
    all_t = []

    for filename in files:
        filepath = os.path.join(datadir, filename)

        # extract time from filename
        try:
            time_part = filename.replace("eta_coords_", "").replace(".xyz", "")
            time_val = float(time_part)
        except ValueError:
            print(f"Warning: could not extract time from filename: {filename}")
            continue

        x_data, y_data = extract_xy_coords(filepath)

        if x_data is None or y_data is None:
            continue
        if len(x_data) == 0:
            continue

        all_x.extend(x_data)
        all_y.extend(y_data)
        all_t.extend([time_val] * len(x_data))

    if len(all_x) == 0:
        raise RuntimeError("No valid data found for contour plot.")

    # convert to numpy arrays
    all_x = np.asarray(all_x)
    all_y = np.asarray(all_y)
    all_t = np.asarray(all_t)

    # remove duplicate (x, y) points
    pts = np.column_stack((all_x, all_y))
    pts_unique, idx = np.unique(pts, axis=0, return_index=True)
    all_x = pts_unique[:, 0]
    all_y = pts_unique[:, 1]
    all_t = all_t[idx]

    # create grid
    xi = np.linspace(all_x.min(), all_x.max(), 400)
    yi = np.linspace(all_y.min(), all_y.max(), 400)
    Xi, Yi = np.meshgrid(xi, yi)

    # interpolate time onto grid
    Ti = griddata(
        points=(all_x, all_y),
        values=all_t,
        xi=(Xi, Yi),
        method="linear"
    )

    # fallback for NaNs (very common)
    if np.isnan(Ti).any():
        Ti_nearest = griddata(
            points=(all_x, all_y),
            values=all_t,
            xi=(Xi, Yi),
            method="nearest"
        )
        Ti = np.where(np.isnan(Ti), Ti_nearest, Ti)

    # contour plot
    contour = plt.contourf(Xi, Yi, Ti, levels=100, cmap="plasma")
    plt.colorbar(contour, label="Time")

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Contour Plot of All Time Steps")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("contour_plot.png", dpi=300)
    plt.show()        

#now need to read results to calculate regression rate
#using:
#overall average x over time
#max x over time
#forward-backward difference
#make a new file to save results
#read results file
def read_results_file(filename):
    """Reads the results file and returns lists of times, max_r, and avg_r."""
    times = []
    max_rs = []
    avg_rs = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 3:
                try:
                    times.append(float(row[0]))
                    max_rs.append(float(row[1]))
                    avg_rs.append(float(row[2]))
                except ValueError:
                    continue  # Skip rows with invalid float conversion
    return times, max_rs, avg_rs


def calc_reg_rate(times, max_r, avg_r):
    #instantaneous regression rate at each time, furthest r 
    #forward difference
    inst_burn_rates = []

    N = len(times)
    for i in range(N):
        if i == 0: #forward dif at beginning
            dt = times[i+1] - times[i]
            dr_max = max_r[i+1] - max_r[i]
        elif i == N-1: #backward dif at end
            dt = times[i] - times[i-1]
            dr_max = max_r[i] - max_r[i-1]
        else: #central dif in the middle
            dt = times[i+1] - times[i-1]
            dr_max = max_r[i+1] - max_r[i-1]
        burn_rate = dr_max / dt
        inst_burn_rates.append((times[i], burn_rate))

    #average burn rate, overall
    total_time = times[-1] - times[0]
    avg_burn_avg = (avg_r[-1] - avg_r[0]) / (total_time)
    #average burn rate, furthest x coord
    avg_burn_max = (max_r[-1] - max_r[0]) / (total_time)

    return inst_burn_rates, avg_burn_avg, avg_burn_max


def save_burn_rates(inst_burn_rates, avg_burn_avg, avg_burn_max, filename):
    with open(filename, 'w') as f:
        f.write(f"\nOverall Average Burn Rate (Avg R): {avg_burn_avg:.10f}\n")
        f.write(f"Overall Average Burn Rate (Max R): {avg_burn_max:.10f}\n")
        f.write("Time, Instantaneous_Burn_Rate\n")
        for time, rate in inst_burn_rates:
            f.write(f"{time:.6f}, {rate:.10f}\n")

def plot_burn_rates(inst_burn_rates, avg_burn_avg, avg_burn_max, output_image='burn_rate_plot.png'):
    times = [t for t, _ in inst_burn_rates]
    rates = [r for _, r in inst_burn_rates]

    plt.figure(figsize=(10, 6))
    plt.plot(times, rates, label="Instantaneous Burn Rate", marker='o', linestyle='-', color='blue')

    # Add average lines
    plt.axhline(avg_burn_avg, color='green', linestyle='--', label=f"Avg Burn Rate (Avg R): {avg_burn_avg:.4f}")
    plt.axhline(avg_burn_max, color='red', linestyle='--', label=f"Avg Burn Rate (Max R): {avg_burn_max:.4f}")

    plt.xlabel("Time")
    plt.ylabel("Burn Rate (dr/dt)")
    plt.title("Regression (Burn) Rate Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_image)
    plt.show() #if you don't want to see it, comment this out



def main():
    results_file = "results.txt"
    burn_output_file = "burn_rates.txt"
    burn_rate_plot_file = "burn_rate_plot.png"
    contour_plot_file = "contour_plot.png"
    times, max_r, avg_r = read_results_file(results_file)

    inst_rates, avg_burn_avg, avg_burn_max = calc_reg_rate(times, max_r, avg_r)
    save_burn_rates(inst_rates, avg_burn_avg, avg_burn_max, burn_output_file)
    plot_burn_rates(inst_rates, avg_burn_avg, avg_burn_max)
    contourf_plot()

    print(f"Results saved to {results_file} and {burn_output_file}")
    print(f"Burn rate plot saved as {burn_rate_plot_file}")
    print(f"Contour plot saved as {contour_plot_file}")



if __name__ == '__main__':
    main()
