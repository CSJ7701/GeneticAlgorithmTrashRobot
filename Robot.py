import random

class Agent:
    def __init__(self, board):
        self.position=(0,0) # (y,x)
        self.path=[]
        self.path.append(self.position)
        self.move_limit=200
        self.wall_penalty=2
        self.can_bonus=20
        self.stay_penalty=1
        self.pickup_penalty=2
        self.crossing_penalty=5
        self.gathered_can_locations=[]
        self.board=board

    def Reset(self):
        self.path=[]
        self.position=(0,0)
        self.path.append(self.position)
        self.gathered_can_locations=[]

    def IsCan(self, target):
        if self.board[target[0], target[1]] == 1 and target not in self.gathered_can_locations:
            return True
        else:
            return False

    def IsWall(self, target):
        x=target[1]
        y=target[0]
        if x < 0 or x >= self.board.shape[0] or y < 0 or y >= self.board.shape[1]:
            return True
        else:
            return False

    def IsOnPath(self, target):
        exists=any(target == sublist for sublist in self.path)
        return exists

    def CheckArea(self) -> list:
        """
        Checks agent's surroundings. 0: Nothing, 1: Wall, 2: Can.

        Returns:
        - result(list): A list of the agent's surroundings.
        """
        here=self.position
        result=[]
        surroundings=[
            (here[0]-1, here[1]), # North
            (here[0]+1, here[1]), # South
            (here[0], here[1]+1), # East
            (here[0], here[1]-1), # West
            (here[0], here[1]),   # Here
            ]
        for location in surroundings:
            if self.IsWall(location):
                result.append(1)
            elif self.IsCan(location):
                result.append(2)
            else:
                result.append(0)
        return result

    def MoveNorth(self):
        target=(self.position[0]-1, self.position[1])
        if self.IsWall(target):
            return False
        self.position=target
        self.path.append(self.position)
        return True

    def MoveSouth(self):
        target=(self.position[0]+1, self.position[1])
        if self.IsWall(target):
            return False
        self.position=target
        self.path.append(self.position)
        return True

    def MoveEast(self):
        target=(self.position[0], self.position[1]+1)
        if self.IsWall(target):
            return False
        self.position=target
        self.path.append(self.position)
        return True

    def MoveWest(self):
        target=(self.position[0], self.position[1]-1)
        if self.IsWall(target):
            return False
        self.position=target
        self.path.append(self.position)
        return True

    def MoveRandom(self):
        func=[self.MoveNorth, self.MoveSouth, self.MoveEast, self.MoveWest]
        choice=random.choice(func)
        return choice()

    def Pickup(self):
        if self.IsCan(self.position) and self.position not in self.gathered_can_locations:
            self.gathered_can_locations.append(self.position)
            # print(f"Gathered Cans: {self.gathered_can_locations}")
            # print(f"     Pickup @ {self.position}")
            return True
        else:
            return False
