import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def animate_traces(traces: np.array, interval=100, save=False, filename='animation.gif'):
    # Create a Figure and Axes objects
    fig, ax = plt.subplots()

    # Set the x and y limits of the Axes object
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)

    # set axis equal
    ax.set_aspect('equal')

    # Initialize the line and scatter objects to be plotted
    line, = ax.plot([], [], lw=3, color="b")
    scatter = ax.scatter([], [], s=100, color="r")

    # The function to animate the plot
    def animate(i):
        # Set the data for the line and scatter objects
        line.set_data(traces[0, :i+1], traces[1, :i+1])
        scatter.set_offsets([traces[0, i], traces[1, i]])

        # Set the alpha value of the scatter object to decrease over time
        scatter.set_alpha(1 - i/traces.shape[1])
        line.set_alpha(1 - i/traces.shape[1])

        # Return the line and scatter objects to be plotted
        return line, scatter

    # Create an animation using the animate function
    anim = FuncAnimation(
        fig,
        animate,
        frames=traces.shape[1],
        interval=interval,
        repeat=True,
        blit=True,
    )

    if save:
        # Save the animation as a gif
        anim.save(filename, writer="imagemagick", fps=10)
        plt.close()
    else:
        # Show the animation
        plt.show()
