# Coursework 2 - Astroid game
# Screen Resolution 1280x720
# Spaceship sprite from
# https://www.clipartkey.com/view/iRhiwi_8-bit-spaceship-png-8-bit-spaceship-sprites/
# To enter cheat code press button in top left of menu and enter code "Shield"
# Re-enter same code to deactivate
# Restart program after saving
# Controls:
# Arrows to move
# Space bar to shoot
# 'p' to pause
# 'b' is boss key
# Text input through terminal


from tkinter import *
from random import randint
import re
import pickle


def cheat():
    # This function is to deflect astroids when the cheat code is enetered
    pos = canvas.coords(ship)
    pos.append(pos[0] + 150)
    pos.append(pos[1] + 150)
    pos.append(pos[0] - 100)
    pos.append(pos[1] - 100)
    for i in range(len(astroids)):
        a = canvas.coords(astroids[i])
        if pos[4] < a[2] and pos[2] > a[0] and pos[5] < a[3] and pos[3] > a[1]:
            if xvel > 0:
                if pos[0] < a[0]:
                    canvas.move(astroids[i], xvel, 0)
                    smallX[i] = xvel
                else:
                    canvas.move(astroids[i], -xvel, 0)
                    smallX[i] = -xvel
            elif xvel < 0:
                if pos[0] > a[0]:
                    canvas.move(astroids[i], xvel, 0)
                    smallX[i] = xvel
                else:
                    canvas.move(astroids[i], -xvel, 0)
                    smallX[i] = -xvel
            else:
                smallX[i] = -smallX[i]

            if yvel > 0:
                if pos[1] < a[1]:
                    canvas.move(astroids[i], 0, yvel)
                    smallY[i] = yvel
                else:
                    canvas.move(astroids[i], 0, -yvel)
                    smallY[i] = -yvel
            elif yvel < 0:
                if pos[1] > a[1]:
                    canvas.move(astroids[i], 0, yvel)
                    smallY[i] = yvel
                else:
                    canvas.move(astroids[i], 0, -yvel)
                    smallY[i] = -yvel
            else:
                smallY[i] = -smallY[i]

    for i in range(len(bigAstroids)):
        a = canvas.coords(bigAstroids[i])
        if pos[4] < a[2] and pos[2] > a[0] and pos[5] < a[3] and pos[3] > a[1]:
            if xvel > 0:
                if pos[0] < a[0]:
                    canvas.move(bigAstroids[i], xvel, 0)
                    bigX[i] = xvel
                else:
                    canvas.move(bigAstroids[i], -xvel, 0)
                    bigX[i] = -xvel
            elif xvel < 0:
                if pos[0] > a[0]:
                    canvas.move(bigAstroids[i], xvel, 0)
                    bigX[i] = xvel
                else:
                    canvas.move(bigAstroids[i], -xvel, 0)
                    bigX[i] = -xvel
            else:
                bigX[i] = -bigX[i]

            if yvel > 0:
                if pos[1] < a[1]:
                    canvas.move(bigAstroids[i], 0, yvel)
                    bigY[i] = yvel
                else:
                    canvas.move(bigAstroids[i], 0, -yvel)
                    bigY[i] = -yvel
            elif yvel < 0:
                if pos[1] > a[1]:
                    canvas.move(bigAstroids[i], 0, yvel)
                    bigY[i] = yvel
                else:
                    canvas.move(bigAstroids[i], 0, -yvel)
                    bigY[i] = -yvel
            else:
                bigY[i] = -bigY[i]


def saveGame():
    # This function saves the game in the current state
    # It saves it in a seperate file
    position = canvas.coords(ship)
    APos = []
    BAPos = []
    BPos = []
    ALen = len(astroids)
    BALen = len(bigAstroids)
    BLen = len(bullets)
    for i in range(len(astroids)):
        APos.append(canvas.coords(astroids[i]))
    for i in range(len(bigAstroids)):
        BAPos.append(canvas.coords(bigAstroids[i]))
    for i in range(len(bullets)):
        BPos.append(canvas.coords(bullets[i]))
    with open("save", "wb") as f:
        pickle.dump([xvel, yvel, score, BPos, bullDir, level,
                    bigX, bigY, smallX, smallY, BAPos, APos, position,
                    direction, ALen, BALen, BLen], f)
    clearCanvas()
    canvas.delete(pauseText, scoreText)
    canvas.create_text(width/2, height/2, fill="white",
                       font="Times 60 bold", text="Game saved!")
    window.after(3000, menu)


