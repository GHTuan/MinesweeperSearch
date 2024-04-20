from Minesweeper import *
import time

class Heuristics(Game):
    def __init__(self):
        super().__init__()
        self.auto = True
        self.min = 1
        self.minList = []
    def getUncoverNeighbors(self,x,y):
        directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        
        neighbors = []
        
        for direct in directions:
            dx, dy = direct[0] + x, direct[1] + y
            if dx >= 0 and dy >= 0 and dx < len(self.grid) and dy < len(self.grid[0]):
                    if self.grid[dx][dy].clicked == False and self.grid[dx][dy].flag == False:
                        neighbors += [self.grid[dx][dy]]
        return neighbors
        
    def getFlagNeighbors(self,x,y):
        directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    
        neighbors = []
        
        for direct in directions:
            dx, dy = direct[0] + x, direct[1] + y
            if dx >= 0 and dy >= 0 and dx < len(self.grid) and dy < len(self.grid[0]):
                    if self.grid[dx][dy].flag == True:
                        neighbors += [self.grid[dx][dy]]
        return neighbors
        
    def run(self):
        change = True
        while change and self.gameState == "Playing":
            change = False
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    change += self.visit(x,y)
            if not change:
                if self.checkState():
                    return
                self.randomMove()
                self.checkState()
                change = True    
            self.min = 1
            self.minList = []
                        
 
    def randomMove(self):
        #print("Random move")
        while True:
            cell = self.minList[random.randrange(0,len(self.minList))]
            if cell.clicked == False:
                self.openGrid += cell.revealGrid()
                self.renderAndWait()
                break      
            print("this will never be call")
                
    def visit(self,x,y):
        if self.grid[x][y].clicked == False:
            if not self.grid[x][y].flag:
                self.grid[x][y].point = self.mineLeft / ((len(self.grid) * len(self.grid[0])) - self.openGrid)
                self.minPoint([self.grid[x][y]])
            return False
        
        if self.grid[x][y].val == 0:
            return False
       
        uncoverNeighbors = self.getUncoverNeighbors(x,y)
        flagNeighbors = self.getFlagNeighbors(x,y)
        
        if len(uncoverNeighbors) == 0:
            return False

        if self.grid[x][y].val - len(flagNeighbors) == len(uncoverNeighbors):
            self.changeState(uncoverNeighbors,'flag')
            return True

        if self.grid[x][y].val == len(flagNeighbors):
            self.changeState(uncoverNeighbors,'uncover')
            return True
        
        self.setNeighborPoint(uncoverNeighbors, (self.grid[x][y].val - len(flagNeighbors)) / len(uncoverNeighbors))
        self.minPoint(uncoverNeighbors)
        return False

    def changeState(self,neighbors,type):  
        if type == "flag":
            for neighbor in neighbors:
                neighbor.flag = True
                self.mineLeft -= 1
                self.openGrid += 1
                self.renderAndWait()
        elif type == "uncover":
            for neighbor in neighbors:
                if not neighbor.clicked:
                    self.openGrid += neighbor.revealGrid()
                    self.renderAndWait()
                
    
    def minPoint(self,listcell=[]):
        if self.minList == []:
            self.min = listcell[0].point
            self.minList = listcell
            return
        for cell in listcell:
            
            if cell.point < self.min:
                self.min = cell.point
                self.minList = [cell]
            elif cell.point == self.min and cell not in self.minList:
                self.minList += [cell]

    def setNeighborPoint(self,neighbor,point):
        for cell in neighbor:
            cell.point = point
                
                
game = Heuristics()


game.allowStep = True # Allow the game to pause after each step
game.finalText = True # Show the final text 
game.auto = False # Auto step
game.allowGameOver = True 

running = True
while running:
    # print("genning")
    # game.mainGridGen([[1,1],[1,2],[1,3],[1,4],[1,5],[2,1],[2,2],[2,3],[2,4],[2,5]])
    game.mainGridGen()
    # game.mainGridGen([[2,0],[3,0],[0,3]])
    #print("starting game")
    game.run()
    #print(game.gameState)
    print(game.gameState)
    r = True
    while r:
        keys = pygame.key.get_pressed()
        e = pygame.event.wait()
        if keys[pygame.K_ESCAPE]:
            r = False
            running = False
        if keys[pygame.K_r]:
            game.reset()
            r = False
    game.reset()
    r = False


pygame.quit()
quit()
        
    
    
    