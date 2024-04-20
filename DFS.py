from Minesweeper import *

class DFS_SOLVER(Game):
    def __init__(self):
        super().__init__()
        self.auto = True
        
    # def dfs(self): 
        
    #     for i in range(len(self.grid)):
    #         for j in range(len(self.grid[0])):
    #             if self.grid[i][j].clicked == 0:
    #                 self.dfs_click(i, j)

    # def dfs_click(self,x,y):  
    #         directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
            
    #         if self.grid[x][y].clicked or self.grid[x][y].flag:
    #             return
            
    #         gameDisplay.fill(bg_color)
    #         self.grid[x][y].revealGrid()
    #         self.Draw()
    #         self.wait()
            
    #         if self.grid[x][y].val == -1:      
    #             self.grid[x][y].hideGrid()
    #             self.grid[x][y].flag = True
    #             self.mineLeft -= 1
    #             self.Draw()
    #             self.wait()
    #             return

    #         for direct in directions:
    #             dx, dy = direct[0] + x, direct[1] + y
    #             if dx >= 0 and dy >= 0 and dx < len(self.grid) and dy < len(self.grid[0]):
    #                 self.dfs_click(dx,dy) 
    

    
    def revealAllUncoverGrid(self):
        for i in self.grid:
            for j in i:
                if j.clicked == False and j.flag == False:
                    j.revealGridNoAdjacent()
    
    def hideAllRevealGrid(self):
        for i in self.grid:
            for j in i:
                if j.clicked == True and j.flag == False:
                    j.hideGrid()
                    
            
    def dfs(self,x=0,y=0):
        if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
            return
        
        if self.grid[x][y].clicked or self.grid[x][y].flag:
            return
        
        if self.gameState != "Playing":
            return
        
        nextcord = self.nextcord(x,y)
    
        if self.mineLeft > 0:
            self.grid[x][y].flag = True
            self.mineLeft -= 1
            self.renderAndWait()
            if nextcord:
                self.dfs(nextcord[0],nextcord[1])
                if self.gameState != "Playing":
                    return
            else:
                self.revealAllUncoverGrid()
                self.renderAndWait()
                self.hideAllRevealGrid()
                self.renderAndWait()
                if self.checkState(): return
            self.grid[x][y].flag = False
            self.mineLeft += 1
            self.renderAndWait()
        if nextcord:
            self.dfs(nextcord[0],nextcord[1])
            if self.gameState != "Playing":
                return
        else:
            self.revealAllUncoverGrid()
            self.renderAndWait()
            self.hideAllRevealGrid()
            self.renderAndWait()
            if self.checkState(): return
        
        # self.grid[x][y].hideGrid()
        #self.renderAndWait()
        


    
    def nextcord(self,x,y):
        if x == len(self.grid) - 1 and y == len(self.grid[0]) - 1:
            return False
        if y < len(self.grid[0]) - 1:
            return x, y + 1
        
        if x < len(self.grid) - 1:
            return x + 1, 0
        

    def test(self):
        initstate = self.grid
        gameDisplay.fill(bg_color)
        self.Draw()
        self.wait()
        self.grid[0][0].revealGrid()
        self.grid[0][2].revealGrid()
        self.grid[0][3].revealGrid()
        gameDisplay.fill(bg_color)
        self.Draw()
        self.wait()
        self.grid = initstate
        gameDisplay.fill(bg_color)
        self.Draw()
        self.wait()
        
        
        
        
game = DFS_SOLVER()



game.allowStep = True # Allow the game to pause after each step
game.finalText = True # Show the final text 
game.auto = False # Auto step
game.allowGameOver = False # Allow the game to be over if the mine is clicked

running = True
while running:
    # print("genning")
    # game.mainGridGen([[1,1],[1,2],[1,3],[1,4],[1,5],[2,1],[2,2],[2,3],[2,4],[2,5]])
    game.mainGridGen()
    # game.mainGridGen([[2,0],[3,0],[0,3]])
    # print("starting game")
    game.dfs()
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


pygame.quit()
quit()
