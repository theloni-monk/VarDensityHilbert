import numpy as np
import matplotlib.pyplot as plt
import math
import copy

"""
HC order 1:
     ____
    |    |
    |    |
Rules: 
TL start 0,2
TR start 2,2
BL flip along y=x start 0,0
BR flip along y=-x start 2,0
     __>_     __>_
    |    |   |    |
    ^    v   ^    v
    |    |   |    |

     _<__     __<_
         |   v
         ^   |
         |   |
start>---     --->end
"""

#WRITEME: instead of rotation just do flips and store the axis alongwhich u r flipping
#flip is equivalent to shifting the indicicies
xyflip = np.array([[0,1],[1,0]])
negxyflip = np.array([[0,-1],[-1,0]])
class HilbertCurve:
    order = 1
    scale = 1
    flipx = False
    flipy = False
    start = np.array([0,0]) # translation matrix
    points = np.array([[0,0],[0,1],[1,1],[0,1]]) #Point array

    def __init__(self,o, s, fxy, nfxy,ps):
        self.order = o
        self.scale = s
        self.flipxy = fxy
        self.negflipxy = nfxy
        self.points = ps

    def compile(self):
        
        smat = np.array([[0,self.scale],[self.scale,0]])
        self.points = np.transpose(np.matmul(smat, np.transpose(self.points)))
        
        if self.flipxy:
            self.points = np.transpose(np.matmul(xyflip, np.transpose(self.points)))
        elif self.negflipxy:
            self.points = np.transpose(np.matmul(negxyflip, np.transpose(self.points)))
        
        for p in self.points:
            p+=self.start
        
        self.flipx = False
        self.flipy = False
        
        self.scale = 1
        self.start = [0,0]

    def mergepoints(h1, h2):
        return h1.points.concat(h2.points)

#FIXME: figure out scaling issue
# o   2  3
# sm  3  3.3
def makeHilbertGeneric(order, size):
    if(order == 1):
        return HilbertCurve(1, 1, False, False, np.array([[0,0],[0,1],[1,1],[1,0]]))
    print("order", order, "")

    BL = makeHilbertGeneric(order - 1, 1)
    BL.scale = 1/2
    BL.flipxy = True
    BL.start = np.array([0,0])
    BL.compile()

    TL = makeHilbertGeneric(order-1, 1)
    TL.scale = 1/2
    TL.start = np.array([1,0]) 
    TL.compile()


    TR = makeHilbertGeneric(order- 1, 1)
    TR.scale = 1/2
    TR.start = np.array([1,1])
    TR.compile()

    BR = makeHilbertGeneric(order - 1, 1)
    BR.scale = 1/2
    BR.negflipxy = True
    BR.start = np.array([1/2, 3/2])
    BR.compile()

    blpoints = copy.deepcopy(BL.points)
    outpoints = np.concatenate((np.concatenate((np.concatenate((blpoints,TL.points)),TR.points)),BR.points))
    out = HilbertCurve(order, size, False, False, outpoints)
    out.compile() #apply scale

    return out


def makeHilbertVarDense(tr_order, tl_order, br_order, bl_order, size):
    TR = makeHilbertGeneric(tr_order, 1)
    TL = makeHilbertGeneric(tl_order, 1)
    BR = makeHilbertGeneric(br_order, 1)
    BL = makeHilbertGeneric(bl_order, 1)

    #WRITEME
    return out

test = makeHilbertGeneric(2, 1)#makeHilbertVarDense(3,4,5,6, 1)
print(test.points)
xs = test.points[:,0]
ys = test.points[:,1]
plt.plot(xs, ys)
plt.show()