import numpy as np

class Grid:
    def __init__(self, width, height, can_prob):
        self.width=width
        self.height=height
        self.grid=np.zeros((height, width))
        self.can_prob=can_prob
        self.filled_grid=self.FillCans()
        self.can_count=np.sum(self.filled_grid == 1)
        


    # Fills an array of arrays (coordinate grid) of the same size as self.grid (from width and height)
    # Has a probalility 'p'=[1-probability of can, probability of can] - this refers to the [0,1] value passed first, which are the choices the numpy has to fill the array from
    # self.grid is all 0's, so to fill it with cans, I add self.grid, and the generated array of 0's and 1's 
    def FillCans(self):
        CanMask=np.random.choice([0,1], size=self.grid.shape, p=[1- self.can_prob, self.can_prob])
        FilledGrid=self.grid + CanMask
        return FilledGrid
