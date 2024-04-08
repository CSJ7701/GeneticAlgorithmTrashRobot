import itertools
from Robot import Agent
import random

class Algorithm:
    def __init__(self, population_size, mutation_rate, agent:Agent):
        self.population_size=population_size
        self.mutation_rate=mutation_rate
        self.agent=agent

        self.environment_states=[0,1,2]
        self.visible_area=5
        self.possible_actions=6
        self.mating_cutoff=0.1

        self.possibilities_matrix=self.Possibilities()

    def Possibilities(self):
        # Length of possibilities matrix
        num_combinations=len(self.environment_states)**self.visible_area 

        # Creates possibilities matrix and fills with arrays of length possible_actions, populated with 0's.
        array=[[0] * self.visible_area for _ in range(num_combinations)]
        for i, combination in enumerate(itertools.product(self.environment_states, repeat=self.visible_area)):
            array[i]=list(combination)
        return array

    def SearchPossibilities(self, target: list[int]):
        for i, row in enumerate(self.possibilities_matrix):
            if row == target:
                return i
        raise ValueError(f"Combination {target} not found in possibilities")

    def MakeIndividual(self):
        array=[]
        i=0
        while i < len(self.possibilities_matrix):
            num=random.randint(0,self.possible_actions)
            array.append(num)
            i=i+1
        return array

    def EvaluateIndividual(self, Ind: list):
        i=0
        points=[]
        self.agent.Reset()
        while i < self.agent.move_limit:
            # N,S,E,W,C
            surroundings=self.agent.CheckArea()
            index=self.SearchPossibilities(surroundings)
            action=Ind[index]
            if action == 0: # Move North
                if not self.agent.MoveNorth():
                    points.append(-self.agent.wall_penalty)
                    # print(f"Wall. P:{points}")
                # print(f"North. P:{points} @:{self.agent.position}")
            if action == 1: # Move South
                if not self.agent.MoveSouth():
                    points.append(-self.agent.wall_penalty)
                    # print(f"Wall. P: {points}")
                # print(f"South. P:{points} @:{self.agent.position}")
            if action == 2: # Move East
                if not self.agent.MoveEast():
                    points.append(-self.agent.wall_penalty)
                    # print(f"Wall. P: {points}")
                # print(f"East. P:{points} @:{self.agent.position}")
            if action == 3: # Move West
                if not self.agent.MoveWest():
                    points.append(-self.agent.wall_penalty)
                    # print(f"Wall. P: {points}")
                # print(f"West. P:{points} @:{self.agent.position}")
            if action == 4: # Stay
                # print(f"Stay. @:{self.agent.position}")
                points.append(-self.agent.stay_penalty)
                pass
            if action == 5: # Pick Up
                if self.agent.Pickup():
                    points.append(self.agent.can_bonus)
                    # print(f"Can Picked. P:{points} @:{self.agent.position}")
                else:
                    points.append(-self.agent.pickup_penalty)
                    # print(f"Pick Fail. P:{points} @:{self.agent.position}")
            if action == 6: # Move Random
                if not self.agent.MoveRandom():
                    points.append(-self.agent.wall_penalty)
                    # print(f"Wall. P: {points}")
                # print(f"Random. P:{points} @:{self.agent.position}")
            i=i+1
        return points, sum(points)

    def MakeGeneration(self):
        gen=[]
        i=0
        while i < self.population_size:
            ind=self.MakeIndividual()
            gen.append(ind)
            i=i+1
        # print(len(gen))
        return gen

    def EvaluateGeneration(self, gen):
        points=[]
        i=0
        while i < len(gen):
            ind=gen[i]
            score_list, total_score=self.EvaluateIndividual(ind)
            # print(score_list)
            points.append(total_score)
            i=i+1
        return points

    def SelectContenders(self, gen, points):

        if len(gen) != len(points):
            raise IndexError("Length of points does not match length of generations")
        
        max_score=max(points)
        cutoff_perc=self.mating_cutoff
        cutoff_score=(1-cutoff_perc)*max_score
        selected=[]

        eligible=[i for i in range(len(gen)) if points[i] >= cutoff_score]
        indeces=random.sample(eligible, 2)
        selected.append([gen[index] for index in indeces])
        return selected[0]

    def Mate(self, Parents: list[list[int]]) -> list[list[int]]:
        parent1=Parents[0]
        parent2=Parents[1]
        split_index=random.randint(0,len(parent1)-1)

        child1=parent1[:split_index] + parent2[split_index:]
        child2=parent2[:split_index] + parent1[split_index:]

        for child in [child1, child2]:
            i=0
            while i < len(child):
                if random.random() < self.mutation_rate:
                    child[i]=random.randint(0,6)
                i=i+1
        return [child1, child2]
