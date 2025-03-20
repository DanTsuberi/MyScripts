import numpy as np
import matplotlib.pyplot as plt

#Defining 
empty = 0
tree = 1
burn = 4
charred1 = 3
charred2 = 2

# Functions for Forest fire
class ForestFire:
    def __init__(self, size, p_fire = 0.01):
        self.size = size
        self.p_fire = p_fire

        # Create a grid where each cell is either 0 (empty) or 1 (tree)
        # p% of the grid will be empty (0), and 1-p% will have trees (1)

        self.grid = np.random.choice([0, 1], size=(self.size, self.size), p=[0.35, 0.65])
        
  

    def ignite(self, fire_spots = 3):
        for _ in range(fire_spots):
            x, y = np.random.randint(0, self.size, size=2)
            self.grid[x,y] = burn
            print(f"Tree set on fire at ({x}, {y})")

    

    def spread_fire(self):
        """Simulates fire spread for one step."""
        new_grid = self.grid.copy()

        for i in range(1, self.size):
            for j in range (1, self.size):
                if self.grid[i,j] == burn:
                    new_grid[i,j] = empty

                    for di, dj in [(-1,0),(1,0),(0,-1), (0,1)]:
                        neighbor_x, neighbor_y = i + di, j + dj
                        # Skip out-of-bound neighbors
                       
                       if 0 <= neighbor_x < self.size and 0 <= neighbor_y < self.size:    
                            if self.grid[neighbor_x, neighbor_y] == tree:
                                if np.random.rand() < self.p_fire:
                                    new_grid[neighbor_x, neighbor_y] = burn
                                    #print(f"Fire spread to ({neighbor_x}, {neighbor_y})")  # Print where fire spreads
                    
                       elif self.grid[i, j] == charred1: #intermidate state 1
                           new_grid[i, j] = charred2  

                       elif self.grid[i, j] == charred2: #intermidate state 2
                           new_grid[i, j] = empty  
    
        self.grid = new_grid
        #print(self.grid)

    def simulate (self, steps):
        """Runs the simulation for a given number of steps."""
        grids = []
        
        for _ in range(steps):
            grids.append(self.grid.copy())
            self.spread_fire()
        return grids

##################################################################################
#running the model#
forest_model = ForestFire(size=50,p_fire=0.85) # size of grid and probability to ignite neighbor

forest_model.ignite(fire_spots=1) #number of initial fires

simulation_steps = forest_model.simulate(steps=50) # number of steps to calculate

print(f"Number of steps: {len(simulation_steps)}") ##sanity check

###################################################################################
# Visualize one of the steps
# Choose step number 
viz_step = 19

if viz_step_user >= len(simulation_steps):
    viz_step = len(simulation_steps) - 1
else:
    viz_step = viz_step_user

# Define a discrete colormap with four distinct colors
cmap = mcolors.ListedColormap(["white", "green", "black", "orange", "red"]) 

#Use BoundaryNorm to correctly assign each state to a color
norm = mcolors.BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N)

plt.imshow(simulation_steps[viz_step], cmap=cmap, norm=norm)
plt.title(f"Step {viz_step} : Fire Spread Visualization")
plt.show()
    
###################################################################################
# Save steps as seperate images

for step in range(len(simulation_steps)):
    plt.imshow(simulation_steps[step], cmap=cmap, norm=norm)
    plt.title(f"Step {step}: Fire Spread Visualization")

    # Remove axes, ticks, and labels
    plt.axis('off')  # Turn off the axes
    plt.savefig(f"figures/ForestFire/step_{step}.png", bbox_inches='tight')
    plt.close() 

