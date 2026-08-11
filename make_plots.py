#!/usr/bin/env python3

import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

RESULTS_FILENAME = "results.txt"

POSITION_PLOT_FILENAME = "combined_position_vs_time.pdf"
BURN_RATE_PLOT_FILENAME = "combined_burn_rate_vs_time.pdf"


# ============================================================
# SAMPLE COLORS
# ============================================================

SAMPLE_COLORS = {
    "A": "#4169E1",   # Blue
    "H": "#FFAE42",   # Orange
    "S": "#DC143C",   # Red
}


# ============================================================
# PRESSURE LINE STYLES
# ============================================================

PRESSURE_STYLES = {
    "1 MPa": "-",
    "7 MPa": "--",
}


# ============================================================
# PRESSURE OPACITY
# ============================================================

PRESSURE_ALPHA = {
    "1 MPa": 1.0,
    "7 MPa": 0.45,
}


# ============================================================
# IDENTIFY SAMPLE
# ============================================================

def identify_sample(folder_name):
    """
    Identify sample A, H, or S from the folder name.

    Examples:

        A_1MPa
        H_7MPa
        S_1MPa
        Sample_A_1MPa
        test-H-7MPa
    """

    name = folder_name.upper()

    for sample in ["A", "H", "S"]:

        if (
            name == sample
            or name.startswith(sample + "_")
            or name.endswith("_" + sample)
            or f"_{sample}_" in name
            or f"-{sample}-" in name
            or f"-{sample}_" in name
            or f"_{sample}-" in name
        ):
            return sample

    # Fallback
    for sample in ["A", "H", "S"]:

        if sample in name:
            return sample

    return None


# ============================================================
# IDENTIFY PRESSURE
# ============================================================

def identify_pressure(folder_name):
    """
    Identify whether the folder corresponds to
    1 MPa or 7 MPa.
    """

    name = (
        folder_name
        .upper()
        .replace(" ", "")
        .replace("_", "")
    )

    if "1MPA" in name:
        return "1 MPa"

    if "7MPA" in name:
        return "7 MPa"

    return None


# ============================================================
# FIND EXPERIMENT FOLDERS
# ============================================================

def find_experiment_folders(parent_directory):
    """
    Search through all folders underneath the parent directory.

    A folder is considered an experiment folder if it contains
    results.txt and its name identifies both:

        Sample: A, H, or S
        Pressure: 1 MPa or 7 MPa
    """

    experiments = []

    for root, dirs, files in os.walk(parent_directory):

        # Only consider folders containing results.txt
        if RESULTS_FILENAME not in files:
            continue

        folder_name = os.path.basename(root)

        sample = identify_sample(folder_name)
        pressure = identify_pressure(folder_name)

        if sample is None:

            print(
                f"WARNING: Could not identify sample "
                f"in folder: {root}"
            )

            continue

        if pressure is None:

            print(
                f"WARNING: Could not identify pressure "
                f"in folder: {root}"
            )

            continue

        results_file = os.path.join(
            root,
            RESULTS_FILENAME
        )

        experiments.append({
            "folder": root,
            "folder_name": folder_name,
            "sample": sample,
            "pressure": pressure,
            "results_file": results_file,
        })

    return experiments


# ============================================================
# READ RESULTS.TXT
# ============================================================

def read_results_file(filename):
    """
    Reads results.txt.

    Expected format:

        Time, Max_X, Avg_X
        0.000000, ...
        0.010000, ...
        0.020000, ...

    Returns:

        times
        max_x
        avg_x
    """

    times = []
    max_xs = []
    avg_xs = []

    with open(filename, "r") as f:

        reader = csv.reader(f)

        # Skip header
        next(reader, None)

        for row in reader:

            if len(row) != 3:
                continue

            try:

                times.append(float(row[0]))
                max_xs.append(float(row[1]))
                avg_xs.append(float(row[2]))

            except ValueError:

                continue

    return (
        np.asarray(times, dtype=float),
        np.asarray(max_xs, dtype=float),
        np.asarray(avg_xs, dtype=float),
    )


# ============================================================
# CALCULATE INSTANTANEOUS BURN RATE
# ============================================================

