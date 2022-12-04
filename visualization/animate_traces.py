import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation


def animate_traces(df: pd.DataFrame, interval=100, save=False, filename='animation.gif'):
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
    player1_line, = ax.plot([], [], color="red")
    player2_line, = ax.plot([], [], color="green")
    player3_line, = ax.plot([], [], color="blue")
    player1_scatter = ax.scatter([], [], s=100, color="red", edgecolor="k")
    player2_scatter = ax.scatter([], [], s=100, color="green", edgecolor="k")
    player3_scatter = ax.scatter([], [], s=100, color="blue", edgecolor="k")

    # The function to animate the plot
    def animate(i):
        # Set the data for the line and scatter objects
        player1_line.set_data([i[0] for i in df.loc[:i+1, 'pos1']],
                              [i[1] for i in df.loc[:i+1, 'pos1']])
        player2_line.set_data([i[0] for i in df.loc[:i+1, 'pos2']],
                              [i[1] for i in df.loc[:i+1, 'pos2']])
        player3_line.set_data([i[0] for i in df.loc[:i+1, 'pos3']],
                              [i[1] for i in df.loc[:i+1, 'pos3']])
        player1_scatter.set_offsets(df.loc[i, 'pos1'])
        player2_scatter.set_offsets(df.loc[i, 'pos2'])
        player3_scatter.set_offsets(df.loc[i, 'pos3'])

        # Set the alpha value of the scatter object to decrease over time
        player1_line.set_alpha(0.5)
        player2_line.set_alpha(0.5)
        player3_line.set_alpha(0.5)
        player1_scatter.set_alpha(0.7)
        player2_scatter.set_alpha(0.7)
        player3_scatter.set_alpha(0.7)

        # Return the line and scatter objects to be plotted
        return player1_line, player2_line, player3_line, player1_scatter, player2_scatter, player3_scatter

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
        anim.save(filename, writer="imagemagick", fps=10)
        plt.close()
    else:
        # Show the animation
        plt.show()
