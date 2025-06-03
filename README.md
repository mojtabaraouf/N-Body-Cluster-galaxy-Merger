# Galaxy Cluster Merger N-Body Simulation

## Overview

This Python script simulates two N-body scenarios of galaxy cluster mergers, each with 100 particles of \(10^{10}\) solar masses, modeling the formation of massive galaxies within a cluster. The simulations produce distinct outcomes: **Scenario 1** forms one central massive galaxy with satellite galaxies, while **Scenario 2** forms two massive galaxies with satellites. The dynamics are visualized as a GIF animation with two panels, showing particle positions and gravitational potential contours over 10 million years (Myr). The code uses NumPy for numerical computations, Matplotlib for visualization, and Pillow for GIF generation, suitable for astrophysical analysis and visualization.

The simulation employs a simple Euler integrator with a softening length to avoid singularities, designed for short-term dynamics. It can be extended with advanced integrators (e.g., Verlet) or frameworks like AMUSE for long-term simulations, aligning with high-performance computing (HPC) workflows.

![galaxy_merger_animation](https://github.com/user-attachments/assets/fc718a5d-5fce-4c6b-9cc9-b008edfabfeb)


## Features

- **Scenarios**:
  - **Scenario 1**: One central cluster (60 particles) merges with two smaller groups (20 each), forming a single massive galaxy with satellites.
  - **Scenario 2**: Two equal clusters (50 particles each) form two massive galaxies with satellites.
- **Particles**: 100 particles per scenario, each with a mass of \(10^{10}\) solar masses (~dwarf galaxy mass).
- **Simulation**:
  - Duration: 10 Myr (~3.156e14 seconds, ~1e6 steps with 0.01 Myr time step).
  - Euler integration with a 100 parsec (pc) softening length.
  - Units: Positions in parsecs, velocities in m/s, time in Myr.
- **Visualization**:
  - Two-panel GIF: Scenario 1 (top, blue particles), Scenario 2 (bottom, green particles).
  - Plot limits: ±100 kpc, capturing merger dynamics.
  - Gravitational potential contours (red) overlaid dynamically in each frame.
  - Output: `galaxy_merger_animation.gif` (~2-5 MB, ~100 frames at 20 fps).
- **Codebase**: Leverages NumPy, Matplotlib, and Pillow for efficient computation and visualization.

## Requirements

- Python 3.6+
- NumPy (`pip install numpy`)
- Matplotlib (`pip install matplotlib`)
- Pillow (`pip install pillow`)

## Installation

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd galaxy-cluster-merger-nbody
   ```
2. Install dependencies:
   ```bash
   pip install numpy matplotlib pillow
   ```
3. Ensure the script (`galaxy_merger_nbody_gif.py`) is in the working directory.

## Usage

1. Run the script:
   ```bash
   python galaxy_merger_nbody_gif.py
   ```
2. The script simulates 10 Myr of dynamics for both scenarios and saves a GIF animation as `galaxy_merger_animation.gif` in the working directory.
3. View the GIF using any image viewer or browser.

### Output
- **File**: `galaxy_merger_animation.gif`
- **Size