def calculate_burn_rate(times, max_x):
    """
    Calculate instantaneous regression/burn rate:

        burn rate = d(Max X) / dt

    Uses:

        Forward difference at first point
        Central difference at interior points
        Backward difference at final point
    """

    if len(times) < 2:

        return (
            np.array([]),
            np.array([])
        )

    burn_rates = np.zeros(
        len(times)
    )

    # --------------------------------------------------------
    # First point: forward difference
    # --------------------------------------------------------

    dt = times[1] - times[0]

    if dt != 0:

        burn_rates[0] = (
            max_x[1] - max_x[0]
        ) / dt

    else:

        burn_rates[0] = np.nan

    # --------------------------------------------------------
    # Interior points: central difference
    # --------------------------------------------------------

    for i in range(
        1,
        len(times) - 1
    ):

        dt = (
            times[i + 1]
            - times[i - 1]
        )

        if dt != 0:

            burn_rates[i] = (
                max_x[i + 1]
                - max_x[i - 1]
            ) / dt

        else:

            burn_rates[i] = np.nan

    # --------------------------------------------------------
    # Last point: backward difference
    # --------------------------------------------------------

    dt = (
        times[-1]
        - times[-2]
    )

    if dt != 0:

        burn_rates[-1] = (
            max_x[-1]
            - max_x[-2]
        ) / dt

    else:

        burn_rates[-1] = np.nan

    return (
        times.copy(),
        burn_rates
    )


# ============================================================
# LOAD ALL EXPERIMENT DATA
# ============================================================

def load_experiment_data(experiments):

    loaded_data = []

    print()
    print("=" * 70)
    print("LOADING RESULTS")
    print("=" * 70)

    for exp in experiments:

        print()
        print(
            f"Reading: {exp['folder']}"
        )

        try:

            times, max_x, avg_x = (
                read_results_file(
                    exp["results_file"]
                )
            )

        except Exception as e:

            print(
                f"WARNING: Could not read "
                f"{exp['results_file']}"
            )

            print(
                f"         {e}"
            )

            continue

        if len(times) < 2:

            print(
                "WARNING: Not enough data."
            )

            continue

        # Calculate instantaneous burn rate
        burn_times, burn_rates = (
            calculate_burn_rate(
                times,
                max_x
            )
        )

        loaded_data.append({
            **exp,

            "times": times,

            # Position plot uses Maximum X
            "max_x": max_x,

            "avg_x": avg_x,

            "burn_times": burn_times,

            "burn_rates": burn_rates,
        })

    return loaded_data


# ============================================================
# MAKE POSITION PLOT
# ============================================================

def make_position_plot(
    data,
    output_file
):
    """
    Maximum X Position vs Simulation Time.

    Color:
        A = Blue
        H = Orange
        S = Red

    Line:
        1 MPa = solid
        7 MPa = dotted

    Opacity:
        1 MPa = 1.0
        7 MPa = 0.45

    IMPORTANT:
        The original position data are NOT modified.

        A single (0, 0) point is simply added to the
        beginning of each plotted curve.
    """

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    # Sort so plotting order is consistent
    data_sorted = sorted(
        data,
        key=lambda x: (
            x["sample"],
            x["pressure"]
        )
    )

    for exp in data_sorted:

        sample = exp["sample"]
        pressure = exp["pressure"]

        color = SAMPLE_COLORS[sample]

        linestyle = PRESSURE_STYLES[
            pressure
        ]

        alpha = PRESSURE_ALPHA[
            pressure
        ]

        label = (
            f"{sample} — {pressure}"
        )

        # ----------------------------------------------------
        # Add a single (0, 0) point.
        #
        # The original data are NOT shifted or subtracted.
        # ----------------------------------------------------

        plot_times = np.insert(
            exp["times"],
            0,
            0.0
        )

        plot_position = np.insert(
            exp["max_x"],
            0,
            0.0
        )

        ax.plot(
            plot_times,
            plot_position,

            color=color,

            linestyle=linestyle,

            linewidth=2.0,

            alpha=alpha,

            label=label,
        )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    ax.set_xlabel(
        "Time (s)",
        fontsize=13
    )

    ax.set_ylabel(
        "Position (mm)",
        fontsize=13
    )

    #ax.set_title(
    #    "Maximum Position vs. Simulation Time",
    #    fontsize=15
    #)

    # --------------------------------------------------------
    # Grid
    # --------------------------------------------------------

    ax.grid(
        True,
        alpha=0.3
    )

    # --------------------------------------------------------
    # Legend
    # --------------------------------------------------------

    ax.legend(
        fontsize=11,
        loc="best"
    )

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    fig.tight_layout()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print()
    print(
        f"Saved position plot:"
    )

    print(
        f"    {output_file}"
    )


