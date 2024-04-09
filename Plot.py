import matplotlib
from matplotlib import colors
from matplotlib import axis
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

class Plotter:
    def __init__(self, agent, index: int=1):
        self.agent=agent
        self.grid=agent.board
        self.fig=plt.figure()
        self.file_name_tag=str(index)
        self.do_plot=True

        self.plot_agent()

    def update_agent(self, frame):
        plt.clf()
        plt.imshow(self.grid, cmap='binary', origin='lower')
        plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        plt.tick_params(axis='both', which='both', bottom=False,
                    left=False, labelbottom=False, labelleft=False)
        x_path, y_path=zip(*self.agent.path)
        x_path_now=x_path[:frame]
        y_path_now=y_path[:frame]
        for x,y in zip(x_path_now, y_path_now):
            if self.grid[x,y] == 1 and (x,y) in self.agent.gathered_can_locations:
                plt.plot(y,x,markersize=20, marker='x', color='green')
            else:
                plt.plot(y,x,markersize=20, marker='o', color='red')

    def plot_agent(self):
        ani=animation.FuncAnimation(self.fig, self.update_agent, frames=len(self.agent.path)+1, interval=400, repeat=True)
        plt.axis('off')
        plt.show()
        # export_file=os.path.join('assets', self.file_name_tag + '.gif')
        # gif_write=animation.PillowWriter(fps=2)
        # ani.save(export_file, writer=gif_write)
        # plt.close()
        # print(f"Plot Number {self.file_name_tag}")
        
