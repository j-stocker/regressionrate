import os
import csv
import matplotlib.pyplot as plt

datadir = "./eta_coords"
output_file = "results.txt"

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


def append_result_to_file(time, max_val, avg_val, output_filename):
    """Append the time, max X, and avg X to a results file."""
    with open(output_filename, 'a') as f:
        f.write(f"{time:.6f}, {max_val:.10f}, {avg_val:.10f}\n")


# Get list of XYZ files
files = sorted([
    f for f in os.listdir(datadir)
    if os.path.isfile(os.path.join(datadir, f)) and f.endswith(".xyz")
])

# Clear output file at start
with open(output_file, 'w') as f:
    f.write("Time, Max_X, Avg_X\n")

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

    # Extract X coordinates (second column)
    x_data = extract_second_column(filepath)
    if not x_data:
        print(f"Warning: No data in file: {filename}")
        continue

    max_x = max(x_data)
    avg_x = sum(x_data) / len(x_data)

    # Append result
    append_result_to_file(time_val, max_x, avg_x, output_file)
#THIS ALL WORKS!!

#now need to read results to calculate regression rate
#using:
#overall average x over time
#max x over time
#forward-backward difference
#make a new file to save results
#read results file
def read_results_file(filename):
    """Reads the results file and returns lists of times, max_x, and avg_x."""
    times = []
    max_xs = []
    avg_xs = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) == 3:
                try:
                    times.append(float(row[0]))
                    max_xs.append(float(row[1]))
                    avg_xs.append(float(row[2]))
                except ValueError:
                    continue  # Skip rows with invalid float conversion
    return times, max_xs, avg_xs


def calc_reg_rate(times, max_x, avg_x):
    #instantaneous regression rate at each time, furthest x coord
    inst_burn_rates = []

    for i in range(1, len(times)):
        dt = times[i] - times[i-1]
        dx_max = max_x[i] - max_x[i-1]
        if dt != 0:
            burn_rate = dx_max / dt
            inst_burn_rates.append((times[i], burn_rate))

    #average burn rate, overall
    total_time = times[-1] - times[0]
    avg_burn_avg = (avg_x[-1] - avg_x[0]) / (total_time)
    #average burn rate, furthest x coord
    avg_burn_max = (max_x[-1] - max_x[0]) / (total_time)

    return inst_burn_rates, avg_burn_avg, avg_burn_max


def save_burn_rates(inst_burn_rates, avg_burn_avg, avg_burn_max, filename):
    with open(filename, 'w') as f:
        f.write(f"\nOverall Average Burn Rate (Avg X): {avg_burn_avg:.10f}\n")
        f.write(f"Overall Average Burn Rate (Max X): {avg_burn_max:.10f}\n")
        f.write("Time, Instantaneous_Burn_Rate\n")
        for time, rate in inst_burn_rates:
            f.write(f"{time:.6f}, {rate:.10f}\n")

def plot_burn_rates(inst_burn_rates, avg_burn_avg, avg_burn_max, output_image='burn_rate_plot.png'):
    times = [t for t, _ in inst_burn_rates]
    rates = [r for _, r in inst_burn_rates]

    plt.figure(figsize=(10, 6))
    plt.plot(times, rates, label="Instantaneous Burn Rate", marker='o', linestyle='-', color='blue')

    # Add average lines
    plt.axhline(avg_burn_avg, color='green', linestyle='--', label=f"Avg Burn Rate (Avg X): {avg_burn_avg:.4f}")
    plt.axhline(avg_burn_max, color='red', linestyle='--', label=f"Avg Burn Rate (Max X): {avg_burn_max:.4f}")

    plt.xlabel("Time")
    plt.ylabel("Burn Rate (dx/dt)")
    plt.title("Regression (Burn) Rate Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_image)
    plt.show()



def main():
    results_file = "results.txt"
    burn_output_file = "burn_rates.txt"
    times, max_x, avg_x = read_results_file(results_file)

    inst_rates, avg_burn_avg, avg_burn_max = calc_reg_rate(times, max_x, avg_x)
    save_burn_rates(inst_rates, avg_burn_max, avg_burn_avg, burn_output_file)
    plot_burn_rates(inst_rates, avg_burn_avg, avg_burn_max)

    print(f"Results saved to {results_file} and {burn_output_file}")
    print(f"Burn rate plot saved as 'burn_rate_plot.png'")


if __name__ == '__main__':
    main()
