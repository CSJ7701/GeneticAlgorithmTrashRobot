# Overview
This project was an exploration of reinforcement learning using genetic algorithms.
Based on an excerpt from 'Complexity: A Guided Tour' by Melanie Mitchell, the general premise is that of an autonomous robot that exists in a grid. Some random number of spaces within this grid contain pieces of trash, and the robot's job is to navigate the grid and retrieve as many pieces of trash as possible.

# General Theory
As a quick overview, genetic algorithms are based on a collection of 'Individuals', which make up a 'Generation'.
Each individual is essentially a single robot, and a generation is a collection of *N* of those individual robots.

Each individual is evaluated based on a 'control vector', which is a list that tells the individual how to behave in a given scenario.
For example, an individuals control vector might specify that when there is a wall to the north and west, and a can to the east, that the robot should move east.

A genetic algorithm will step through some number of time steps, using the control vector to make the individual perform actions. 
Those actions earn or deduct 'points' from the individual, and at the end of the simulation, those points are added to produce the individual's 'score'.

A generation will consist of N individuals, each with a score. The generation will then evolve, choosing some method of reproduction between its best component individuals.
There will be some percentage chance of mutation (or random change), but the individuals with the highest scores should be allowed to reproduce.
This reproduction will continue until a new generation composed of N individuals is generated, at which point the evaluation process will begin again.

This process repeats until some benchmark is met.

# Implementation
My code consists of 5 files. 
- Plot.py
- Algorithm.py
- Robot.py
- Grid.py
- Main.py

Grid.py specifies the environment that the robot will operate in. It defines an X by X square matrix, then fills that matrix with 'cans' or 'trash' based on some probability.
These are all tuneable parameters.

Robot.py defines the agent that will operate. It has methods to move, look around, and pick up cans.
As the agent moves, it records its path. This path is cleared on each new iteration.
The agent's methods return true or false based on whether they succeed, these are used elsewhere to compute score.

Algorithm.py defines methods for evaluating both individuals and generations, and for reproducing.
It also defines the options that are available for the agent to perform (move N,S,E,W etc)

Plot.py defines a method to visualize the best performing individuals within each generation.
Plotting is optional, with a switch option located in Main.py

Main.py is the wrapper for all the supporting files.
It initializes each component, and sets limits to define how long the program will run. 
It also displays information in the terminal about each generation's general performance.

# Running This Code
## Requirements
**Python** - preferrably 3.10
Most of these libraries used should come with your python installation. They are listed here in case they do not.
Use [pip](https://pypi.org/project/pip/) to install any missing libraries.
- *Numpy*
- *Matplotlib*
- *itertools*
- *random*
- *os*
- *copy*

