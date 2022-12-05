import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation


def animate_traces(df: pd.DataFrame, n_players, interval=100, save=False, filename='animation.gif', fps=10):
    df.reset_index(inplace=True)

    # Create a Figure and Axes objects
    fig, ax = plt.subplots()

    # Set the x and y limits of the Axes object
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)

    # Remove the axes
    ax.axis('off')

    # set axis equal
    ax.set_aspect('equal')

    # Initialize the line and scatter objects to be plotted
    lines, scatters = [], []
    for i in range(n_players + 1):
        # generate random color
        color = np.random.rand(3, )
        # resource
        if i == 0:
            color = 'black'

        line, = ax.plot([], [], color=color)
        lines.append(line)

        scatter = ax.scatter([], [], s=100, color=color, edgecolor="k")
        scatters.append(scatter)

    # The function to animate the plot
    def animate(i):
        for j in range(n_players + 1):
            # resource
            if j == 0:
                x = 'x_resource'
                z = 'z_resource'
            else:
                x = f'x_{j}'
                z = f'z_{j}'

            lines[j].set_data(df.loc[:i, x], df.loc[:i, z])
            scatters[j].set_offsets(df.loc[i, [x, z]])

            # set alpha
            lines[j].set_alpha(0.5)
            scatters[j].set_alpha(0.7)

        # Return the line and scatter objects to be plotted
        return lines + scatters

    # Create an animation using the animate function
    anim = FuncAnimation(
        fig,
        animate,
        frames=df.shape[0],
        interval=interval,
        repeat=True,
        blit=True,
    )

    if save:
        # Save the animation as a gif
        anim.save(filename, writer="imagemagick", fps=fps)
        plt.close()
    else:
        # Show the animation
        plt.show()