def loadGame():
    # This function will check if there is a save file
    # And will load it in if there is one
    global xvel, yvel, score, bullets, bullDir, level, bigX
    global bigY, smallX, smallY, bigAstroids, astroids, position
    global direction, ship, scoreText, colours, pause
    canvas.delete(header)
    canvas.delete(newGameWindow)
    canvas.delete(leaderWindow)
    canvas.delete(loadWindow)
    canvas.delete(quitWindow)
    canvas.delete(codeWindow)
    colours = ["#A59692", "#5a554c", "#767676", "#93928c"]
    bigAstroids = []
    astroids = []
    bullets = []
    pause = False
    resume = True
    countdown = 3
    if 'pauseText' in globals():
        pauseText = canvas.create_text(width/2, height/4, fill="white",
                                       font="Times 40 italic bold",
                                       text="")
    if 'countdownText' in globals():
        countdownText = canvas.create_text(width/2, height/2 - 25,
                                           fill="white",
                                           font="Times 100 italic bold",
                                           text="")

    try:
        with open("save", "rb") as f:
            xvel, yvel, score, BPos, bullDir, level, bigX, bigY,
            smallX, smallY, BAPos, APos, position, direction, ALen,
            BALen, BLen = pickle.load(f)
        txt = "Score: " + str(score)
        scoreText = canvas.create_text(width/2, 20, fill="white",
                                       font="Times 20 italic bold",
                                       text=txt)
        if direction == "left":
            ship = canvas.create_image(position[0], position[1],
                                       anchor=NW, image=shipLeft)
        elif direction == "right":
            ship = canvas.create_image(position[0], position[1],
                                       anchor=NW, image=shipRight)
        elif direction == "up":
            ship = canvas.create_image(position[0], position[1],
                                       anchor=NW, image=shipUp)
        elif direction == "down":
            ship = canvas.create_image(position[0], position[1],
                                       anchor=NW, image=shipDown)

        for i in range(ALen):
            c = randint(0, 3)
            xy = (APos[i][0], APos[i][1], APos[i][2], APos[i][3])
            astroids.append(canvas.create_oval(xy, fill=colours[c]))
        for i in range(BALen):
            c = randint(0, 3)
            xy = (BAPos[i][0], BAPos[i][1], BAPos[i][2], BAPos[i][3])
            bigAstroids.append(canvas.create_oval(xy, fill=colours[c]))
        for i in range(BLen):
            xy = (BPos[i][0], BPos[i][1], BPos[i][2], BPos[i][3])
            bullets.append(canvas.create_oval(xy, fill="red"))
        window.after(100, moveShip)
    except Exception as e:
        print(e)
        canvas.create_text(width/2, height/2, fill="white",
                           font="Times 60 bold", text="Save file not found!")
        window.after(3000, menu)


