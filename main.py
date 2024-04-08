from Env import Environment
from Agent import Agent
from Overseer import Overseer
import matplotlib.pyplot as plt
import numpy as np

# === Rules ===

# PossibilitiesMatrix
# [N, S, E, W, C]
# 0 = Nothing, 1 = Wall, 2 = Can

# Actions
# 0=move north 1=move south 2=move east 3=move west
# 4=stay 5=pick up 6=move random



# === Functions ===

def visualize(agent_moves, can_locations):
    fig, ax=plt.subplots()
    for can_location in can_locations:
        ax.plot(can_location[0], can_location[1], 'bo', markersize=8)

    # Plot agent's path
    x_values=[move[0] for move in agent_moves]
    y_values=[move[1] for move in agent_moves]
    ax.plot(x_values, y_values, 'r-', linewidth=2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    ax.set_title('Agent Path')

    ax.grid(True)

    plt.show()
    


if __name__ == "__main__":

    TrashEnv=Environment()
    TrashAgent=Agent(Environment=TrashEnv)
    TrashOverseer=Overseer(Agent=TrashAgent, Env=TrashEnv)

    Generation=TrashEnv.Populate()
    scores, Total, avg_score=TrashOverseer.EvaluateGeneration(Generation=Generation)
    print(f"Total: {Total} --- Avg: {avg_score}")

    original_path=TrashAgent.path

    CanCount=len(TrashEnv.CanLocations)
    while Total < CanCount*TrashAgent.CanBonus:

        TrashAgent.path=[]
        TrashAgent.location=(0,0)
        TrashAgent.GatheredCanLocations=[]
        
        Generation=TrashOverseer.Mate(scores=scores, Generation=Generation)
        scores, Total, avg_score=TrashOverseer.EvaluateGeneration(Generation=Generation)
        print(f"Total: {Total} --- Avg: {avg_score}")
        # visualize(TrashAgent.path, TrashEnv.CanLocations)

        
        
