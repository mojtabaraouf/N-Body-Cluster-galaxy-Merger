import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11
# Solar mass (kg)
M_sun = 1.989e30
# Particle mass (10^10 solar masses in kg)
m_particle = 1e10 * M_sun
# Conversion factors
pc = 3.0857e16  # Parsec in meters
Myr = 3.15576e13  # Megayear in seconds

# Simulation parameters
N_particles = 100
dt = 0.01 * Myr  # Time step (0.01 Myr)
t_max = 10 * Myr  # Total simulation time (10 Myr)
n_steps = int(t_max / dt)
n_frames = 100  # Number of frames for GIF

# Softening length to avoid singularities (in meters, ~100 pc)
epsilon = 100 * pc

def initialize_scenario1():
    """Initialize Scenario 1: One central cluster leading to one massive galaxy."""
    np.random.seed(42)
    pos = np.zeros((N_particles, 2))
    vel = np.zeros((N_particles, 2))
    masses = np.full(N_particles, m_particle)
    
    # Central cluster at origin (r < 10 kpc, v ~ 200 km/s)
    r_max = 10e3 * pc
    v_max = 2e5
    pos[:60] = np.random.normal(0, r_max / 2, (60, 2))
    vel[:60] = np.random.normal(0, v_max / 2, (60, 2))
    
    # Two smaller groups offset (x = ±50 kpc, v ~ ±100 km/s)
    pos[60:80] = np.random.normal([50e3 * pc, 0], r_max / 4, (20, 2))
    vel[60:80] = np.random.normal([-1e5, 0], v_max / 4, (20, 2))
    pos[80:] = np.random.normal([-50e3 * pc, 0], r_max / 4, (20, 2))
    vel[80:] = np.random.normal([1e5, 0], v_max / 4, (20, 2))
    
    return pos, vel, masses

def initialize_scenario2():
    """Initialize Scenario 2: Two clusters leading to two massive galaxies."""
    np.random.seed(43)
    pos = np.zeros((N_particles, 2))
    vel = np.zeros((N_particles, 2))
    masses = np.full(N_particles, m_particle)
    
    # Cluster 1 at x = -30 kpc (r < 10 kpc, v ~ 150 km/s)
    r_max = 10e3 * pc
    v_max = 1.5e5
    pos[:50] = np.random.normal([-30e3 * pc, 0], r_max / 2, (50, 2))
    vel[:50] = np.random.normal([1e5, 0], v_max / 2, (50, 2))
    
    # Cluster 2 at x = +30 kpc (r < 10 kpc, v ~ -150 km/s)
    pos[50:] = np.random.normal([30e3 * pc, 0], r_max / 2, (50, 2))
    vel[50:] = np.random.normal([-1e5, 0], v_max / 2, (50, 2))
    
    return pos, vel, masses

