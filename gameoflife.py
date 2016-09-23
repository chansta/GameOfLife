####################################################################################################################################################
"""
Name:                   gameoflife.py
Author:                 Felix Chan
Email:                  fmfchan@gmail.com
Date Created:           2016.09.23
Description:            A Python implementation of Conway's Game of Life
"""
####################################################################################################################################################

import numpy as np
import scipy as sp
import scipy.stats as sps
import matplotlib.pyplot as plt
import itertools as it
import sys as sys
from matplotlib import animation

class gameoflive(object): 
    """
    Implementing Conway's game of life as an animation. 
    """
    
    def __init__(self, N, board=None):
        """
        Initiate the board and other information. 
        """
        self.N = N
        move = np.array([-1,0,1])
        move = set(it.product(move, move))
        nullset = set([(0,0)])
        move = move.difference(nullset)
        self.allmove = dict(move_corner00=set([(0,1), (1,0), (1,1)]), move_cornerNN=set([(-1,0), (0,-1), (-1,-1)]), move_corner0N=set([(0,-1), (1,0), (1,-1)]),
               move_cornerN0=set([(-1,0), (0,1), (-1,1)]), move_edgetop=set([(-1,0), (1,0), (-1,-1), (1,-1), (0,-1)]),
               move_edgebottom=set([(-1,0), (1,0), (-1,1), (1,1), (0,1)]), move_edgeleft=set([(0,1), (0,-1), (1,1),(1,-1),(1,0)]), 
               move_edgeright=set([(0,1), (0,-1), (-1,1), (-1,1), (-1,0)]), move=move)
        if board is not None:
            self.board = board
        else:
            self.board = sps.randint.rvs(size=(N,N), low=0, high=2)     
        self.get_status()

    def checkpos(self, s):
        """
        check position to see if it is an edge, corner or interior of the board. 
        s: position to be checked as a tuple
        N: size of the board
        """
        if s == (0,0):
            return "move_corner00"
        elif s == (0,self.N-1):
            return "move_corner0N"
        elif s == (self.N-1,0):
            return "move_cornerN0"
        elif s == (self.N-1,self.N-1):
            return "move_cornerNN"
        elif s[0] == 0: 
            return "move_edgeleft"
        elif s[0] == self.N-1:
            return "move_edgeright"
        elif s[1] == 0:
            return "move_edgebottom"
        elif s[1] == self.N-1:
            return "move_edgetop"
        else:
            return "move"
    
    def liveordie(self, s):
        """
        Check if a given position s should live or die. 
        """
        place_to_check = self.allmove[self.checkpos(s)]
        coord = [tuple(np.array(s)+np.array(i)) for i in place_to_check]
        check = sum([1 for i in coord if self.board[i[0],i[1]] == 1 ])
        if (check <2) or (check >4):
            return 0
        else:
            return 1
        return check
    
    def born(self, s):
        """
        Check and see if an empty cell should be occupied. 
        """
        place_to_check = self.allmove[self.checkpos(s)]
        coord = [tuple(np.array(s)+np.array(i)) for i in place_to_check]
        check = sum([1 for i in coord if self.board[i[0],i[1]] == 1 ])
        if check == 3:
            return 1
        else:
            return 0
        return check
    
    def get_status(self):
        self.deathcells = [(i,j) for i,e1 in enumerate(self.board) for j,e2 in enumerate(e1) if self.board[i,j] == 0 ]
        self.livecells = [(i,j) for i,e1 in enumerate(self.board) for j,e2 in enumerate(e1) if self.board[i,j] == 1 ]
        return 0
    
    def next_gen(self):
        new_lc = list(map(self.liveordie, self.livecells))
        new_dc = list(map(self.born, self.deathcells))
        for i, e1 in enumerate(self.livecells):
            self.board[e1[0], e1[1]] = new_lc[i]
        for i, e1 in enumerate(self.deathcells):
            self.board[e1[0], e1[1]] = new_dc[i]
        self.get_status()
        return 0
    
    def draw_board(self):
        plt.clf()
        plt.xlim(0, self.N)
        plt.ylim(0, self.N)
        temp = [list(i) for i in self.livecells]
        boardx, boardy = zip(*temp)
        plt.scatter(boardx, boardy)

def FuncAnimate(i, g):
    g.next_gen()
    g.draw_board()
    plt.title("Generation {0}".format(i))


N = 50
g = gameoflive(N)
frames=1000
fig = plt.figure(figsize=(12,9), facecolor=(1,1,1))
FA = lambda i: FuncAnimate(i,g)
anim = animation.FuncAnimation(fig, FA, frames=1000)
if sys.argv[1] == "save":
    anim.save("gameoflife.mp4")
else:
    plt.show()

