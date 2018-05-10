import pygame
import time
from noise import pnoise2
from random import randint
from PIL import Image, ImageDraw
pygame.init()
pygame.font.init()
done = False


menuX = 0
menuY = 0

# Important Variables
offX = randint(-5000000, 5000000)
offY = randint(-5000000, 5000000)
#offX = 5
#offY = 0
winWidth = 1280
winHeight = 720
clock = pygame.time.Clock()
screen = pygame.display.set_mode((winWidth, winHeight))
font = pygame.font.SysFont('Times New Roman MS',30)
menuPos = -1
MaxX = 130 # Max X
MaxY = 130 # Max Y
size = MaxX * MaxY
tileSize = 10
focusSize = 10

clicked = False

wood = 100
stone = 100
food = 100
metal = 0
pop = 1
gold = 0

inventory = [100,100,100,0,0,0]
#           Wood,Stone,Food,Copper,Tin,Iron
focusX = 0
focusY = 0

land = []
oreGEN = []

showGrid = False

# Constants
WATER = 0
SAND = 1
GRASS = 2
FOREST = 3
MOUNTAIN = 4

COLORS = [(46, 164, 223), (180,160,140), (82, 127, 25), (53, 76, 25), (230, 230, 230)]
LABELS = ["Water", "Sand", "Grass", "Forest", "Mountain"]

SelectImage = pygame.image.load("img/Cursor2.png")
landImg = pygame.image.load("img/Selection.png")
WoodIcon = pygame.image.load("img/WoodIcon.png")
StoneIcon = pygame.image.load("img/StoneIcon.png")
FoodIcon = pygame.image.load("img/FoodIcon.png")
MetalIcon = pygame.image.load("img/MetalIcon.png")

""" 
---------------BUILDINGS----------------
Castle - 4x4
Farm - 2x2
Outpost = 3x3
House - 2x2
Mine = 2x2
Woodcutter's Camp- 2x2
Fishing Camp - 2x2
"""

MATERIAL_NAMES = ["Wood", "Stone", "Food", "Metal", "Gold", "Population"]
B_NAMES = ["Castle", "Farm", "House", "Mine", "Woodcutter's Camp", "Fishing Camp"]
B_FNAMES = ["Castle", "Barn", "House", "Mine", "WoodCamp", "FishHut"]
B_COSTS = [ 
        [10000, 5000, 8000, 500, 1000, 0],
        [500, 100, 0, 0, 5, 5],
        [100, 500, 250, 0, 50, 0],
        [100, 0, 500, 0, 10, 5],
        [10, 500, 250, 0, 5, 0],
        [250, 250, 50, 25, 25, 10]]

# Helper functions
def createImage():
    global landImg
    img = Image.new('RGB', (1280, 720), (0, 0, 0))
    pixels = img.load()
    '''
    for i in range(100):
        for j in range(72):
            landIndex = doubleToSingle(i, j)
            for k in range(10):
                for l in range(10):
                    pixels[i*10+k, j*10+l] = land[landIndex].color
            #pixels[i*10,j*10] = land[landIndex].color
        # pixels[imgX,imgY] = land[landIndex].color
    '''
    mult = 0.006
    for i in range(1280):
        for j in range(720):
            noise = pnoise2((i + (offX))*mult, (j + (offY))*mult)
            val = (noise+1)*50
            if not showGrid or (i % 10 != 0 and j % 10 != 0):
                pixels[i,j] = COLORS[getNoiseType(val)]
    img.save("img/Land.png", "PNG")
    landImg = pygame.image.load("img/Land.png")


def doubleToSingle(x, y):
    return (MaxX * y) + x

def singleToDouble(i):
    x = i % MaxX
    y = int(i / MaxY)
    return (x, y)


class Tile():
    def __init__(self, type):
        self.type = type
        self.color = COLORS[self.type]
        self.label = LABELS[self.type]
        self.buildingIndex = -1

def getNoiseType(noiseVal):
    if noiseVal > 80:
        TYPE = MOUNTAIN
    elif noiseVal > 60:
        TYPE = FOREST
    elif noiseVal > 40:
        TYPE = GRASS
    elif noiseVal > 35:
        TYPE = SAND
    else:
        TYPE = WATER
    return TYPE

def init():
    # Init the land
    mult = 0.06
    oremult = 0.5
    CopperX = randint(0, 5000)
    CopperY = randint(0, 5000)
    TinX = randint(0, 5000)
    TinY = randint(0, 5000)
    IronX = randint(0, 5000)
    IronY = randint(0, 5000)
    for i in range(MaxX*MaxY):
        X, Y = singleToDouble(i)
        noise = pnoise2((X + (offX/10.0))*mult, (Y + (offY/10.0))*mult)
        val = (noise+1)*50
        TYPE = getNoiseType(val)
        land.append(Tile(TYPE))