def leaderboard(placed=-2):
    # This function displays the leaderboard
    # It will highlight the newest entry after a game
    if placed == -2:
        canvas.delete(header)
        canvas.delete(newGameWindow)
        canvas.delete(leaderWindow)
        canvas.delete(loadWindow)
        canvas.delete(quitWindow)
        canvas.delete(codeWindow)
    highscores = []
    names = []
    file = open("leaderboard.txt")
    raw_scores = file.read().strip().split('\n')
    file.close()

    for score in raw_scores:
        score_split = score.split(",")
        highscores.append(int(score_split[1]))
        names.append(score_split[0])

    highScoresText = []
    nameText = []
    rank = ["1ST", "2ND", "3RD", "4TH", "5TH", "6TH", "7TH", "8TH", "9TH",
            "10TH"]
    rankText = []
    leaderboardText = canvas.create_text(width/2, 75, fill="white",
                                         font="Times 60 bold",
                                         text="HIGH SCORES")
    rankText.append(canvas.create_text(width/4, 150, fill="white",
                    font="Times 30 bold", text="RANK"))
    nameText.append(canvas.create_text(width/2, 150, fill="white",
                    font="Times 30 bold", text="NAME"))
    highScoresText.append(canvas.create_text(3*width/4, 150,
                          fill="white", font="Times 30 bold",
                          text="SCORE"))
    for i in range(len(rank)):
        if placed == i:
            rankText.append(canvas.create_text(width/4, 220 + 50*i,
                            fill="yellow", font="Times 30 bold",
                            text=rank[i]))
        else:
            rankText.append(canvas.create_text(width/4, 220 + 50*i,
                            fill="white", font="Times 30 bold",
                            text=rank[i]))
    for i in range(len(names)):
        if placed == i:
            nameText.append(canvas.create_text(width/2, 220 + 50*i,
                            fill="yellow", font="Times 30 bold",
                            text=names[i]))
        else:
            nameText.append(canvas.create_text(width/2, 220 + 50*i,
                            fill="white", font="Times 30 bold",
                            text=names[i]))
    for i in range(len(highscores)):
        if placed == i:
            highScoresText.append(canvas.create_text(3*width/4,
                                  220 + 50*i, fill="yellow",
                                  font="Times 30 bold",
                                  text=highscores[i]))
        else:
            highScoresText.append(canvas.create_text(3*width/4,
                                  220 + 50*i, fill="white",
                                  font="Times 30 bold",
                                  text=highscores[i]))
    if placed == -1:
        sorry = canvas.create_text(
            width/2, height-15, fill="yellow",
            font="Times 15 bold",
            text="Unlucky, you didn't get a top ten score!")
    window.after(5000, menu)


def addLeaderboard():
    # This function checks if the score is a top ten score
    # If it is it gets added to the text file
    highscores = []
    names = []
    file = open("leaderboard.txt")
    raw_scores = file.read().strip().split('\n')
    file.close()

    for scores in raw_scores:
        score_split = scores.split(",")
        highscores.append(int(score_split[1]))
        names.append(score_split[0])
    placed = -1
    for i in range(len(highscores)):
        if score > highscores[i]:
            highscores.insert(i, score)
            placed = i
            break
    if placed != -1:
        highscores.pop()
        names.pop()
        prompt = canvas.create_text(
            width/2, height/2+100,
            fill="white", font="Times 15 bold",
            text="Please enter your initials in the terminal!")
        regex = "\A[A-Z]{3}\Z"
        while True:
            initials = input(
                "Please enter your initials in the AAA format: ")
            if (re.search(regex, initials)):
                break
        names.insert(placed, initials)
    file = open("leaderboard.txt", "w")
    for i in range(len(highscores)):
        file.write(names[i] + "," + str(highscores[i]) + "\n")
    file.close()
    canvas.delete(gameOverTxt)
    canvas.delete(scoreText)
    if 'prompt' in locals():
        canvas.delete(prompt)
    leaderboard(placed)


def newSmallAstroid(position):
    # Adds a new small astroid at least a certain distance from the ship
    c = randint(0, 3)
    small = 20
    smallX.append(randint(-15-level, 15+level))
    smallY.append(randint(-10-level, 10+level))
    while True:
        x = randint(small, width-small)
        y = randint(small, height-small)
        if (x > (position[2] + 200) or
                x < (position[0] - 200) or
                y > (position[1] + 200) or
                y < (position[3] - 200)):
            break

    xy = (x, y, x+small, y+small)
    astroids.append(canvas.create_oval(xy, fill=colours[c]))


def newBigAstroid(position):
    # Adds a big astroid at least a certain distance from the ship
    c = randint(0, 3)
    big = 50
    bigX.append(randint(-10, 10))
    bigY.append(randint(-5, 5))
    while True:
        x = randint(big, width-big)
        y = randint(big, height-big)
        if (x > (position[2] + 200) or
                x < (position[0] - 200) or
                y > (position[1] + 200) or
                y < (position[3] - 200)):
            break

    xy = (x, y, x+big, y+big)
    bigAstroids.append(canvas.create_oval(xy, fill=colours[c]))


def overlapping(a, b):
    # Checks if two objects are overlapping
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False


