import random
import tkinter as tk
import math
import ArrayLists
import swarmClass
import taskClass
import time as t
import threading

# Change this, if you want more robots.
## NOTE ONLY 7 PROCESSBOTS IS ALLOWED
productBots = 7 # These robots handle the products (eg. Bricks)
processBots = 7 # These robots contain the products (eg. Bricks)

# Variables. Dont touch
orderInfo = []
orderState = []

botID = 0
botTask = ''
botState = 0

# Pickerbots info
orderInfo.append(botID)         # The ID of the robot:    An integer defining the robot.
orderInfo.append(botTask)       # The task of the robot:  One could say the destination. 0-7 == colors. 8 == dropzone
orderInfo.append(botState)      # The state of the robot: 0 == inactive, 1 == pickup, 2 == dropoff

for i in range(productBots):
    orderState.append(orderInfo)

# FDP - Means; For Debugging Purposes
print(orderState)

# Cooperation with ROS
swarmClass.CreateProductBot(productBots)
swarmClass.CreateProcessBot(processBots)
#swarmClass.MakeBotLaunch()
taskClass.AmountBricks()

# Simulation variables
widthBase = 1920
heightBase = 1080

root = tk.Tk()

root.title('Fleet Visualizer')
root.geometry('1920x1080')

canvas = tk.Canvas(root, height=widthBase, width=heightBase)
canvas.pack()
frame = tk.Frame(root, bg='#04050f')
frame.place(relwidth=1, relheight=1)

bricks = ArrayLists.arrayAvailableColor

pickers = ArrayLists.arrayOfProd

object = bricks + pickers

inventory = ArrayLists.arrayAvailableBricks

bagSample1 = []
for i in range(random.randint(1,processBots)):
    bagSample1.append([(random.randint(1,6),ArrayLists.arrayAvailableColor[i])])

print(bagSample1)


# Spawn Deploy-Robot positions at random locations
def spawnDeploy():
    for i in range(len(bricks)):
        bricks[i] = [str(bricks[i]), round(random.uniform(100,widthBase-100),1), round(random.uniform(100,heightBase-100),1)]

    for i in range(len(pickers)):
        pickers[i] = [str(pickers[i]), round(random.uniform(100, widthBase-100), 1), round(random.uniform(100, heightBase-100), 1)]

# Create Deploy-Robots and Picker-bots in view
def positionDeploy(labels, bricks, pickers):

    for i in range(len(bricks)):
        label = tk.Label(frame, bg=bricks[i][0], text=str(inventory[i]))
        label.place(anchor='c', x=round(bricks[i][1]), y=round(bricks[i][2]), width=20, height=20)
        labels.append(label)


    for i in range(len(pickers)):
        label = tk.Label(frame, bg='white')
        label.place(anchor='c', x=round(pickers[i][1]), y=round(pickers[i][2]), width=10, height=10)
        labels.append(label)

    return labels

# Create Deploy-Station for product delivery and process refill
def crtDeployStation(labels, orderstate):

    deploy = [0,0,0,0]
    refill = [0,0,0,0]

    label = tk.Label(frame, bg='white', text='Deploy', font=("Samsung Sharp Sans", 13, "bold"))
    label.place(anchor='c', x=widthBase - 50, y=heightBase / 2, width=100, height=400)
    labels.append(label)

    label = tk.Label(frame, bg='white', text='Refill', font=("Samsung Sharp Sans", 13, "bold"))
    label.place(anchor='c', x=50, y=heightBase / 2, width=100, height=400)
    labels.append(label)

    # We want 4 sub-stations at each station.
    # These are for refilling and dropoffs

    for i in range(len(deploy)):

        if deploy[i] == 1:
            txt = 'OCPB {}'
            col = '#db2e3c'
            label = tk.Label(frame, bg=col)
            label.place(anchor='c', x=widthBase - 75 - 35, y=heightBase / 2 - 325 / 2 + (325 / 3) * i - 16, width=20, height=18)
            labels.append(label)
            label = tk.Label(frame, bg=col)
            label.place(anchor='c', x=widthBase - 75 - 35, y=heightBase / 2 - 325 / 2 + (325 / 3) * i + 16, width=20, height=18)
            labels.append(label)
        else:
            txt = 'AVAIL'
            col = '#20c94e'


        label = tk.Label(frame, bg=col, fg='white', text=txt.format("2"), font=("Samsung Sharp Sans", 9, "bold"))
        label.place(anchor='c', x=widthBase - 75, y=heightBase/2-325/2+(325/3)*i, width=50, height=50)
        labels.append(label)

    for i in range(len(refill)):

        if refill[i] == 1:
            txt = 'OCPB{}'
            col = '#d19a2c'
            label = tk.Label(frame, bg=col)
            label.place(anchor='c', x=75 + 35, y=heightBase / 2 - 325 / 2 + (325 / 3) * i - 20, width=20, height=10)
            labels.append(label)
            label = tk.Label(frame, bg=col)
            label.place(anchor='c', x=75 + 35, y=heightBase / 2 - 325 / 2 + (325 / 3) * i + 20, width=20, height=10)
            labels.append(label)
        else:
            txt = 'AVAIL'
            col = '#20c94e'


        label = tk.Label(frame, bg=col, fg='white', text=txt.format("1"), font=("Samsung Sharp Sans", 9, "bold"))
        label.place(anchor='c', x=75, y=heightBase/2-325/2+(325/3)*i, width=50, height=50)
        labels.append(label)

    return labels

