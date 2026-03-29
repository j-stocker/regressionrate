#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# =========================
# DATA
# =========================

samples = np.array([
    "A","B","C","D","E","F","G","H","I","J","K","R","S","T"
])

# Classification
groups = {
    "Porous": ["A","B","C","D","E","F"],
    "Hollow": ["G","H"],
    "Solid":  ["I","J","K","R","S","T"]
}

# MWD (μm)
mwd = np.array([
    7.7313,4.5596,5.3438,4.3559,8.1854,8.6591,
    3.4167,3.7836,3.0309,3.7919,3.6889,14.8659,7.8058,2.8298
])

Sm = np.array([
    597.22,773.63,658.95,855.68,455.32,402.26,
    1110.4,980.05,702.22,561.1,577.16,142.36,272.92,752.37
])

color_map = {
    "A": (112/255, 66/255, 20/255),     # Sepia
    "B": (128/255, 0/255, 0/255),       # Maroon
    "C": (255/255, 0/255, 0/255),       # Red
    "D": (255/255, 140/255, 0/255),     # YellowOrange
    "E": (218/255, 165/255, 32/255),    # Goldenrod
    "F": (173/255, 255/255, 47/255),    # GreenYellow
    "G": (50/255, 205/255, 50/255),     # LimeGreen
    "H": (107/255, 142/255, 35/255),    # OliveGreen
    "I": (0/255, 176/255, 240/255),     # ProcessBlue
    "J": (0/255, 0/255, 128/255),       # NavyBlue
    "K": (0/255, 0/255, 255/255),       # Blue
    "R": (120/255, 81/255, 169/255),    # RoyalPurple
    "S": (199/255, 21/255, 133/255),    # RedViolet
    "T": (230/255, 230/255, 250/255)    # Lavender
}

# Burn rates
alamo_1 = np.array([2.83,3.04,3.25,2.65,3.53,3.70,4.38,4.59,3.75,3.25,3.25,1.62,2.29,3.86])
kohga_1 = np.array([3.8,3.2,3.6,3.2,3.5,3.0,4.6,5.1,3.4,3.2,3.2,2.2,2.6,3.5])

alamo_7 = np.array([9.52,9.79,9.85,9.47,9.83,10.19,7.59,7.44,5.63,6.00,5.83,5.22,5.63,5.66])
kohga_7 = np.array([10.1,7.1,7.6,7.2,7.8,6.4,13.1,12.0,7.2,6.8,6.9,5.3,6.0,7.2])

# =========================
# MARKERS
# =========================

def get_marker(sample):
    if sample in groups["Porous"]:
        return 'o'
    elif sample in groups["Hollow"]:
        return 's'
    else:
        return '*'

# =========================
# FIT FUNCTION
# =========================

def fit_line(x, y):
    return np.poly1d(np.polyfit(x, y, 1))

# =========================
# FILTER BY GROUP
# =========================

def get_group_data(group_name, x, y_exp, y_model):
    idx = [i for i, s in enumerate(samples) if s in groups[group_name]]
    
    x_g = x[idx]
    y_exp_g = y_exp[idx]
    y_model_g = y_model[idx]
    s_g = samples[idx]

    # remove NaNs
    valid = ~np.isnan(x_g)
    return x_g[valid], y_exp_g[valid], y_model_g[valid], s_g[valid]

# =========================
# PLOTTING
# =========================
def make_plot(x, y_model, y_exp, labels, title, xlabel, log=False):

    plt.figure()

    # -------------------------
    # Plot MODEL points (Alamo)
    # -------------------------
    for i, s in enumerate(labels):
        marker = get_marker(s)
        color = color_map[s]

        plt.scatter(
            x[i],
            y_model[i],
            marker=marker,
            color=color,
            label=f"{s}"
        )

    # -------------------------
    # Fit lines
    # -------------------------
    fit_model = fit_line(x, y_model)   # Alamo
    fit_exp = fit_line(x, y_exp)       # Kohga

    x_fit = np.linspace(min(x), max(x), 100)

    # Model fit (Alamo)
    plt.plot(
        x_fit,
        fit_model(x_fit),
        linestyle='-',
        linewidth=2,
        label="Alamo (Model) Fit"
    )

    # Experimental fit (Kohga ONLY — no points)
    plt.plot(
        x_fit,
        fit_exp(x_fit),
        linestyle='--',
        linewidth=2,
        label="Kohga (Experimental) Fit"
    )

    # -------------------------
    # Log scale if needed
    # -------------------------
    if log:
        plt.xscale('log')
        plt.yscale('log')

    # -------------------------
    # Labels / formatting
    # -------------------------
    plt.xlabel(xlabel)
    plt.ylabel("Burn Rate (mm/s)")
    plt.title(title)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    # Clean legend
    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys(), fontsize=7, ncol=2)

    plt.tight_layout()
    plt.show()
# =========================
# GENERATE ALL PLOTS
# =========================

for group in groups.keys():

    # 1 MPa
    x_mwd, yA1, yK1, s = get_group_data(group, mwd, alamo_1, kohga_1)
    x_sm,  yA1s, yK1s, s = get_group_data(group, Sm,  alamo_1, kohga_1)

    # 7 MPa
    x_mwd7, yA7, yK7, s = get_group_data(group, mwd, alamo_7, kohga_7)
    x_sm7,  yA7s, yK7s, s = get_group_data(group, Sm,  alamo_7, kohga_7)

    # ---- MWD ----
    make_plot(x_mwd, yA1, yK1, s, f"{group}: MWD vs Burn Rate (1 MPa)", "MWD (μm)")
    make_plot(x_mwd, yA7, yK7, s, f"{group}: MWD vs Burn Rate (7 MPa)", "MWD (μm)")

    make_plot(x_mwd, yA1, yK1, s, f"{group}: MWD vs Burn Rate LOG-LOG (1 MPa)", "MWD (μm)", log=True)
    make_plot(x_mwd, yA7, yK7, s, f"{group}: MWD vs Burn Rate LOG-LOG (7 MPa)", "MWD (μm)", log=True)

    # ---- S/m ----
    make_plot(x_sm, yA1s, yK1s, s, f"{group}: S/m vs Burn Rate (1 MPa)", "S/m (m²/kg)")
    make_plot(x_sm7, yA7s, yK7s, s, f"{group}: S/m vs Burn Rate (7 MPa)", "S/m (m²/kg)")

    make_plot(x_sm, yA1s, yK1s, s, f"{group}: S/m vs Burn Rate LOG-LOG (1 MPa)", "S/m (m²/kg)", log=True)
    make_plot(x_sm7, yA7s, yK7s, s, f"{group}: S/m vs Burn Rate LOG-LOG (7 MPa)", "S/m (m²/kg)", log=True)