def moveBullets():
    # Controls the movement of bullets
    # Also checks if a bullet has hit an astroid
    # If it has then it will remove the bullet and astroid
    global score
    popcount = 0
    for i in range(len(bullets)):
        if len(bullets) != 0:
            if bullDir[i-popcount] == "left":
                canvas.move(bullets[i-popcount], -30, 0)
            elif bullDir[i-popcount] == "right":
                canvas.move(bullets[i-popcount], 30, 0)
            elif bullDir[i-popcount] == "up":
                canvas.move(bullets[i-popcount], 0, -30)
            elif bullDir[i-popcount] == "down":
                canvas.move(bullets[i-popcount], 0, 30)

            pos = canvas.coords(bullets[i-popcount])
            if pos[3] > height or pos[1] < 0:
                canvas.delete(bullets[i-popcount])
                bullets.pop(i-popcount)
                bullDir.pop(i-popcount)
                popcount += 1
            elif pos[0] < 0 or pos[2] > width:
                canvas.delete(bullets[i-popcount])
                bullets.pop(i-popcount)
                bullDir.pop(i-popcount)
                popcount += 1
            roidPop = 0
            for j in range(len(astroids)):
                if len(bullets) != 0:
                    pos = canvas.coords(astroids[j-roidPop])
                    if overlapping(pos, canvas.coords(
                                   bullets[i-popcount])):
                        canvas.delete(bullets[i-popcount])
                        bullets.pop(i-popcount)
                        bullDir.pop(i-popcount)
                        canvas.delete(astroids[j-roidPop])
                        astroids.pop(j-roidPop)
                        smallX.pop(j-roidPop)
                        smallY.pop(j-roidPop)
                        score += 20
                        txt = "Score: " + str(score)
                        canvas.itemconfigure(scoreText, text=txt)
                        roidPop += 1
                        popcount += 1

            bigRoidPop = 0
            for j in range(len(bigAstroids)):
                if len(bullets) != 0:
                    pos = canvas.coords(bigAstroids[j-bigRoidPop])
                    if overlapping(pos, canvas.coords(bullets[i-popcount])):
                        canvas.delete(bullets[i-popcount])
                        bullets.pop(i-popcount)
                        bullDir.pop(i-popcount)
                        canvas.delete(bigAstroids[j-bigRoidPop])
                        bigAstroids.pop(j-bigRoidPop)
                        bigX.pop(j-bigRoidPop)
                        bigY.pop(j-bigRoidPop)
                        score += 10
                        txt = "Score: " + str(score)
                        canvas.itemconfigure(scoreText, text=txt)
                        bigRoidPop += 1
                        popcount += 1


def makeBullet(position):
    # This function creates a bullet at the position of the ship
    xy = (position[0]+20, position[1]+20, position[0]+30, position[1]+30)
    bullets.append(canvas.create_oval(xy, fill="red"))
    bullDir.append(direction)


def moveAstroids():
    # This function moves the astroids
    # It bounces them off walls
    global width, height
    for i in range(len(astroids)):
        pos = canvas.coords(astroids[i])

        if pos[3] > height or pos[1] < 0:
            smallY[i] = -smallY[i]

        if pos[0] < 0 or pos[2] > width:
            smallX[i] = -smallX[i]

        canvas.move(astroids[i], smallX[i], smallY[i])

    for i in range(len(bigAstroids)):
        pos = canvas.coords(bigAstroids[i])

        if pos[3] > height or pos[1] < 0:
            bigY[i] = -bigY[i]

        if pos[0] < 0 or pos[2] > width:
            bigX[i] = -bigX[i]

        canvas.move(bigAstroids[i], bigX[i], bigY[i])


def paused():
    # This function is called when the game is paused
    # Displays paused and save button in top left
    global pauseText, saveWindow, saveButton
    txt = "paused"
    if 'pauseText' not in globals():
        pauseText = canvas.create_text(width/2, height/4, fill="white",
                                       font="Times 40 italic bold",
                                       text=txt)
        saveButton = Button(canvas, text="Save Game", font="Times 10",
                            bg="black", fg="white", command=saveGame)
    else:
        canvas.itemconfigure(pauseText, text=txt)
    if saveWindow == "":
        saveWindow = canvas.create_window(50, 20, window=saveButton)


