import math
import lib601.util as util
import lib601.soarWorld as soarWorld
import lib601.search as search
from soar.io import io
from mazeAnswers import *

import tk
import soarWorld
tk.setInited()

worldname = 'dl2World'
worldname = 'bigEmptyWorld'

PATH_TO_WORLD = '%s.py' % worldname
world = [i.strip() for i in open('%s.txt' % worldname).readlines()]

bounds = {'dl2World': (0.0,0.0,10.8,10.8),
          'bigEmptyWorld': (0.0,0.0,4.05,4.05)}
pathInd = 0
xhist = 0
yhist = 0
angHist = 0
halfw = 0.1
halfh = 0.1

def getPath(worldname, world):
    if worldname == 'dl2World':
        return search.search(MazeSearchNode(world, world.start, None), lambda state: state==world.goal)
    else:
        return [(15,4), (17,8), (13,12), (11,8), (9,4), (5,8), (7,12)]
        

class RobotMaze(Maze):
    def __init__(self, world, x0, y0, x1, y1):
        self.map = world
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
        Maze.__init__(self,world)

    def pointToIndices(self, point):
        ix = int(math.floor((point.x-self.x0)*self.width/(self.x1-self.x0)))
        iix = min(max(0,ix),self.width-1)
        iy = int(math.floor((point.y-self.y0)*self.height/(self.y1-self.y0)))
        iiy = min(max(0,iy),self.height-1)
        return ((self.height-1-iiy,iix))

    def indicesToPoint(self, (r,c)):
        halfw = (self.x1 - self.x0)/self.width
        halfh = (self.y1- self.y0)/self.height
        x = ((self.x1 - self.x0)/self.width) * (c+.5) + self.x0
        y = ((self.y1 - self.y0)/self.height) * ((self.height - r)-.5) + self.y0
        
        pntInst = util.Point(x,y)
        return pntInst



# this function is called when the brain is loaded
def setup():
    robot.maze = RobotMaze(world, *(bounds[worldname]))
    robot.path = getPath(worldname, robot.maze)
    (robot.window, robot.initialLocation) = \
                   soarWorld.plotSoarWorldDW(PATH_TO_WORLD)
    if robot.path:
        robot.window.drawPath([robot.maze.indicesToPoint(i).x - \
                               robot.initialLocation.x \
                               for i in robot.path],
                              [robot.maze.indicesToPoint(i).y - \
                               robot.initialLocation.y \
                               for i in robot.path], color = 'purple')
    else:
        print 'no plan from', robot.maze.start, 'to', robot.maze.goal
    robot.slimeX = []
    robot.slimeY = []

# this function is called when the start button is pushed
def brainStart():
    pass

# this function is called 10 times per second
def step():
    global pathInd, angHist
    x, y, theta = io.getPosition()
    robot.slimeX.append(x)
    robot.slimeY.append(y)
    
    #print robot.goal
    currentPoint = util.Point(x,y).add(robot.initialLocation)
    currentAngle = theta
    destinationPoint = robot.maze.indicesToPoint(robot.path[pathInd])

    dx = destinationPoint.x-currentPoint.x
    dy = destinationPoint.y - currentPoint.y
    
    #atanVal = math.atan((destinationPoint.y-currentPoint.y)/(destinationPoint.x - currentPoint.x)) 
    atanVal2 = math.atan2(dy,dx)
    thresh = 0.01
    destAng = fixAngle02Pi(atanVal2)

    print 'CurrentPoint'+str(currentPoint)
    print 'Dest Point'+str(destinationPoint)
    
    if atanVal + angHist < 0:
        destAng = 2* math.pi + atanVal + angHist
    else:
        destAng = atanVal + angHist

    

    print 'CurrAng'+str(currentAngle)
    
    if abs(dx) <= thresh and abs(dy) <= thresh:
        pathInd +=1
        angHist = currentAngle
        print '\n\n Im at destination! \n\n'+str(currentPoint)
    elif 
##    elif -thresh< atanVal < thresh:
##        io.setRotational(0)
##        io.setForward(math.sqrt(dx**2 + dy**2))
##        print 'Within thresh \n Atan:'+str(atanVal)
##        print 'GO forward'
    elif -thresh < (destAng - currentAngle) < thresh :
        io.setRotational(0)
        io.setForward(math.sqrt(dx**2 + dy**2))
        print 'Within thresh'+str(destAng - currentAngle)
        print 'GO forward'
        print atanVal
    elif destAng - currentAngle > math.pi:
        io.setForward(0)
        io.setRotational(-(destAng - currentAngle)/2)
        print 'Atan:'+str(atanVal)
        print 'Turning Right' + str(destAng - currentAngle)
        print atanVal
    elif destAng - currentAngle < math.pi:
        io.setForward(0)
        io.setRotational(destAng - currentAngle)
        print 'Atan' + str(atanVal)
        print 'Turning' + str(destAng - currentAngle)
        print atanVal
        
# called when the stop button is pushed
def brainStop():
    for i in range(len(robot.slimeX)):
        robot.window.drawPoint(robot.slimeX[i], robot.slimeY[i], 'red')
        
# called when brain or world is reloaded (before setup)
def shutdown():
    pass
