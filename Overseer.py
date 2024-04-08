from Agent import Agent
from Env import Environment
import random
import numpy as np

class Overseer:
    def __init__(self, *, Agent:Agent, Env:Environment, MutationChance:float = 0.2):
        self.Agent=Agent
        self.Env=Env
        self.MutationChance=MutationChance

    def EvaluateGeneration(self, *, Generation: list[list[int]]):
        scores=[]
        for individual in Generation:
            individual_scores=[]
            i=0
            while i < self.Agent.MoveLimit:
                score=self.Agent.Act(individual)
                individual_scores.append(score)
                i=i+1
            scores.append(individual_scores)
        print(f"Scores: {scores}")
        return scores #, sum(scores), sum(scores)/len(scores)

    def Mate(self, *, scores: list[int], Generation: list[list[int]]):
        indeces=np.argpartition(scores, -5)[-5:] # This should return the indeces of the 5 largest scores
        best_performing_individuals=[]
        for i in indeces:
            best_performing_individuals.append(Generation[i])
        new_generation=[]
        generation_size=self.Env.generation_size
        while len(new_generation) < generation_size:
            partner_indeces=random.sample(range(len(best_performing_individuals)), 2)
            split_index=random.sample(range(generation_size), 1)[0]
            partner1=best_performing_individuals[partner_indeces[0]]
            partner2=best_performing_individuals[partner_indeces[1]]
            partner11=partner1[:split_index]
            partner12=partner1[split_index:]
            partner21=partner2[:split_index]
            partner22=partner2[split_index:]

            offspring1=partner11 + partner22
            offspring2=partner21 + partner12

            for child in [offspring1, offspring2]:
                mutated_child=[]
                for number in child:
                    mutate_chance=random.random() # Generate a random number between 0 and 1
                    if mutate_chance < self.MutationChance: # Checks whether should mutate
                        mutated_child.append(random.randint(0,6))
                    else:
                        mutated_child.append(number)
                new_generation.append(mutated_child)
        return new_generation
        