def bossed():
    # This function is called when boss button is pressed
    # Displays a cover over the game
    global bossCover, bossText
    if 'bossCover' not in globals():
        bossCover = canvas.create_rectangle(0, 0, width, height, fill="white")
    else:
        canvas.itemconfigure(bossCover, fill="white")


def restart():
    # This function provides countdown when resuming game
    global countdownText
    if 'countdownText' not in globals():
        countdownText = canvas.create_text(width/2, height/2 - 25,
                                           fill="white",
                                           font="Times 100 italic bold",
                                           text=str(countdown))
    else:
        canvas.itemconfigure(countdownText, text=str(countdown))


def clearCanvas():
    # This function removes all moving objects from canvas
    canvas.delete(ship)
    for i in range(len(astroids)):
        canvas.delete(astroids[i])
    for i in range(len(bigAstroids)):
        canvas.delete(bigAstroids[i])
    if len(bullets) != 0:
        for i in range(len(bullets)):
            canvas.delete(bullets[i])


def moveShip():
    # This is the main function that is repeated when game is running
    # It calls all other functions that control movement of objects
    global xvel, yvel, score, shoot, countdown, resume, level, initials
    global gameOverTxt, saveWindow
    canvas.pack()
    if pause:
        paused()
        countdown = 3
    elif boss:
        bossed()
        countdown = 3
    elif resume:
        if 'pauseText' in globals():
            canvas.itemconfigure(pauseText, text="")
            if saveWindow != "":
                canvas.delete(saveWindow)
                saveWindow = ""
        if 'bossCover' in globals():
            canvas.itemconfigure(bossCover, fill='')
        if countdown != 0:
            restart()
            countdown += -1
        else:
            resume = False
            countdown = 3
            canvas.itemconfigure(countdownText, text="")
    else:
        position = []
        position = canvas.coords(ship)
        position.append(position[0] + 50)
        position.append(position[1] + 50)
        if position[0] < 0:
            canvas.coords(ship, width-shipSize, position[3])
        elif position[2] > width:
            canvas.coords(ship, 0+shipSize, position[1])
        elif position[3] > height:
            canvas.coords(ship, position[0], 0+shipSize)
        elif position[1] < 0:
            canvas.coords(ship, position[0], height-shipSize)
        position.clear()
        position = canvas.coords(ship)
        position.append(position[0] + 50)
        position.append(position[1] + 50)
        # Below controls movement of ship
        if direction == "left":
            canvas.itemconfig(ship, image=shipLeft)
            if xvel > -15:
                xvel += -5
            if yvel > 0:
                yvel += -1
            if yvel < 0:
                yvel += 1
            canvas.move(ship, xvel, yvel)
        elif direction == "right":
            canvas.itemconfig(ship, image=shipRight)
            if xvel < 15:
                xvel += 5
            if yvel > 0:
                yvel += -1
            if yvel < 0:
                yvel += 1
            canvas.move(ship, xvel, yvel)
        elif direction == "up":
            canvas.itemconfig(ship, image=shipUp)
            if yvel > -15:
                yvel += -5
            if xvel > 0:
                xvel += -1
            if xvel < 0:
                xvel += 1
            canvas.move(ship, xvel, yvel)
        elif direction == "down":
            canvas.itemconfig(ship, image=shipDown)
            if yvel < 15:
                yvel += 5
            if xvel > 0:
                xvel += -1
            if xvel < 0:
                xvel += 1
            canvas.move(ship, xvel, yvel)
        # Below controls scoring and increasing difficulty
        score += level
        if score % 50 == 0:
            newSmallAstroid(position)
        if score % 100 == 0:
            level += 1
            newBigAstroid(position)
        txt = "Score: " + str(score)
        canvas.itemconfigure(scoreText, text=txt)
        # Ends game if ship hits one of the astroids
        for i in range(len(astroids)):
            if overlapping(position, canvas.coords(astroids[i])):
                gameOver = True
        for i in range(len(bigAstroids)):
            if overlapping(position, canvas.coords(bigAstroids[i])):
                gameOver = True

        if shoot:
            # Player only gets 4 active bullets
            if len(bullets) < 4:
                makeBullet(position)
            shoot = False
        if len(bullets) > 0:
            moveBullets()
        # If cheat code entered - cheat function runs
        if shield:
            cheat()
        moveAstroids()
    if 'gameOver' not in locals():
        if resume:
            window.after(1000, moveShip)
        else:
            window.after(80, moveShip)
    else:
        clearCanvas()
        gameOverTxt = canvas.create_text(width/2, height/2-100, fill="white",
                                         font="Times 40 italic bold",
                                         text="Game Over!")
        canvas.coords(scoreText, width/2, height/2)
        canvas.itemconfigure(scoreText, font="Times 40 bold")
        window.after(5000, addLeaderboard)


