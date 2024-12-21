#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from astropy.timeseries import LombScargle
from matplotlib.colors import LogNorm

# Plot configurations
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avenir'

# Parameters for Gaussian profiles
mean_spot = 16.39  # Mean RV of the starspot
mean_planet = 16.39  # Mean RV of the planet
stddev_spot = 3.0  # Standard deviation of the spot's Gaussian
stddev_star = 9.92  # Standard deviation of the star's Gaussian
amplitude_spot = 5.1e-3  # Amplitude of the spot's CCF
amplitude_star = 0.0614  # Amplitude of the star's CCF

# Parameters for Doppler shifts
amplitude_motion_spot = 0.0  # Initial amplitude of spot-induced motion
amplitude_motion_planet = 0.30  # Semi-amplitude of the planet's motion (K)
frequency_motion_planet = 0.0396  # Planet orbital frequency (1/25.2 days)
frequency_motion_spot = 0.11  # Spot modulation frequency (1/9 days)

# Arrays to store results
spot_to_star_ratio = []  # Ratios of spot-to-planet amplitude (h/K)
powers = []  # Lomb-Scargle periodogram powers

# Time and RV axis setup
times = np.linspace(0, 100, 100)  # Time array for simulation
x = np.linspace(-40, 70, 1000)  # RV axis for Gaussian evaluation

# Loop over varying spot-to-planet amplitude ratios
for j in range(100):
    miny_list = []  # RV minima for this iteration
    amplitude_motion_spot += 0.015  # Increment spot modulation amplitude
    spot_to_star_ratio.append(amplitude_motion_spot / amplitude_motion_planet)

    # Simulate the combined effect over 100 time steps
    for i in range(100):
        # Define Gaussians for the star and spot with periodic Doppler shifts
        gaussian_planet = norm(mean_planet + amplitude_motion_planet * np.sin(2 * np.pi * frequency_motion_planet * i), stddev_star)
        gaussian_spot = norm(mean_spot + amplitude_motion_spot * np.sin(2 * np.pi * frequency_motion_spot * i), stddev_spot)

        # Compute the total CCF from star and spot components
        y_spot = -amplitude_spot * gaussian_spot.pdf(x)  # Spot contribution
        y_planet = amplitude_star * gaussian_planet.pdf(x)  # Planet contribution
        y = -1.0 * (y_spot + y_planet) + 1.0  # Total CCF profile

        # Identify the RV minimum (peak of the total CCF)
        peak_index = np.argmin(y)
        peak_x = x[peak_index]
        miny_list.append(peak_x)

    # Compute Lomb-Scargle periodogram for RV minima
    ls = LombScargle(times, miny_list)
    freqs, pows = ls.autopower(minimum_frequency=0.01, maximum_frequency=0.7, samples_per_peak=50)
    powers.append(pows)

# Convert results to numpy arrays for analysis
spot_to_star_ratio_array = np.array(spot_to_star_ratio)
freqs_array = 1. / np.array(freqs)  # Convert frequencies to periods
powers_array = np.array(powers)

# Plot the 2D periodogram
fig, ax = plt.subplots()

# Create a color-coded 2D periodogram plot
im = ax.pcolormesh(spot_to_star_ratio_array, freqs_array, powers_array.T, cmap='plasma', norm=LogNorm(vmin=0.02, vmax=1.0))
cbar = plt.colorbar(im)
cbar.ax.tick_params(labelsize=12)
cbar.set_label('Periodogram Power', fontsize=16)

# Annotate the plot with relevant features
plt.text(2.2, 28, 'Injected planet', fontsize=12, color='white')
plt.text(2.2, 11, 'Spot signal', fontsize=12, color='white')

# Add vertical lines for specific $h/K$ thresholds
ax.axvline(1.1, color='white', linestyle='dashed', label='$h/K = 1.1$ (CI Tau)')
ax.axvline(4.0, color='aquamarine', linestyle='dashed', label='$h/K = 4.0$ (optical)')
ax.axvline(1.7, color='bisque', linestyle='dashed', label='$h/K = 1.7$ (H-band)')

# Add axis labels and legend
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_xlabel('${h}$/${K}$', fontsize=16)
ax.set_ylabel('Period (d)', fontsize=16)

# Save and display the plot
plt.legend(fontsize=12)
plt.savefig('spot_to_star_amplitude_ratio_2d.png')
plt.show()
