import itertools
import random
import pickle
import os

class Environment:
    def __init__(self, *, generation_size=200, visible_area=5, environment_states=3, possible_actions=6, board_dimensions=(20,20), can_prob=0.5):
        """
        Initializes an Environment instance.

        Parameters:
        - generation_size (int): The size of the population.
        - visible_area (int): The size of the area that the Agent can see.
        - environment_states (int): The number of environment states.
        - possible_actions (int): The number of actions that the agent can make.
        - board_dimensions (tuple): The dimensions of the environment board.
        - can_prob (float): The probability of a cell containing a can.

        Returns:
        - None
        """
        self.generation_size=generation_size
        self.visible_area=visible_area
        self.environment_states=list(range(environment_states))
        self.possible_actions=possible_actions
        self.board_dimensions=board_dimensions
        self.can_probability=can_prob

        if not os.path.exists('./Combinations.pkl'):
            self.FillPossibilitiesArray()
        self.PossibilitiesMatrix=self.LoadPossibilities()

        self.MakeBoard(Length=self.board_dimensions[0], Width=self.board_dimensions[1])
        self.FillCans()


    def FillPossibilitiesArray(self):
        """
        Fills an array with all possible combinations of environment states within the visible area.

        Returns:
        - None
        """
        num_combinations=len(self.environment_states)**self.visible_area # Finds the number of possible rows. NumColumns^NumPossibleValues
        array=[[0] * self.visible_area for _ in range(num_combinations)] # Fill an array with 'num_combinations' number of 1*possible_actions arrays, filled with 0's 
        for i, combination in enumerate(itertools.product(self.environment_states, repeat=self.visible_area)):
            array[i] = list(combination) # Fills each subarray with each successive combination of possible values
        print(array)    
        with open('./Combinations.pkl', 'wb') as f:
            pickle.dump(array, f)

    def LoadPossibilities(self):
        """
        Loads the array of possible combinations from file.

        Returns:
        - array (list): The array of possible combinations.
        """
        with open('./Combinations.pkl', 'rb') as f:
            array=pickle.load(f)
        return array

    def SearchPossibilities(self, Array: list[list[int]], Target: list[int]) -> int:
        """
        Searches an array for a specific target.

        Parameters:
        - Array (list): The 2-dimensional array to search.
        - Target (list): The target array to find in the array.

        Returns:
        - index (int): The index where the target is found.

        Raises:
        - ValueError: If the target is not found in the array.
        """
        for i, row in enumerate(Array):
            if row == Target:
                return i
        raise ValueError(f"Combination {Target} not found in array")

    def Populate(self) -> list[list[int]]:
        """
        Populates a Generation with individuals

        Returns:
        - Generation
        """
        Generation=[]
        index=0
        while index < self.generation_size: 
            Individual=[]
            Individual_Length=len(self.PossibilitiesMatrix)
            for i in range(Individual_Length):
                Individual.append(random.randint(0,self.possible_actions))
            Generation.append(Individual)
            index=index+1
        return Generation
        
    def MakeBoard(self, *, Length=10, Width=10):
        """
        Creates the game board.

        Parameters:
        - Length (int): The length of the board.
        - Width (int): The width of the board.

        Returns:
        - None
        """
        grid=[]
        for y in range(Width):
            row=[]
            for x in range(Length):
                row.append((x,y))
            grid.append(row)
        self.Board=grid

    def FillCans(self):
        """
        Randomly fills the environment with cans based on probability.

        Returns:
        - None
        """
        cans=[]
        for y in range(len(self.Board)):
            for x in range(len(self.Board[0])):
                if random.random() < self.can_probability:
                    cans.append((x,y))
        self.CanLocations=cans