def setAstroids(w, h):
    # This function sets positions and speed of astroids at start of game
    global bigX, bigY, smallX, smallY, bigAstroids, astroids, colours
    bigX = []
    bigY = []
    bigAstroids = []
    smallX = []
    smallY = []
    astroids = []
    colours = ["#A59692", "#5a554c", "#767676", "#93928c"]

    for i in range(15):
        c = randint(0, 3)
        small = 20
        smallX.append(randint(-15, 15))
        smallY.append(randint(-10, 10))
        while True:
            x = randint(small, w-small)
            y = randint(small, h-small)
            if (x > (3*w/4) or x < (w/4) or y > (3*h/4) or y < (h/4)):
                break

        xy = (x, y, x+small, y+small)
        astroids.append(canvas.create_oval(xy, fill=colours[c]))

    for i in range(5):
        c = randint(0, 3)
        big = 50
        bigX.append(randint(-10, 10))
        bigY.append(randint(-5, 5))
        while True:
            x = randint(big, w-big)
            y = randint(big, h-big)
            if (x > (3*w/4) or x < (w/4) or y > (3*h/4) or y < (h/4)):
                break

        xy = (x, y, x+big, y+big)
        bigAstroids.append(canvas.create_oval(xy, fill=colours[c]))


def newGame():
    # This function sets variables at start of new game
    global xvel, yvel, score, scoreText, bullets, bullDir, level, ship
    global pause, resume, countdown, pauseText, countdownText
    canvas.delete(header)
    canvas.delete(newGameWindow)
    canvas.delete(leaderWindow)
    canvas.delete(loadWindow)
    canvas.delete(quitWindow)
    canvas.delete(codeWindow)
    pause = False
    resume = True
    countdown = 3
    if 'pauseText' in globals():
        pauseText = canvas.create_text(width/2, height/4, fill="white",
                                       font="Times 40 italic bold",
                                       text="")
    if 'countdownText' in globals():
        countdownText = canvas.create_text(width/2, height/2 - 25,
                                           fill="white",
                                           font="Times 100 italic bold",
                                           text="3")
    xvel = 0
    yvel = 0
    bullets = []
    bullDir = []
    level = 1
    score = 0
    txt = "Score: " + str(score)
    ship = canvas.create_image((width/2)-25, (height/2)-25, anchor=NW,
                               image=shipUp)
    scoreText = canvas.create_text(width/2, 20, fill="white",
                                   font="Times 20 italic bold",
                                   text=txt)

    setAstroids(width, height)
    moveShip()


# The functions below are for when keys are pressed
def leftKey(event):
    global direction
    direction = "left"


def rightKey(event):
    global direction
    direction = "right"


def upKey(event):
    global direction
    direction = "up"


def downKey(event):
    global direction
    direction = "down"


def spaceKey(event):
    global shoot
    shoot = True


def pKey(event):
    global pause, resume
    if pause is False and boss is False:
        pause = True
    else:
        pause = False
        resume = True
        saveWindow = ""


def bossKey(event):
    global boss, resume
    if boss is False and pause is False:
        boss = True
    else:
        boss = False
        resume = True


def createBackground():
    # This function creates the background
    global canvas, width, height
    star = []
    c = ["white", "#fefefe", "#dfdfdf", "purple", "red", "blue", "yellow"]

    for i in range(200):
        x = randint(1, width-1)
        y = randint(1, height-1)
        size = randint(2, 4)
        f = randint(0, 6)
        xy = (x, y, x+size, y+size)
        tmp_star = canvas.create_oval(xy)
        canvas.itemconfig(tmp_star, fill=c[f])
        star.append(tmp_star)