# Calculate distance between bots
def checkDistance(p, p1):

    x1 = p[0]
    y1 = p[1]
    x2 = p1[0]
    y2 = p1[1]

    result = round((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)

    if result <= 100:
        return True
    else:
        return False

# Calculate direction to nearest bot
def checkDirection(targetCoord, robotCoord):
    xDist = targetCoord[0] - robotCoord[0]
    yDist = targetCoord[1] - robotCoord[1]

    dir = math.degrees(math.atan2(yDist, xDist))

    return dir

# Move bot away in direction
def moveBotinDir(direction, object, i):
    k = 0.15
    object[i][1] += math.cos(math.radians(direction)) * k
    object[i][2] += math.sin(math.radians(direction)) * k

# Do the above
def obstacleSafety(labels, object):
    object
    safetyDist = 25

    for i in range(len(object)):
        X = object[i][1]
        Y = object[i][2]

        for j in range(len(object)):
            if j != i:
                x = object[j][1] # X coordinate could round
                y = object[j][2] # Y coordinate

                txt = "The robot is too close? {} . Color is {}"
                result = checkDistance((x,y), (X,Y))
                if result == True:
                    #print(txt.format(result, str(object[j][0])))
                    moveBotinDir(checkDirection((X,Y),(x,y)), object, i)
    return object

def createProcedure(product):
    product[0].sort(reverse=True)

    procedure = []

    test = len(product)
    test = list(product[0][0])[1]

    totalBricks = 0
    for i in range(len(product)):
        procedure.append(list(product[i][0])[1])
        totalBricks += list(product[i][0])[0]
    #print(str(procedure) + " " + str(totalBricks))

    '''if totalBricks >= 3:
        procedure.insert(0,'Large')
    else:
        procedure.insert(0,'Small')'''

    return procedure

def moveToGoal(robot, robotCoord, targetCoord):
    k = 3
    xDist = targetCoord[0] - robotCoord[robot][1]
    yDist = targetCoord[1] - robotCoord[robot][2]

    robotCoord[robot][1] += math.cos(math.radians(math.degrees(math.atan2(yDist, xDist)))) * k
    robotCoord[robot][2] += math.sin(math.radians(math.degrees(math.atan2(yDist, xDist)))) * k





def swarmPlacement(procedure, object):
    target = []
    for i in range(len(procedure)):

        target.append((widthBase/2+i*20,heightBase/2))

        search = str(procedure[i])
        j = 0
        for sublists in object:
            if search in sublists:
                moveToGoal(j, object, target[i])
                #movePicker(target[i][0], target[i][1], j)
            j += 1

    #for i in range(len(pickers)):
    return

def movePickerinDir(direction, object, i):
    k = 2
    object[i][1] += round(math.cos(math.radians(direction)) * k,1)
    object[i][2] += round(math.sin(math.radians(direction)) * k,1)

def dirPicker(targetCoord, robotCoord):
    xDist = round(targetCoord[0] - robotCoord[0], 1)
    yDist = round(targetCoord[1] - robotCoord[1], 1)

    dir = round(math.degrees(math.atan2(yDist, xDist)),2)


    return dir

def movePicker(x,y,i):
    movePickerinDir(dirPicker((x, y), ((pickers[i][1]), pickers[i][2])), pickers, i)

    xDist = x - pickers[i][1]
    yDist = y - pickers[i][2]

    #txt = "{} for Picker {} is in proximity"
    if -1 <= xDist <= 1 and -1 <= yDist <= 1:
        #print(txt.format("X and Y", i))
        return True
    else:
        return False


def pickerManagement(procedure):

    return


def ProdBotEat():
    job = len(bagSample1)
    order = ["Not Complete", "Not Complete", "Not Complete", "Not Complete", "Not Complete", "Not Complete",
             "Not Complete", ]
    while job != 0:
        newamount = 50  # ændre til hvor meget der kan være i the process robot
        for i in range(productBots):
            for j in range(len(bagSample1)):
                if int(list(bagSample1[j][0])[0]) > 0 and ArrayLists.State[j] == "Not Occupied" and order[j] == "Not Complete":
                    ArrayLists.State[j] = "Occupied"
                    u = getPosfromColor(str(list(bagSample1[j][0])[1]))

                    x1 = u[0]
                    y1= u[1]
                    movePicker(x1, y1, i)

                    #totalAmountOfColor = ArrayLists.arrayAvailableBricks[ArrayLists.arrayAvailableColor.index(ArrayLists.arrayOfBricks[j])]
                    #prodTaskHowManyOfColor = bagSample1[i][0][0]
                    #ArrayLists.arrayOfInv[i] += prodTaskHowManyOfColor
                    #newAmountAfterBrickGone = totalAmountOfColor - prodTaskHowManyOfColor
                    #ArrayLists.arrayAvailableBricks[ArrayLists.arrayAvailableColor.index(ArrayLists.arrayOfBricks[j])] = newAmountAfterBrickGone
                    #if ArrayLists.arrayAvailableBricks[ArrayLists.arrayAvailableColor.index(ArrayLists.arrayOfBricks[j])] < 5:  # ændre til det antal bricks der skal til for en ordre
                    #    ArrayLists.arrayAvailableBricks[ArrayLists.arrayAvailableColor.index(ArrayLists.arrayOfBricks[j])] = newamount
                    job -= 1
                    ArrayLists.State[j] = "Not Occupied"
                    order[j] = "Complete"

def getPosfromColor(color):
    object = pickers + bricks
    search = str(color)
    j = 0
    pos = []
    for sublists in object:
        if search in sublists:
            pos.append(object[j][1])
            pos.append(object[j][2])
            # movePicker(target[i][0], target[i][1], j)
        j += 1
    return pos


spawnDeploy()


## Processkrav
# 1. Deploybots kan ikke overlevere items
# 2. Items skal overleveres af Pickerbots
# 3. Items skal i bags
# 4. Small bag <= 2 < Large bag
# 5. Securitydistance på radius 20 pixels omkring robotterne
# 6. Products skal leveres til deploystation


# Waiting pos:
x1 = widthBase-200
y1 = heightBase/2 + 50

# Deploy pos:
xDeploy = widthBase - 110
yDeploy1 = heightBase / 2 - 325 / 2 + (325 / 3) * 0
yDeploy2 = heightBase / 2 - 325 / 2 + (325 / 3) * 1
yDeploy3 = heightBase / 2 - 325 / 2 + (325 / 3) * 2
yDeploy4 = heightBase / 2 - 325 / 2 + (325 / 3) * 3



k = 0

while True:
    labels = []

    positionDeploy(labels, bricks, pickers)

    crtDeployStation(labels, orderState)

    ## Obstacle / Safety Avoidance
    procedure = createProcedure(bagSample1)

    troels = obstacleSafety(labels,bricks)

    swarmPlacement(procedure,troels)

    pickerManagement(procedure)


    print(procedure)

    for i in range(len(procedure)):
        x, y = getPosfromColor(procedure[i])
        movePicker(x,y,i)


    root.update()

    for label in labels:
        label.destroy()
