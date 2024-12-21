# Radial Velocity Detection Limit Simulation

## Description
This code simulates the detection limit of a planet's radial velocity (RV) signal in the presence of stellar spot activity using Cross-Correlation Functions (CCFs) and Doppler motion. It constructs Gaussian profiles for the star and stellar spots, models their respective Doppler shifts over time, and combines these effects to create a total RV signal. 

The simulation calculates the RVs at each time step and generates a 2D periodogram to visualize how the spot-to-planet amplitude ratio ($h/K$) affects the detectability of the planet's signal.

## Key Features
1. Injects a 25.2-day periodic RV signal for the planet.
2. Simulates a 9-day spot modulation with varying amplitudes.
3. Identifies the threshold $h/K$ ratios where the planet's signal is detectable.
4. Applies the method to CI Tau to evaluate the detectability of its planetary signal amidst strong stellar activity.

## Usage
Run the code to simulate the 2D periodogram and visualize how varying spot-to-planet amplitude ratios affect the detection of the planet's RV signal.

## Output
The code generates a 2D periodogram plot showing:
- The detectability threshold for the planet's RV signal at different $h/K$ values.
- Annotations highlighting key detection thresholds based on specific cases (e.g., CI Tau, optical, and H-band).

The plot is saved as `spot_to_star_amplitude_ratio_2d.png` in the current directory.

For more info, please see Manick et al. 2024 (https://ui.adsabs.harvard.edu/abs/2024A%26A...686A.249M/abstract) 