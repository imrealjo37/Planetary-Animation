import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants for the planets (values from Table 2a)
# Each planet has a list of: [semi-major axis (AU), eccentricity, inclination (degrees), longitude of perihelion (degrees)]

planets = {
    "Mercury": [0.38709843, 0.20563661, 7.00559432, 252.25166724],
    "Venus": [0.72332102, 0.00676399, 3.39777545, 181.97970850],
    "Earth": [1.00000018, 0.01673163, -0.00054346, 100.46691572],
    "Mars": [1.52371243, 0.09336511, 1.85181869, -4.56813164],
    "Jupiter": [5.20248019, 0.04853590, 1.29861416, 34.33479152],
    "Saturn": [9.54149883, 0.05550825, 2.49424102, 50.07571329],
    "Uranus": [19.18797948, 0.04685740, 0.77298127, 314.20276625],
    "Neptune": [30.06952752, 0.00895439, 1.77005520, 304.22289287],
}

# Function to calculate planet position based on time
def calculate_position(a, e, I, L, t):
    # Mean anomaly (degrees)
    M = (L + (360 * t / 365.25)) % 360  # Calculate the mean anomaly based on the time t
    # True anomaly (theta), ignoring eccentricity (e) for simplicity
    theta = M  # Use mean anomaly as an approximation for true anomaly
    # Convert orbital plane coordinates to Cartesian coordinates in the ecliptic plane
    x_orbital = a * 50 * np.cos(np.radians(theta))  # Scale orbits for better visibility
    y_orbital = a * 50 * np.sin(np.radians(theta))  # Scale orbits for better visibility

    # Convert to 3D space taking inclination into account
    x = x_orbital  # x coordinate in the ecliptic plane
    y = y_orbital * np.cos(np.radians(I))  # y coordinate adjusted for inclination
    
    return [x], [y]  # Return x and y as lists for 2D animation

# Update function for animation
def update(frame):
    # Update the position of each planet based on the current frame
    for planet, params in planets.items():
        a, e, I, L = params  # Unpack planet parameters
        x, y = calculate_position(a, e, I, L, frame)  # Calculate current position
        planet_dots[planet].set_data(x, y)  # Update the plot data for each planet
    return planet_dots.values()  # Return updated planet dots for the animation

# Tkinter window setup
root = tk.Tk()  # Create the main window
root.title("Planet Animation")  # Set the window title
root.geometry("1000x1000")  # Resize window to 1000x1000 pixels
root.configure(bg='black')  # Set the entire background to black

# Initialize the figure and axis for the plot
fig, ax = plt.subplots()  # Create a figure and axis
ax.set_xlim(-2000, 2000)  # Set x-axis limits to include Neptune
ax.set_ylim(-2000, 2000)  # Set y-axis limits to include Neptune
ax.set_aspect('equal')  # Set aspect ratio to equal for accurate representation

# Change the background color of the plot to black
ax.set_facecolor('black')  # Set the plot background to black
fig.patch.set_facecolor('black')  # Set the figure background to black

# Create scatter plot for the planets
planet_dots = {}  # Dictionary to hold planet dot objects
for planet in planets.keys():
    dot, = ax.plot([], [], 'o', label=planet)  # Create a scatter plot for each planet
    planet_dots[planet] = dot  # Store the dot object for each planet

# Embed Matplotlib figure into Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)  # Create a canvas to hold the figure
canvas_widget = canvas.get_tk_widget()  # Get the Tkinter widget for the canvas
canvas_widget.pack(fill=tk.BOTH, expand=True)  # Make the canvas fill the window and expand with resizing

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=365, interval=100, blit=True)  # Animate the plot over 365 frames

# Add the Matplotlib legend and position it at the top-right
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1))  # Move legend to the top-right outside the plot

# Start the Tkinter main loop
root.mainloop()  # Run the application
