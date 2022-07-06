import dataclass
import numpy as np
import math

@dataclass
class BoundingBox:
    start = [0,0]
    end = [1,1]
    def getWidth(self):
        return self.end[0] - self.start[0]
    def getHeight(self):
        return self.end[1] - self.start[1]
    def getArea(self):
        return self.getWidth() * self.getHeight()

"""
HC order 1:
     ____
    |    |
    |    |
Rule: 
"""

class HilbertCurve:
    order = 1
    scale = 1
    rot = 0 # used to generate mat
    start = [0,0] # translation matrix
    points = [[0,0],[0,1],[1,1],[0,1]] #Point array

    def __init__(self,o,s,r,ps):
        self.order = o
        self.scale = s
        self.rot = r
        self.points = ps

    def getBBox(self):
        return BoundingBox(self.points[0], self.points[-1])

    #WRITEME: apply rot matrix and 0 rot
    def compile(self):
        pass
        self.rot = 0

    #WRITEME: concat points
    def merge(self, other):
        pass

HC1 = HilbertCurve(1, 1, 0, [[0,0],[0,1],[1,1],[0,1]])

#WRITEME
def makeHilbertGeneric(order, size):
    if(order == 1):
        return HC1
    
    TR = makeHilbertGeneric(order - 1, 1)  #FIXME: figure out scaling here
    TL = makeHilbertGeneric(order - 1, 1)
    BR = makeHilbertGeneric(order - 1, 1)
    BL = makeHilbertGeneric(order - 1, 1)

    TR.scale = size/4
    TR.rot = 0
    TR.start = [0,2] 
    TR.compile()

    TL.scale = size/4
    TL.rot = 0
    TL.start = [2,2]
    TL.compile()

    BR.scale = size/4
    BR.rot = 3 * math.PI / 2
    BR.start = [0,0]
    BR.compile()

    BL.scale = size/4
    BL.rot = math.PI / 2
    BL.start = [2,0]
    BL.compile()

    out = BL.merge(TL).merge(TR).merge(BR)
    out.scale = size
    out.compile()
    return out


def makeHilbertVarDense(tr_order, tl_order, br_order, bl_order):
    TR = makeHilbertGeneric(tr_order)
    TL = makeHilbertGeneric(tl_order)
    BR = makeHilbertGeneric(br_order)
    BL = makeHilbertGeneric(bl_order)
