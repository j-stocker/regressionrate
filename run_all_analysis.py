#!/usr/bin/env python3

import os
import sys
import subprocess


# ============================================================
# SETTINGS
# ============================================================

# Your existing scripts
EXPORT_SCRIPT = "export_eta_coords.py"
BURN_RATE_SCRIPT = "burn_rate_analysis.py"

# VisIt command
# Change this if your VisIt executable has a different name/path.
VISIT_COMMAND = "visit"

# Database name inside each simulation folder
DATABASE_NAME = "celloutput.visit"


# ============================================================
# FIND SIMULATION FOLDERS
# ============================================================

def find_simulation_folders(parent_directory):

    simulation_folders = []

    for item in sorted(os.listdir(parent_directory)):

        full_path = os.path.join(
            parent_directory,
            item
        )

        # Only look at directories
        if not os.path.isdir(full_path):
            continue

        # Must contain celloutput.visit
        database = os.path.join(
            full_path,
            DATABASE_NAME
        )

        if not os.path.isfile(database):
            continue

        simulation_folders.append(full_path)

    return simulation_folders


# ============================================================
# RUN VISIT
# ============================================================

def run_visit(simulation_folder, export_script):

    print()
    print("=" * 70)
    print("RUNNING VISIT")
    print("=" * 70)

    print(
        f"Folder: {simulation_folder}"
    )

    # Run VisIt from inside the simulation directory.
    #
    # The "." tells VisIt to use the current simulation
    # directory as the database location.
    #
    # IMPORTANT:
    # Do NOT include "--" here. VisIt interprets "--"
    # as part of the database/path arguments, which causes
    # it to look for:
    #
    #     simulation_folder/--/celloutput.visit

    command = [
        VISIT_COMMAND,
        "-cli",
        "-nowin",
        "-s",
        export_script,
        "."
    ]

    print()
    print("Command:")
    print(" ".join(command))
    print()

    result = subprocess.run(
        command,
        cwd=simulation_folder
    )

    if result.returncode != 0:

        print()
        print(
            "ERROR: VisIt failed in:"
        )
        print(
            f"    {simulation_folder}"
        )

        return False

    print()
    print("VisIt completed successfully.")

    return True


# ============================================================
# RUN BURN RATE ANALYSIS
# ============================================================

def run_burn_rate(
    simulation_folder,
    burn_rate_script
):

    print()
    print("=" * 70)
    print("RUNNING BURN RATE ANALYSIS")
    print("=" * 70)

    print(
        f"Folder: {simulation_folder}"
    )

    eta_directory = os.path.join(
        simulation_folder,
        "eta_coords"
    )

    # Make sure VisIt actually created eta_coords
    if not os.path.isdir(eta_directory):

        print()
        print(
            "ERROR: eta_coords directory does not exist:"
        )
        print(
            f"    {eta_directory}"
        )

        return False

    # Your burn_rate_analysis.py expects
    # the eta_coords directory as sys.argv[1].
    command = [
        sys.executable,
        burn_rate_script,
        eta_directory
    ]

    print()
    print("Command:")
    print(" ".join(command))
    print()

    result = subprocess.run(
        command,
        cwd=simulation_folder
    )

    if result.returncode != 0:

        print()
        print(
            "ERROR: Burn-rate analysis failed in:"
        )
        print(
            f"    {simulation_folder}"
        )

        return False

    print()
    print("Burn-rate analysis completed successfully.")

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Parent directory
    # --------------------------------------------------------

    if len(sys.argv) > 1:

        parent_directory = os.path.abspath(
            sys.argv[1]
        )

    else:

        # If no argument is provided, use current directory
        parent_directory = os.getcwd()

    print()
    print("=" * 70)
    print("RUN ALL SIMULATION ANALYSIS")
    print("=" * 70)

    print()
    print(
        "Parent directory:"
    )
    print(
        f"    {parent_directory}"
    )

    # --------------------------------------------------------
    # Check scripts
    # --------------------------------------------------------

    export_script = os.path.join(
        parent_directory,
        EXPORT_SCRIPT
    )

    burn_rate_script = os.path.join(
        parent_directory,
        BURN_RATE_SCRIPT
    )

    if not os.path.isfile(export_script):

        print()
        print(
            "ERROR: Could not find:"
        )
        print(
            f"    {export_script}"
        )

        sys.exit(1)

    if not os.path.isfile(burn_rate_script):

        print()
        print(
            "ERROR: Could not find:"
        )
        print(
            f"    {burn_rate_script}"
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Find simulation folders
    # --------------------------------------------------------

    simulation_folders = find_simulation_folders(
        parent_directory
    )

    if len(simulation_folders) == 0:

        print()
        print(
            "ERROR: No simulation folders found."
        )

        print(
            "Each folder must contain:"
        )

        print(
            f"    {DATABASE_NAME}"
        )

        sys.exit(1)

    print()
    print(
        f"Found {len(simulation_folders)} "
        f"simulation folders:"
    )

    for folder in simulation_folders:

        print(
            f"    {os.path.basename(folder)}"
        )

    # --------------------------------------------------------
    # Process every simulation
    # --------------------------------------------------------

    successful = []
    failed = []

    for simulation_folder in simulation_folders:

        folder_name = os.path.basename(
            simulation_folder
        )

        print()
        print()
        print("#" * 70)
        print(
            f"PROCESSING: {folder_name}"
        )
        print("#" * 70)

        # ----------------------------------------------------
        # STEP 1
        # Run VisIt
        # ----------------------------------------------------

        visit_success = run_visit(
            simulation_folder,
            export_script
        )

        if not visit_success:

            failed.append(folder_name)

            print()
            print(
                f"SKIPPING burn-rate analysis for "
                f"{folder_name}"
            )

            continue

        # ----------------------------------------------------
        # STEP 2
        # Run burn-rate analysis
        # ----------------------------------------------------

        burn_success = run_burn_rate(
            simulation_folder,
            burn_rate_script
        )

        if not burn_success:

            failed.append(folder_name)
            continue

        successful.append(folder_name)

        print()
        print(
            f"COMPLETED: {folder_name}"
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print()
    print("=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)

    print()
    print(
        f"Successful: {len(successful)}"
    )

    for folder in successful:

        print(
            f"    {folder}"
        )

    if failed:

        print()
        print(
            f"Failed: {len(failed)}"
        )

        for folder in failed:

            print(
                f"    {folder}"
            )

    print()
    print(
        "The individual simulation results are now ready."
    )

    print(
        "You can run your combined plotting script "
        "without rerunning VisIt."
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
