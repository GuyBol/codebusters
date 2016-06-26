import sys
import math
import random
 
# Constants
MAX_X = 16000
MAX_Y = 9000
FOG_RANGE = 2200
MOVE_DISTANCE = 800
TRAP_RANGE_MIN = 900
TRAP_RANGE_MAX = 1760
MAX_GHOST_CARRY = 1
BASE_RANGE = 1600
 
 

def distance(a, b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

def randomPosition():
    return Position(random.randint(0,MAX_X), random.randint(0,MAX_Y))
 
''' Class representing a position '''
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
       
    def distance(self, b):
        return distance(self, b)
 
 
''' Buster '''
class Buster:
    def __init__(self, position, idn):
        self.pos = position
        self.idn = idn
        self.hasGhost = False
        self.command = None
        self.defaultTarget = randomPostion()
       
    def __init__(self, position, idn, hasGhost):
        self.pos = position
        self.idn = idn
        self.hasGhost = hasGhost
        self.command = None
        self.defaultTarget = randomPosition()
       
    def setCommand(self, ghost, d):
        if d > TRAP_RANGE_MAX:
            self.command = 'MOVE ' + str(ghost.pos.x) + ' ' + str(ghost.pos.y)
        elif d > TRAP_RANGE_MIN:
            self.command = 'BUST ' + str(ghost.idn)
    
    def getDefaultCommand(self):
        if distance(self.pos, self.defaultTarget) <= MOVE_DISTANCE:
            self.defaultTarget = randomPosition()
        return 'MOVE ' + str(self.defaultTarget.x) + ' ' + str(self.defaultTarget.y)
 
 
''' Ghost '''
class Ghost:
    def __init__(self, position, idn):
        self.pos = position
        self.idn = idn
 
 
''' World containing all participants '''
class World:
    def __init__(self, myTeamId):
        self.myTeamId = myTeamId
        self.myBusters = []
        self.enemyBusters = []
        self.ghosts = []
   
    def clean(self):
        #self.myBusters = []
        self.enemyBusters = []
        self.ghosts = []
   
    def addEntity(self, entity_id, x, y, entity_type, state, value):
        position = Position(x, y)
        # One of my busters (update if already exists)
        if entity_type == self.myTeamId:
            currentBuster = None
            for busterIter in self.myBusters:
                if busterIter.idn == entity_id:
                    currentBuster = busterIter
            if currentBuster:
                currentBuster.pos = position
                currentBuster.hasGhost = state==1
                currentBuster.command = None
            else:
                buster = Buster(position, entity_id, state==1)
                self.myBusters.append(buster)
        # Ghost
        elif entity_type == -1:
            ghost = Ghost(position, entity_id)
            self.ghosts.append(ghost)
        # Enemy buster
            buster = Buster(position, entity_id, state==1)
            self.enemyBusters.append(buster)
           
    def findClosestBuster(self, ghost):
        m = 10000000000
        busterRef = None
        for buster in self.myBusters:
            if not buster.command:
                d = distance(buster.pos, ghost.pos)
                if  d < m:
                    m = d
                    busterRef = buster
        if busterRef:
            busterRef.setCommand(ghost, m)
    
    def getBase(self):
        if self.myTeamId == 0:
            return Position(0,0)
        else:
            return Position(MAX_X, MAX_Y)
   
    def play(self):
        # Send back to base the busters with a ghost
        for buster in self.myBusters:
            if buster.hasGhost:
                if distance(buster.pos, self.getBase()) < BASE_RANGE:
                    buster.command = 'RELEASE'
                else:
                    buster.command = 'MOVE ' + str(self.getBase().x) + ' ' + str(self.getBase().y)
        for ghost in self.ghosts:
            self.findClosestBuster(ghost)
           
# Send your busters out into the fog to trap ghosts and bring them home!
 
busters_per_player = int(raw_input())  # the amount of busters you control
ghost_count = int(raw_input())  # the amount of ghosts on the map
my_team_id = int(raw_input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right
 
world = World(my_team_id)
 
# game loop
while True:
    world.clean()
    entities = int(raw_input())  # the number of busters and ghosts visible to you
    for i in xrange(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost.
        # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, state, value = [int(j) for j in raw_input().split()]
        world.addEntity(entity_id, x, y, entity_type, state, value)
       
    world.play()
   
    for i in xrange(busters_per_player):
 
        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."
       
        # MOVE x y | BUST id | RELEASE
        if world.myBusters[i].command != None:
            print world.myBusters[i].command
        else:
            print world.myBusters[i].getDefaultCommand()
