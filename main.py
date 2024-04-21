from Robot import Agent
from Grid import Grid
from Algorithm import Algorithm
from Plot import Plotter

def main():
    grid=Grid(20,20,0.6)
    agent=Agent(grid.filled_grid)
    Alg=Algorithm(200, 0.1, agent)

    max_possible_score=grid.can_count*agent.can_bonus

    print(f" Num Cans: {grid.can_count}")
    print(grid.filled_grid)

    print(f"Loop runs until max score == {max_possible_score}")

    i=1
    Avg=0
    Max=0
    while int(Max) < int(max_possible_score):
        if i == 1:
            Generation=Alg.MakeGeneration()
        else:
            NewGen=[]
            # while len(NewGen) < len(Generation): # Old mating process
            #     Parents=Alg.SelectContenders(Generation, results)
            #     Children=Alg.Mate(Parents)
            #     NewGen.append(Children[0])
            #     NewGen.append(Children[1])

            NewGen=Alg.SelectiveMate(Generation, results)
            Generation=NewGen
            
        results, best_agent=Alg.EvaluateGeneration(Generation)
        # print(results)
        Max=max(results)
        Avg=sum(results)/len(results)
        print(f"Trial {i}: Max={Max}, Avg={Avg}")
        # if Max > 50:
            # Plotter(best_agent)
        i=i+1

    
if __name__ == "__main__":
    main()