# ============================================================
# MAKE BURN RATE PLOT
# ============================================================

def make_burn_rate_plot(
    data,
    output_file
):
    """
    Instantaneous Burn Rate vs Simulation Time.

    Color:
        A = Blue
        H = Orange
        S = Red

    Line:
        1 MPa = solid
        7 MPa = dotted

    Opacity:
        1 MPa = 1.0
        7 MPa = 0.45
    """

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    # Sort so plotting order is consistent
    data_sorted = sorted(
        data,
        key=lambda x: (
            x["sample"],
            x["pressure"]
        )
    )

    for exp in data_sorted:

        sample = exp["sample"]
        pressure = exp["pressure"]

        color = SAMPLE_COLORS[sample]

        linestyle = PRESSURE_STYLES[
            pressure
        ]

        alpha = PRESSURE_ALPHA[
            pressure
        ]

        label = (
            f"{sample} — {pressure}"
        )

        ax.plot(
            exp["burn_times"],
            exp["burn_rates"],

            color=color,

            linestyle=linestyle,

            linewidth=2.0,

            alpha=alpha,

            label=label,
        )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    ax.set_xlabel(
        "Time (s)",
        fontsize=13
    )

    ax.set_ylabel(
        "Instantaneous Burn Rate (mm/s)",
        fontsize=13
    )

    #ax.set_title(
    #    "Instantaneous Burn Rate vs. Simulation Time",
    #    fontsize=15
    #)

    # --------------------------------------------------------
    # Grid
    # --------------------------------------------------------

    ax.grid(
        True,
        alpha=0.3
    )

    # --------------------------------------------------------
    # Legend
    # --------------------------------------------------------

    ax.legend(
        fontsize=11,
        loc="best"
    )

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    fig.tight_layout()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print()
    print(
        f"Saved burn-rate plot:"
    )

    print(
        f"    {output_file}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Get parent directory
    # --------------------------------------------------------

    if len(sys.argv) > 1:

        parent_directory = os.path.abspath(
            sys.argv[1]
        )

    else:

        parent_directory = os.getcwd()

    # --------------------------------------------------------
    # Check directory
    # --------------------------------------------------------

    if not os.path.isdir(
        parent_directory
    ):

        print(
            "ERROR: Directory does not exist:"
        )

        print(
            f"    {parent_directory}"
        )

        sys.exit(1)

    print()
    print("=" * 70)
    print("COMBINED PLOT GENERATOR")
    print("=" * 70)

    print()
    print(
        f"Parent directory:"
    )

    print(
        f"    {parent_directory}"
    )

    # --------------------------------------------------------
    # Find experiments
    # --------------------------------------------------------

    experiments = (
        find_experiment_folders(
            parent_directory
        )
    )

    if len(experiments) == 0:

        print()
        print(
            "ERROR: No experiment folders found."
        )

        print()
        print(
            "Each experiment folder must contain:"
        )

        print(
            "    results.txt"
        )

        sys.exit(1)

    print()
    print(
        f"Found {len(experiments)} "
        f"experiment folders:"
    )

    for exp in experiments:

        print(
            f"    {exp['sample']} | "
            f"{exp['pressure']} | "
            f"{exp['folder']}"
        )

    # --------------------------------------------------------
    # Load results
    # --------------------------------------------------------

    data = load_experiment_data(
        experiments
    )

    if len(data) == 0:

        print()
        print(
            "ERROR: No valid data found."
        )

        sys.exit(1)

    print()
    print(
        f"Successfully loaded "
        f"{len(data)} experiment(s)."
    )

    # --------------------------------------------------------
    # Output filenames
    # --------------------------------------------------------

    position_output = os.path.join(
        parent_directory,
        POSITION_PLOT_FILENAME
    )

    burn_rate_output = os.path.join(
        parent_directory,
        BURN_RATE_PLOT_FILENAME
    )

    # --------------------------------------------------------
    # Create position plot
    # --------------------------------------------------------

    make_position_plot(
        data,
        position_output
    )

    # --------------------------------------------------------
    # Create burn-rate plot
    # --------------------------------------------------------

    make_burn_rate_plot(
        data,
        burn_rate_output
    )

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)

    print()
    print(
        "Plots created:"
    )

    print(
        f"    {position_output}"
    )

    print(
        f"    {burn_rate_output}"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()


