import pygame
from pygame.locals import *
import random
pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)


game_width = 16          # Change this to increase size
game_height = 16         # Change this to increase size
numMine = 30             # Number of mines


grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# # Create global values
# grid = []  # The main grid
# mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)




# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type, grid):
        self.grid = grid
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  # Value of the grid, -1 is mine
        self.point = 1; # This is for heuristics purposes
    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        # Auto reveal if it's a 0
        t = 1
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if not self.grid[self.xGrid + x][self.yGrid + y].clicked:
                                t += self.grid[self.xGrid + x][self.yGrid + y].revealGrid()          
        return t


    def hideGrid(self):
        self.clicked = False
        
    def revealGridNoAdjacent(self):
        self.clicked = True

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if self.grid[self.xGrid + x][self.yGrid + y].val == -1:
                                self.val += 1

class Game:
    def __init__(self):
        self.grid = []  # The main grid
        self.mines = []  # Pos of the mines
        self.gameState = "Playing"  # Game state
        self.mineLeft = numMine  # Number of mine left
        self.t = 0  # Set time to 0
        self.openGrid = 0
        self.auto = True
        self.allowStep = False
        self.finalText = False
        self.allowGameOver = False
        
        
    def mainGridGen(self,mines = []):
        # print("generating mines")
            # Generating mines
        if mines == []:
            self.mines = [[random.randrange(0, game_width),
                random.randrange(0, game_height)]]
            # print(self.mines)
            for c in range(numMine - 1):
                pos = [random.randrange(0, game_width),
                random.randrange(0, game_height)]
                same = True
                while same:
                    for i in range(len(self.mines)):
                        if pos == self.mines[i]:
                            pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                            break
                        if i == len(self.mines) - 1:
                            same = False
                self.mines.append(pos)
        else: self.mines = mines
            
        # print("generating grid")
        
        # Generating entire grid
        for i in range(game_width):
            line = []
            for j in range(game_height):
                if [i, j] in self.mines:
                    line.append(Grid(i, j, -1, self.grid))
                else:
                    line.append(Grid(i, j, 0, self.grid))
            self.grid.append(line)
        #print("Updated grid")
        # Update of the grid
        for i in self.grid:
            for j in i:
                j.updateValue()
        
    def revealAllMines(self):
            # Auto reveal all mines if it's a mine
        for m in self.mines:
            if not self.grid[m[0]][m[1]].clicked:
                self.grid[m[0]][m[1]].revealGrid()

    def startManual(self):
         # Main Loop
        while self.gameState == "Playing":
            # Reset screen
            gameDisplay.fill(bg_color)

            # User inputs
            for event in pygame.event.get():
                # Check if player close window
                if event.type == pygame.QUIT:
                    self.gameState = "Exit"
                    pygame.quit()
                # Check if play restart
                if self.gameState == "Game Over" or self.gameState == "Win":
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_r:
                    #         self.gameState = "Exit"
                    #         gameLoop()
                    self.gameState = "Exit"
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        for i in self.grid:
                            for j in i:
                                if j.rect.collidepoint(event.pos):
                                    if event.button == 1:
                                        # If player left clicked of the grid
                                        self.openGrid += j.revealGrid()
                                        # Toggle flag off
                                        if j.flag:
                                            self.mineLeft += 1
                                            j.falg = False
                                        # If it's a mine
                                        if j.val == -1:
                                            # self.gameState = "Game Over"
                                            # self.revealAllMines()
                                            j.mineClicked = True
                                    elif event.button == 3:
                                        # If the player right clicked
                                        if not j.clicked:
                                            if j.flag:
                                                j.flag = False
                                                self.mineLeft += 1
                                            else:
                                                j.flag = True
                                                self.mineLeft -= 1                
                self.checkState()
                self.Draw()
    
    def checkState(self):
         # Check if won

        w = True
        for i in self.grid:
            for j in i:
                if j.val != -1 and not j.clicked:
                    w = False
                    if not self.allowGameOver:
                        return False
                elif j.val == -1 and j.clicked:
                    w = False
                    #print("Mineclick")
                    #print(self.allowGameOver)
                    if self.allowGameOver:
                     #   print("Game Over")
                        self.gameState = "Game Over"
                        self.revealAllMines()
                        gameDisplay.fill(bg_color)
                        self.Draw()
                    return False
        
        if w and self.gameState != "Exit":
            self.gameState = "Win"
            gameDisplay.fill(bg_color)
            self.Draw()
            return True
            
        gameDisplay.fill(bg_color)
        self.Draw()
        return False
        
        
        
    
    def Draw(self):
        # Draw Texts
        for i in self.grid:
            for j in i:
                j.drawGrid()
        if self.gameState != "Game Over" and self.gameState != "Win":
            self.t += 1
        elif self.gameState == "Game Over":
            if self.finalText:
                drawText("Game Over!", 50)
                drawText("R to restart", 35, 50)
            for i in self.grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            if self.finalText:
                drawText("You WON!", 50)
                drawText("R to restart", 35, 50)
        # Draw time
        s = str(self.t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(self.mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps
    def reset(self):
        self.grid = []  # The main grid
        self.mines = []  # Pos of the mines
        self.gameState = "Playing"  # Game state
        self.mineLeft = numMine  # Number of mine left
        self.t = 0  # Set time to 0
        self.openGrid = 0
            
    def wait(self): 
        # return
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return
    def renderAndWait(self):
        if self.allowStep:
            gameDisplay.fill(bg_color)
            self.Draw()
            if not self.auto:
                self.wait()
            