def renderTopBar():
    pygame.draw.rect(screen, (100,100,100), (0, 0, 1280, 40))
    woodText = font.render( str(wood),True,(255,255,255))
    stoneText = font.render(str(stone),True,(255,255,255))
    foodText = font.render(str(food),True,(255,255,255))
    metalText = font.render(str(metal),True,(255,255,255))
    popText = font.render('Population: ' + str(pop),True,(255,255,255))
    goldText = font.render('Gold: ' + str(gold),True,(255,255,255))

    screen.blit(woodText, (60, 12))
    screen.blit(stoneText, (150, 12))
    screen.blit(foodText, (240, 12))
    screen.blit(metalText, (340, 12))
    screen.blit(popText, (800, 12))
    screen.blit(goldText, (1000, 12))

def renderRightMenu():
    global menuPos
    global menuX
    global menuY
    global clicked
    global B_COSTS
    global B_NAMES
    X = int(menuX)
    Y = int(menuY)
    mouseX, mouseY = pygame.mouse.get_pos()
    """ 
    Castle - 4x4
    Farm - 2x2
    Outpost = 3x3
    House - 2x2
    Mine = 2x2
    Woodcutter's Camp- 2x2
    Fishing Camp - 2x2
    """
    castleText = font.render("Castle",True,(255,255,255))
    farmText = font.render("Farm",True,(255,255,255))
    outpostText = font.render("Outpost",True,(255,255,255))
    houseText = font.render("House",True,(255,255,255))
    mineText = font.render("Mine",True,(255,255,255))
    woodText = font.render("Wood",True,(255,255,255))
    fishText = font.render("Fish",True,(255,255,255))

    pygame.draw.rect(screen,(100,100,100),(X,Y,150,240))
    screen.blit(castleText, (X + 10, Y + 10))
    screen.blit(farmText, (X + 10, Y + 50))
    screen.blit(houseText, (X + 10, Y + 90))
    screen.blit(mineText, (X + 10, Y + 130))
    screen.blit(woodText, (X + 10, Y + 170))
    screen.blit(fishText, (X + 10, Y + 210))

    for i in range(7):
        pygame.draw.rect(screen, (0, 0, 0), (X, Y + (40*i), 150, 2))

    menuPos = int((mouseY - Y) / 40)
    if mouseX < menuX or mouseX > (menuX + 150):
        menuPos = -1
    if mouseY < menuY or mouseY > (menuY + 238):
        menuPos = -1

    # Pop-Up Bar
    if menuPos != -1 and menuPos < 6:
        buildText = font.render("[SPACE] BUILD", True, (0, 255, 0))
        buildingText = font.render(B_NAMES[menuPos], True, (0, 255, 0))
        pygame.draw.rect(screen, (100, 100, 100), (X+152, Y, 220, 240))
        pygame.draw.rect(screen, (0, 0, 0), (X+152, Y, 220, 2))
        pygame.draw.rect(screen, (0, 0, 0), (X+372, Y, 2, 240))
        pygame.draw.rect(screen, (0, 0, 0), (X+152, Y+240, 220, 2))
        pygame.draw.rect(screen, (0, 0, 0), (X+152, Y+40, 220, 2))
        screen.blit(buildingText, (X+160, Y+10))
        for i in range(1, 6):
            itemName = MATERIAL_NAMES[i] + ": " + str(B_COSTS[menuPos][i])
            screen.blit(font.render(itemName, True, (255, 255,255)), (X+160, Y + (25*i + 30)))

    # Borders
    pygame.draw.rect(screen, (0, 0, 0), (X, Y, 2, 240))
    pygame.draw.rect(screen, (0, 0, 0), (X+150, Y, 2, 240))

    # Focus Tile
    pygame.draw.rect(screen, (255, 0, 0), (focusX*10, focusY*10, 10, 10))

    pygame.display.update()


def renderBuildings():
    for i in range(MaxX * MaxY):
        if land[i].buildingIndex != -1:
            building = pygame.image.load("img/buildings/" + B_FNAMES[land[i].buildingIndex] + ".png")
            x, y = singleToDouble(i)
            screen.blit(building, (x*10, y*10))


def OnScreenRender():
    global clicked
    global menuX
    global menuY
    global focusX
    global focusY
    global menuPos
    global land
    

    if clicked:
        renderRightMenu()

    mouseX, mouseY = pygame.mouse.get_pos()
    X = int(mouseX/10)
    Y = int(mouseY/10)

    screen.fill((0,0,0))
    screen.blit(landImg,(0,0))
    renderBuildings()
    clock.tick(60)
    screen.blit(SelectImage,(X *10,Y *10))
    renderTopBar()
    screen.blit(WoodIcon,(30,4))
    screen.blit(StoneIcon,(120,4))
    screen.blit(FoodIcon,(210,4))
    screen.blit(MetalIcon,(300,4))
    posText = font.render('['+str(X)+','+str(Y)+']',True,(255,255,255))
    screen.blit(posText,(1200,10))
    landIndex = doubleToSingle(X, Y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                clicked = not clicked
                menuX = mouseX
                menuY = mouseY
                focusX = int(mouseX / 10)
                focusY = int(mouseY / 10)
            elif event.button == 1:
                if menuPos != -1:
                    ind = doubleToSingle(focusX, focusY)
                    land[ind].buildingIndex = menuPos


init()
createImage()
screen = pygame.display.set_mode((winWidth, winHeight))
done = False
while not done:
    OnScreenRender()
    pygame.display.update()
