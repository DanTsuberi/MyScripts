import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Defining 
empty = 0
tree = 1
burn = 2


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
                        if neighbor_x < 0 or neighbor_x >= self.size or neighbor_y < 0 or neighbor_y >= self.size:
                            continue  # Skip this iteration if the neighbor is out of bounds
                            
                        if self.grid[neighbor_x, neighbor_y] == tree:
                            if np.random.rand() < self.p_fire:
                                new_grid[neighbor_x, neighbor_y] = burn
                                #print(f"Fire spread to ({neighbor_x}, {neighbor_y})")  # Print where fire spreads

    
        self.grid = new_grid
        #print(self.grid)

    def simulate (self, steps):
        """Runs the simulation for a given number of steps."""
        grids = []
        
        for _ in range(steps):
            grids.append(self.grid.copy())
            self.spread_fire()
        return grids
    

def animate_forest(forest, steps=50):
    """Animates the spread of fire in the forest."""
    fig, ax = plt.subplots()

    def update(frame):
        #ax.clear()
        cmap = plt.cm.get_cmap("viridis", 3)
        ax.imshow(forest[frame], cmap=cmap, vmin=0, vmax=2)
        ax.set_title(f"Step {frame}")
        ax.set_xticks([]) 
        ax.set_yticks([])

    anim = animation.FuncAnimation(fig,update,frames=len(forest), interval= 200)
    plt.show()

##################################################################################
#running the model#

forest_model = ForestFire(size=50,p_fire=0.85)
forest_model.ignite(fire_spots=1)
simulation_steps = forest_model.simulate(steps=50)
print(f"Number of steps: {len(simulation_steps)}") ##sanity check

###################################################################################
# Visualize one of the steps

plt.imshow(simulation_steps[19], cmap='viridis', vmin=0, vmax=2)
plt.title("Step 1: Fire Spread Visualization")
plt.show()
    
###################################################################################
# Save steps as seperate images

for step in range(len(simulation_steps)):
    plt.imshow(simulation_steps[step], cmap="viridis", vmin=0, vmax=2)
    plt.title(f"Step {step}: Fire Spread Visualization")

    # Remove axes, ticks, and labels
    plt.axis('off')  # Turn off the axes
    plt.savefig(f"figures/fire/test/step_{step}.png", bbox_inches='tight', pad_inches=0.1)
    plt.close() 