def compute_acceleration(pos, masses):
    """Calculate gravitational acceleration for all particles."""
    N = len(pos)
    acc = np.zeros((N, 2))
    for i in range(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_norm = np.sqrt(np.sum(r**2) + epsilon**2)
                acc[i] += G * masses[j] * r / r_norm**3
    return acc

def compute_potential(pos, masses, grid):
    """Calculate gravitational potential on a grid."""
    x, y = grid
    potential = np.zeros_like(x)
    for i in range(len(pos)):
        r = np.sqrt((x - pos[i, 0])**2 + (y - pos[i, 1])**2 + epsilon**2)
        potential -= G * masses[i] / r
    return potential

# Initialize both scenarios
pos1, vel1, masses1 = initialize_scenario1()
pos2, vel2, masses2 = initialize_scenario2()

# Store trajectories
traj1 = [pos1.copy()]
traj2 = [pos2.copy()]

# Simulate both scenarios
for step in range(n_steps):
    # Scenario 1
    acc1 = compute_acceleration(pos1, masses1)
    vel1 += acc1 * dt
    pos1 += vel1 * dt
    if step % (n_steps // n_frames) == 0:
        traj1.append(pos1.copy())
    
    # Scenario 2
    acc2 = compute_acceleration(pos2, masses2)
    vel2 += acc2 * dt
    pos2 += vel2 * dt
    if step % (n_steps // n_frames) == 0:
        traj2.append(pos2.copy())

# Set up plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
fig.suptitle('N-Body Simulation of Galaxy Cluster Mergers (10 Myr)', fontsize=16)

# Plotting parameters
plot_limits = 1e5 * pc  # 100 kpc
grid_res = 50  # Reduced for performance
x = np.linspace(-plot_limits, plot_limits, grid_res)
y = np.linspace(-plot_limits, plot_limits, grid_res)
X, Y = np.meshgrid(x, y)
grid = (X, Y)

# Initialize plots with initial potential
initial_potential1 = compute_potential(traj1[0], masses1, grid)
initial_potential2 = compute_potential(traj2[0], masses2, grid)
levels1 = np.linspace(np.min(initial_potential1), np.max(initial_potential1) * 0.5, 10)
levels2 = np.linspace(np.min(initial_potential2), np.max(initial_potential2) * 0.5, 10)

scatter1 = ax1.scatter([], [], s=10, c='blue', alpha=0.5)
contour1 = ax1.contour(X / pc, Y / pc, initial_potential1, levels=levels1, colors='red', alpha=0.5)
ax1.set_xlim(-plot_limits / pc, plot_limits / pc)
ax1.set_ylim(-plot_limits / pc, plot_limits / pc)
ax1.set_xlabel('X (pc)')
ax1.set_ylabel('Y (pc)')
ax1.set_title('Scenario 1: One Massive Galaxy')
ax1.grid(True)
ax1.set_aspect('equal')

scatter2 = ax2.scatter([], [], s=10, c='green', alpha=0.5)
contour2 = ax2.contour(X / pc, Y / pc, initial_potential2, levels=levels2, colors='red', alpha=0.5)
ax2.set_xlim(-plot_limits / pc, plot_limits / pc)
ax2.set_ylim(-plot_limits / pc, plot_limits / pc)
ax2.set_xlabel('X (pc)')
ax2.set_ylabel('Y (pc)')
ax2.set_title('Scenario 2: Two Massive Galaxies')
ax2.grid(True)
ax2.set_aspect('equal')

def init():
    """Initialize animation."""
    scatter1.set_offsets(np.zeros((N_particles, 2)))
    scatter2.set_offsets(np.zeros((N_particles, 2)))
    return [scatter1, scatter2]

def animate(i):
    """Update animation frame."""
    global contour1, contour2
    # Scenario 1
    pos1 = traj1[i]
    scatter1.set_offsets(pos1 / pc)
    potential1 = compute_potential(pos1, masses1, grid)
    levels1 = np.linspace(np.min(potential1), np.max(potential1) * 0.5, 10)
    for coll in contour1.collections:
        coll.remove()
    contour1 = ax1.contour(X / pc, Y / pc, potential1, levels=levels1, colors='red', alpha=0.5)
    
    # Scenario 2
    pos2 = traj2[i]
    scatter2.set_offsets(pos2 / pc)
    potential2 = compute_potential(pos2, masses2, grid)
    levels2 = np.linspace(np.min(potential2), np.max(potential2) * 0.5, 10)
    for coll in contour2.collections:
        coll.remove()
    contour2 = ax2.contour(X / pc, Y / pc, potential2, levels=levels2, colors='red', alpha=0.5)
    
    return [scatter1, scatter2]

# Create animation
ani = FuncAnimation(fig, animate, frames=len(traj1), init_func=init, blit=False, interval=50)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save as GIF
writer = PillowWriter(fps=20)
ani.save('galaxy_merger_animation.gif', writer=writer)
print("GIF saved as 'galaxy_merger_animation.gif'")
plt.close()