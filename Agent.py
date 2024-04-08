

from Env import Environment
import random


class Agent:
    def __init__(self, *, Environment: Environment):
        """
        Initializes an Agent instance.

        Parameters:
        - Environment (Environment): The environment in which the agent operates.

        Returns:
        - None
        """
        self.location=(0,0)
        self.path=[]
        self.path.append(self.location)
        self.Env=Environment
        self.MoveLimit=200
        self.WallPenalty=2
        self.CanBonus=5
        self.PickupPenalty=1
        self.GatheredCanLocations=[]

    def IsCan(self, target):
        """
        Checks if the given target location contains a can.

        Parameters:
        - target (tuple): The target location to check.

        Returns:
        - is_can (bool): True if the target location contains a can, False otherwise.
        """
        is_can=target in self.Env.CanLocations
        return is_can

    def IsWall(self, target: tuple):
        """
        Checks if the target location is a wall.

        Parameters:
        - target (tuple): The target location to check.

        Returns:
        - is_wall (bool): True if the location is a wall, False otherwise.
        """
        if target[0] < 0 or target[1] < 0:
            return True
        if target[0] > self.Env.board_dimensions[0]-1 or target[1] > self.Env.board_dimensions[1]-1:
            return True
        return False
            
    def CheckArea(self) -> list:
        """
        Checks the agent's surroundings.

        Returns:
        - result (list): A list representing the surroundings of the agent.
        """
        here=self.location
        result=[]
        location_list=[
            (here[0], here[1]-1), # North
            (here[0], here[1]+1), # South
            (here[0]+1, here[1]), # East
            (here[0]-1, here[1]), # West
            (here[0], here[1]),
            ]
        for location in location_list:
            if self.IsWall(location):
                result.append(1)
            elif self.IsCan(location):
                result.append(2)
            else:
                result.append(0)
        return result

    def MoveNorth(self):
        """
        Moves the agent one unit North.

        Returns:
        - success (bool): True if the move was successful, False otherwise.
        """
        target=(self.location[0], self.location[1]-1)
        if self.IsWall(target):
            return False
        self.location=target
        return True
        
    def MoveSouth(self):
        """
        Moves the agent one unit South.

        Returns:
        - success (bool): True if the move was successful, False otherwise.
        """
        target=(self.location[0], self.location[1]+1)
        if self.IsWall(target):
            return False
        self.location=target
        return True

    def MoveEast(self):
        """
        Moves the agent one unit East.

        Returns:
        - success (bool): True if the move was successful, False otherwise.
        """
        target=(self.location[0]+1, self.location[1])
        if self.IsWall(target):
            return False
        self.location=target
        return True

    def MoveWest(self):
        """
        Moves the agent one unit West.

        Returns:
        - success (bool): True if the move was successful, False otherwise.
        """
        target=(self.location[0]-1, self.location[1])
        if self.IsWall(target):
            return False
        self.location=target
        return True

    def MoveRandom(self):
        """
        Moves the agent one unit in a rancom direction.

        Returns:
        - success (bool): True if the move was successful, False otherwise.
        """
        functions=[self.MoveNorth, self.MoveSouth, self.MoveEast, self.MoveWest]
        choice=random.choice(functions)
        return choice()

    def Pickup(self):
        """
        Picks up a can if the Agent is in the same location as a can.

        Returns:
        - success (bool): True if the robot picked up a can, False if there was no can.
        """
        if self.IsCan(self.location) and self.location not in self.GatheredCanLocations:
            # print(f"Can found: {len(self.Env.CanLocations)}")
            self.GatheredCanLocations.append(self.location)
            return True
        else:
            return False
        
    def Act(self, gene: list[int]):
        """
        Performs an action based on the agent's gene and surroundings.

        Parameters:
        - Gene (list[int]): The agent's current gene.
        Returns:
        - Score
        """
        surroundings=self.CheckArea()
        index=self.Env.SearchPossibilities(self.Env.PossibilitiesMatrix, surroundings)
        action=gene[index]
        score=0
        if action == 0:
            if self.MoveNorth() is False:
                score=score-self.WallPenalty
        elif action == 1:
            if self.MoveSouth() is False:
                score=score-self.WallPenalty
        elif action == 2:
            if self.MoveEast() is False:
                score=score-self.WallPenalty
        elif action == 3:
            if self.MoveWest() is False:
                score=score-self.WallPenalty
        elif action == 4:
            pass
        elif action == 5:
            if self.Pickup() is True:
                score=score+self.CanBonus
            else:
                score=score-self.PickupPenalty
        elif action == 6:
            if self.MoveRandom() is False:
                score=score-self.WallPenalty
        self.path.append(self.location)
        return score
        
