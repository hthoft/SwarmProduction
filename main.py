import random
import tkinter as tk
import math

root = tk.Tk()

root.title('Fleet Visualizer')
root.geometry('500x500')

canvas = tk.Canvas(root, height=500, width=500)
canvas.pack()
frame = tk.Frame(root, bg='#04050f')
frame.place(relwidth=1, relheight=1)

bricks = \
    ['Red', 'Blue', 'Green', 'Yellow']
bags = \
    ['Small', 'Large']
pickers = \
    ['Johnny', 'Tonni']


bagSample1 = [(5,'Blue')]


# Spawn Deploy-Robot positions at random locations
def spawnDeploy():
    for i in range(len(bricks)):
        bricks[i] = [str(bricks[i]), round(random.uniform(100,400),1), round(random.uniform(100,400),1)]
    for i in range(len(bags)):
        bags[i] = [str(bags[i]), round(random.uniform(100, 400), 1), round(random.uniform(100, 400), 1)]
    for i in range(len(pickers)):
        pickers[i] = [str(pickers[i]), round(random.uniform(100, 400), 1), round(random.uniform(100, 400), 1)]

# Create Deploy-Robots and Picker-bots in view
def positionDeploy(labels, bricks, bags, pickers):
    for i in range(len(bricks)):
        label = tk.Label(frame, bg=bricks[i][0])
        label.place(anchor='c', x=bricks[i][1], y=bricks[i][2], width=20, height=20)
        labels.append(label)

    for i in range(len(bags)):
        label = tk.Label(frame, bg='grey', text=bags[i][0])
        label.place(anchor='c', x=bags[i][1], y=bags[i][2], width=40, height=30)
        labels.append(label)

    for i in range(len(pickers)):
        label = tk.Label(frame, bg='white')
        label.place(anchor='c', x=pickers[i][1], y=pickers[i][2], width=10, height=10)
        labels.append(label)

    return labels

# Create Deploy-Station for product delivery
def crtDeployStation(labels):
    label = tk.Label(frame, bg='white', text='Deploy')
    label.place(anchor='c', x=475, y=250, width=50, height=100)
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
def obstacleSafety(labels, object1, object2):
    object = object1 + object2

    safetyDist = 25

    for i in range(len(object)):
        X = round(object[i][1])
        Y = round(object[i][2])

        for j in range(len(object)):
            if j != i:
                x = object[j][1] # X coordinate
                y = object[j][2] # Y coordinate

                txt = "The robot is too close? {} . Color is {}"
                result = checkDistance((x,y), (X,Y))
                if result == True:
                    #print(txt.format(result, str(object[j][0])))
                    moveBotinDir(checkDirection((X,Y),(x,y)), object, i)
    return object



def createProcedure(product):
    product.sort(reverse=True)
    totalBricks = 0
    procedure = []
    for i in range(len(product)):
        for j in range(product[i][0]):
            totalBricks += 1
            procedure.append(product[i][1])
    print(procedure)

    if totalBricks >= 3:
        procedure.insert(0,'Large')
    else:
        procedure.insert(0,'Small')

    return procedure

def moveToGoal(robot, robotCoord, targetCoord):
    k = 0.4
    xDist = targetCoord[0] - robotCoord[robot][1]
    yDist = targetCoord[1] - robotCoord[robot][2]

    robotCoord[robot][1] += math.cos(math.radians(math.degrees(math.atan2(yDist, xDist)))) * k
    robotCoord[robot][2] += math.sin(math.radians(math.degrees(math.atan2(yDist, xDist)))) * k


def swarmPlacement(procedure, object):
    target = []
    for i in range(len(procedure)):

        target.append((425-(i*50),250))

        search = str(procedure[i])
        j = 0
        for sublists in object:
            if search in sublists:
                moveToGoal(j, object, target[i])
            j += 1

    #for i in range(len(pickers)):
    return


def movePickerinDir(direction, object, i):
    k = 0.6
    object[i][1] += math.cos(math.radians(direction)) * k
    object[i][2] += math.sin(math.radians(direction)) * k

def dirPicker(targetCoord, robotCoord):
    xDist = targetCoord[0] - robotCoord[0]
    yDist = targetCoord[1] - robotCoord[1]

    dir = math.degrees(math.atan2(yDist, xDist))

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



spawnDeploy()
print(bricks)

## Processkrav
# 1. Deploybots kan ikke overlevere items
# 2. Items skal overleveres af Pickerbots
# 3. Items skal i bags
# 4. Small bag <= 2 < Large bag
# 5. Securitydistance på radius 20 pixels omkring robotterne
# 6. Products skal leveres til deploystation


# Waiting pos:
x1 = 400
y1 = 295
x2 = 425
y2 = 295

while True:
    labels = []

    positionDeploy(labels, bricks, bags, pickers)
    crtDeployStation(labels)

    ## Obstacle / Safety Avoidance
    procedure = createProcedure(bagSample1)

    swarmPlacement(procedure,obstacleSafety(labels,bricks,bags))


    pickerManagement(procedure)
    movePicker(x1, y1, 0)

    movePicker(x2, y2, 1)





    root.update()

    for label in labels:
        label.destroy()