def setWindowDimensions(w, h):
    # This function sets the screen dimensions for game window
    window = Tk()
    window.title("Astroid Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


def cheatCode():
    # This function allows user to enter cheat code into terminal
    global shield
    canvas.delete(header)
    canvas.delete(newGameWindow)
    canvas.delete(leaderWindow)
    canvas.delete(loadWindow)
    canvas.delete(quitWindow)
    canvas.delete(codeWindow)
    cheatHeader = canvas.create_text(width/2, height/2, fill="white",
                                     font="Times 60 bold",
                                     text="Enter code in terminal!")
    while True:
        code = input("Enter code or press <enter> to go back to menu: ")
        if code == "":
            window.after(1000, menu)
        elif code == "shield" or code == "Shield":
            if shield is False:
                shield = True
                canvas.delete(cheatHeader)
                canvas.create_text(width/2, height/2, fill="white",
                                   font="Times 60 bold",
                                   text="Shield Activated!")
                window.after(5000, menu)
                break
            else:
                shield = False
                canvas.delete(cheatHeader)
                canvas.create_text(width/2, height/2, fill="white",
                                   font="Times 60 bold",
                                   text="Shield Deactivated!")
                window.after(5000, menu)
                break
        else:
            print("Not valid code!")


def endProgram():
    # Closes window when called
    window.destroy()


def quit():
    # This function displays thanks for playing before window is closed
    canvas.delete(header)
    canvas.delete(newGameWindow)
    canvas.delete(leaderWindow)
    canvas.delete(loadWindow)
    canvas.delete(quitWindow)
    canvas.delete(codeWindow)
    canvas.create_text(width/2, height/2, fill="white",
                       font="Times 60 bold",
                       text="Thanks for playing!")
    window.after(2000, endProgram)


def menu():
    # This function displays menu
    global header, newGameWindow, leaderWindow, loadWindow
    global quitWindow, codeWindow
    canvas.delete("all")
    createBackground()
    direction = "up"
    shoot = False
    pause = False
    boss = False
    resume = True
    countdown = 3
    saveWindow = ""
    menuWindow = ""
    canvas.pack()
    header = canvas.create_text(width/2, height/4, fill="white",
                                font="Times 60 bold", text="ASTROIDS")
    newGameButton = Button(canvas, text="New Game", font="Times 20",
                           bg="black", fg="white", width=15, pady=15,
                           activebackground="#C0C0C0", command=newGame)
    newGameWindow = canvas.create_window(width/2, height/2-50,
                                         window=newGameButton)
    leaderButton = Button(canvas, text="Leaderboard", font="Times 20",
                          bg="black", fg="white", width=15, pady=15,
                          activebackground="#C0C0C0", command=leaderboard)
    leaderWindow = canvas.create_window(width/2, height/2+50,
                                        window=leaderButton)
    loadButton = Button(canvas, text="Load Game", font="Times 20",
                        bg="black", fg="white", width=15, pady=15,
                        activebackground="#C0C0C0", command=loadGame)
    loadWindow = canvas.create_window(width/2, height/2+150,
                                      window=loadButton)
    quitButton = Button(canvas, text="Quit", font="Times 20",
                        bg="black", fg="white", width=15, pady=15,
                        activebackground="#C0C0C0", command=quit)
    quitWindow = canvas.create_window(width/2, height/2+250,
                                      window=quitButton)
    codeButton = Button(canvas, text="Cheats", font="Times 10",
                        bg="black", fg="black", width=15, pady=15,
                        activebackground="#C0C0C0", command=cheatCode)
    codeWindow = canvas.create_window(30, 20, window=codeButton)


width = 1280
height = 720
window = setWindowDimensions(width, height)

canvas = Canvas(window, bg="black", width=width, height=height)

shipUp = PhotoImage(file="shipUp.png")
shipDown = PhotoImage(file="shipDown.png")
shipLeft = PhotoImage(file="shipLeft.png")
shipRight = PhotoImage(file="shipRight.png")

shipSize = 50
# Binds all keys used to functions
canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.bind("<space>", spaceKey)
canvas.bind("<p>", pKey)
canvas.bind("<b>", bossKey)
canvas.focus_set()

direction = "up"
shoot = False
pause = False
boss = False
resume = True
countdown = 3
saveWindow = ""
shield = False
# Menu is called entering loop
menu()
window.mainloop()
