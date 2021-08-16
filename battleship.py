import pygame
import time
import random

pygame.init() #initialize pygame

display_width = 800 #defining size of game window
display_height = 600

black = (0, 0, 0) #defining colors
white = (255, 255, 255)
blue = (0, 0, 255)
buttonGrey = (60, 60, 60)
buttonLightGrey = (160, 160, 160)
lightBlue=(95,158,160)
darkBlue=(57.6, 85.9, 92.5)
grey=(229,229,229)
navyBlue=(25,25,112)
red=(220,20,60)

gameDisplay = pygame.display.set_mode((display_width, display_height)) #open game window
pygame.display.set_caption('Battleship')
clock = pygame.time.Clock()

introImg = pygame.image.load('battleship.jpg')

boardX=10 #initialize board size
boardY=10

try:
    gameFile = open("playerInfo.txt", "r") #to check if file doesn't exist
except:
    file= open("playerInfo.txt", "w+") #creates file if it doesn't exist
    file.close()
else:
    gameFile.close()

def messageDisplay(text, color, x,y,size=20):
    """Displays the message at the given location in the given color.
    Input: text (string): Text to be displayed
           color (tuple): RGB color of text to be displayed
           x (int): x coordinate of the text to be displayed
           y (int): y coordinate of the text to be displayed
           size (int): size of text, default is 20
    Output: Displays the text.
    Return: --.
    """
    font = pygame.font.Font('freesansbold.ttf', size)
    displayText=font.render(text, True, color)
    gameDisplay.blit(displayText,(x,y)) #displays the given message

def button(msg, x, y, width, height, highlColor, unhighlColor, action=None):
    """Generates and displays the "button" on the game window, and performs action when button is clicked.
    Input: msg (string): text message to be displayed
           x (int): x coordinate of button
           y (int): y coordinate of button
           width (int): width of button
           height (int): height of button
           highlColor (tuple): highlighted color of button
           unhighlColor (tuple): unhighlighted color of button
           action (string): action performed by button; default None
    Output: Displays the buttons.
    Return: Return True if action is "click", otherwise no return.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, highlColor, (x, y, width, height))
        if click[0] == 1 and action != None: #check action when being clicked
            if action == "login":
                gameLogin()
            elif action == "create":
                gameCreate()
            elif action=="quit":
                pygame.quit()
                quit()
            elif action=="click":
                return True
            elif action=="instructions":
                Instructions()
            elif action=="back":
                gameIntro()

    else:
        pygame.draw.rect(gameDisplay, unhighlColor, (x, y, width, height))
    smallText = pygame.font.Font('freesansbold.ttf', 10)
    textSurface = smallText.render(msg, True, white)
    textRect = textSurface.get_rect()
    textRect.center = ((x+(width/2)),(y + (height/2)))
    gameDisplay.blit(textSurface, textRect)

def userVerification(username):
    """Verifies that the username doesn't already exist.
    Input: username (string): username input by user
    Output: None.
    Return: True if username already exists, False if it doesn't.
    """
    userExist=False #if user doesn't exist
    username=username.strip()
    gameFile = open("playerInfo.txt", "r")
    userContent = gameFile.readlines()
    for line in userContent:
        line=line.strip()
        words=line.split(" ")
        if words[0]==username:
            userExist=True #If user already exists
    gameFile.close()
    return userExist


def passwordVerification(passWord,userName):
    """Verifies if the password meets the required criteria.
    Input: passWord (string): password to be verified
           userName (string): username entered by the user
    Output: Displays the problems with the password.
    Return: True if the password is appropriate, otherwise returns nothing.
    """
    digit = False #initialize the different requirements
    containsUsername = True
    specialSym = False
    upperCase = False
    lowerCase = False
    length = False
    
    if (len(passWord) <= 8):
        messageDisplay("Password too short!", white, 250, 500)
        return
    else:
        length = True

    for char in passWord:
        if char.isdigit() == True:
                digit = True
        elif char.isupper() == True:
                upperCase = True
        elif char.islower()==True:
                lowerCase = True
        elif char in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                specialSym=True

    if userName not in passWord:
        containsUsername=False
            
    if digit == False:
        messageDisplay("Must contain a digit", white, 250, 500)
        return
    elif specialSym == False:
        messageDisplay("Must contain a special symbol", white, 250, 500)
        return
    elif upperCase == False:
        messageDisplay("Must contain an upper case letter", white, 250, 500)
        return
    elif lowerCase==False:
        messageDisplay("Must contain a lower case letter", white, 250, 500)
        return
    elif containsUsername==True:
        messageDisplay("Must not contain username", white, 250, 500)
        return

    return True #all criteria are met

def gameCreate():
    """Helps the user create an account.
    Input: None.
    Output: Displays the account creation window.
    Return: --
    """
    accCreation = True

    userName = ''
    passWord = ''
    dateOfBirth = ''
    gameDisplay.fill(black)
    messageDisplay("Username: ", white, 100, 50)
    messageDisplay("Password: ", white, 100, 100)
    messageDisplay("Date of Birth: ", white, 100, 150)
    messageDisplay("DDMMYYYY ", white, 100, 180)
    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
    pygame.draw.rect(gameDisplay, blue, (350, 100, 250, 35), 2)
    pygame.draw.rect(gameDisplay, blue, (350, 150, 250, 35), 2)
    messageDisplay("Password must be the following: ", white, 50, 240)
    messageDisplay("1. More than 8 characters ", white, 50, 270)
    messageDisplay("2. Contain at least one upper and lower case ", white, 50, 300)
    messageDisplay("3. Contain at least one digit and special symbol", white, 50, 330)
    messageDisplay("4. Cannot contain username",white,50,360)
    pygame.display.update()
    passState=dateState=userState=False

    while accCreation == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        button("Back", 700,10,30,20,buttonGrey,buttonLightGrey,'back')
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 600 > mouse[0] > 350 and 85 > mouse[1] > 50: #input username
            if click[0] == 1 :
                pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                pygame.display.update()
                userState=False
                while userState == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            keyPressed = pygame.key.get_pressed()
                            if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                userCheck=userVerification(userName) #check if username already exists
                                if userCheck==False:
                                    userState = True
                                    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
                                    pygame.draw.rect(gameDisplay, black, (250, 500, 350, 35))
                                    break
                                else:
                                    messageDisplay("User already exists", white, 250, 500)
                                    userName=""
                            elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                userName = userName[:-1]
                                pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                                pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                            elif event.unicode!="":
                                userName+=event.unicode
                            pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                            pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                            messageDisplay(userName, white, 360,60)
                            pygame.display.update()
                            
        if 600 > mouse[0] > 350 and 135 > mouse[1] > 100: #input password
            if click[0] == 1 and userState==True:
                pygame.draw.rect(gameDisplay, white, (350, 100, 250, 35), 2)
                pygame.display.update()
                passState=False
                while passState == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            keyPressed = pygame.key.get_pressed()
                            if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                pygame.draw.rect(gameDisplay, black, (250, 500, 500, 35))
                                pygame.display.update()
                                passCheck=passwordVerification(passWord,userName) #check if password is valid
                                if passCheck==True:
                                    passState = True
                                    pygame.draw.rect(gameDisplay, blue, (350, 100, 250, 35), 2)
                                    break
                                else:
                                    passWord=''
                            elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                passWord = passWord[:-1]
                                pygame.draw.rect(gameDisplay, black, (350, 100, 250, 35))
                                pygame.draw.rect(gameDisplay, white, (350, 100, 250, 35), 2)
                            elif event.unicode!="":
                                passWord+=event.unicode
                            pygame.draw.rect(gameDisplay, black, (350, 100, 250, 35))
                            pygame.draw.rect(gameDisplay, white, (350, 100, 250, 35), 2)
                            messageDisplay(passWord, white, 360,110)
                            pygame.display.update()
                            
            elif click[0]==1 and userState==False:
                    messageDisplay("Enter username first", white, 250, 500)
                            
        if 600 > mouse[0] > 350 and 185 > mouse[1] > 150: #input date of birth
            if click[0] == 1 :
                dateState=False
                while dateState == False:
                    pygame.draw.rect(gameDisplay, white, (350, 150, 250, 35), 2)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            keyPressed = pygame.key.get_pressed()
                            if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                if len(dateOfBirth)==8 and dateOfBirth.isnumeric()==True: #check if DOB is valid
                                    dateState = True
                                    pygame.draw.rect(gameDisplay, blue, (350, 150, 250, 35), 2)
                                    pygame.draw.rect(gameDisplay, black, (250, 500, 350, 35))
                                    break
                                else:
                                    messageDisplay("Invalid date of birth", white, 250, 500)
                                    dateOfBirth=''
                            elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                dateOfBirth = dateOfBirth[:-1]
                                pygame.draw.rect(gameDisplay, black, (350, 150, 250, 35))
                                pygame.draw.rect(gameDisplay, white, (350, 150, 250, 35), 2)
                            elif event.unicode!="":
                                dateOfBirth+=event.unicode
                            pygame.draw.rect(gameDisplay, black, (350, 150, 250, 35))
                            pygame.draw.rect(gameDisplay, white, (350, 150, 250, 35), 2)
                            messageDisplay(dateOfBirth, white, 360,160)
                            pygame.display.update()
        
        pygame.display.update()
        clock.tick(60)
        if passState==True and userState==True and dateState==True: #after all data has been entered
            check=button("Create Account",250, 500, 80, 25, buttonGrey, buttonLightGrey,'click')
            if check==True:
                gameFile = open("playerInfo.txt", "a")
                print(userName, file = gameFile, end = ' ')
                print(passWord, file = gameFile, end = ' ')
                print(dateOfBirth, file = gameFile)
                gameFile.close()
                accCreation = False     

def checkUser(username,password):
    """Checks if the username and password are correct.
    Input: username (string): username
           password (string): password for username
    Output: None.
    Return: 2 if username and password match, 1 if username exists but password doesn't match,
            0 if username doesn't exist
    """
    gameFile = open("playerInfo.txt", "r")
    userContent = gameFile.readlines()
    gameFile.close()
    playerDict = {}
    for text in userContent:
        text = text.strip()
        word = text.split(' ')
        playerDict[word[0]] = [word[1], word[2]]
        if word[0] == username and playerDict[word[0]][0] == password:
             return 2 #if username and password match
        elif word[0] == username:
            return 1 #username exists
    return 0 #username doesn't exist

def verifyDOB(username,dateOfBirth):
    """Verifies if the date of birth is correct for the given user
    Input: username (string): username to be checked for
           dateOfBirth (string): date of birth
    Output: None
    Return: True if DOB and username match, False otherwise
    """
    gameFile = open("playerInfo.txt", "r")
    userContent = gameFile.readlines()
    gameFile.close()
    playerDict = {}
    for text in userContent:
        text = text.strip()
        word = text.split(' ')
        playerDict[word[0]] = [word[1], word[2]]
        if word[0] == username and playerDict[word[0]][1] == dateOfBirth:
            return True #date of birth is correct
    return False #date of birth is incorrect
       

def gameLogin():
    """Displays the login screen.
    Input: None.
    Output: login screen
    Return: --
    """
    accLogin = True
    userName = ''
    passWord = ''
    gameDisplay.fill(black)
    messageDisplay("Username: ",white, 100,50)
    messageDisplay("Password: ", white,100,100)
    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
    pygame.draw.rect(gameDisplay, blue, (350, 100, 250, 35), 2)
    pygame.display.update()
    passState=userState=False
    noOfAttempts=0
        
    while accLogin == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        button("Back", 700,10,30,20,buttonGrey,buttonLightGrey,'back')
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 600 > mouse[0] > 350 and 85 > mouse[1] > 50: #input username
                if click[0] == 1:
                    pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                    pygame.display.update()
                    userState = False
                    while userState == False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                keyPressed = pygame.key.get_pressed()
                                if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                    userState = True
                                    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
                                    pygame.draw.rect(gameDisplay, black, (250, 500, 350, 35))
                                    break
                                elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                    userName = userName[:-1]
                                    pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                                    pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                                elif event.unicode!="":
                                    userName+=event.unicode
                                pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                                pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                                messageDisplay(userName,white,360,60)
                                pygame.display.update()


        if 600 > mouse[0] > 350 and 135 > mouse[1] > 100: #input password
            if click[0]==1:
                pygame.draw.rect(gameDisplay, white, (350, 100, 250, 35), 2)
                pygame.display.update()
                passState=False
                while passState == False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                keyPressed = pygame.key.get_pressed()
                                if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                    passState = True
                                    pygame.draw.rect(gameDisplay, blue, (350, 100, 250, 35), 2)
                                    pygame.draw.rect(gameDisplay, black, (250, 500, 350, 35))
                                    pygame.display.update()
                                    break
                                elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                    passWord = passWord[:-1]
                                    pygame.draw.rect(gameDisplay, black, (350, 100, 250, 35))
                                    pygame.draw.rect(gameDisplay, white, (350, 100, 250, 35), 2)
                                elif event.unicode!="":
                                    passWord+=event.unicode
                                messageDisplay(passWord,white,360,110)
                                pygame.display.update()
                  
        pygame.display.update()
        clock.tick(60)
        if passState==True and userState==True: #after all data has been entered
            check=button("Login",250, 300, 80, 25, buttonGrey, buttonLightGrey,'click')
            if check==True:
                pygame.draw.rect(gameDisplay, black, (250, 500, 450, 35))
                pygame.display.update()
                noOfAttempts+=1
                loginOrNot=checkUser(userName, passWord)
                if loginOrNot==2:
                    messageDisplay("Login Successful", white, 250, 500)
                    time.sleep(3)
                    gamePlay()
                elif noOfAttempts < 3 and loginOrNot == 1:
                    messageDisplay("Try again! "+str(3-noOfAttempts)+" attempt(s) remain(s)", white, 250, 500)
                    pygame.display.update()
                    time.sleep(0.5)
                elif loginOrNot==1 and noOfAttempts == 3:
                    lockDown(userName)
                    gameLogin()
                else: 
                    messageDisplay("Username doesn't exist", white, 400, 300)
                    pygame.display.update()
                    time.sleep(2)
                    gameLogin()
        
def lockDown(username):
    """Lockdown mode when the password is entered incorrectly 3 times.
    Input: username (string): username for which account is locked
    Output: displays the lockdown screen
    Return: --
    """
    dateOfBirth = ''
    lock=True
    gameDisplay.fill(black)
    messageDisplay("Date of birth: ", white, 100,50)
    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
    messageDisplay("LOCKDOWN MODE. Enter date of birth for user "+'"'+username+'"'+" to unlock", white, 40, 240)
    pygame.display.update()
    
    while lock==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 600 > mouse[0] > 350 and 85 > mouse[1] > 50: #input date of birth
            if click[0] == 1 :
                pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                pygame.display.update()
                while lock==True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            keyPressed = pygame.key.get_pressed()
                            if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                dateCheck=verifyDOB(username,dateOfBirth) #check if date of birth is correct
                                if dateCheck==True:
                                    lock=False
                                    pygame.draw.rect(gameDisplay, blue, (350, 50, 250, 35), 2)
                                    pygame.draw.rect(gameDisplay, black, (250, 500, 350, 35))
                                    break
                                else:
                                    messageDisplay("Incorrect date of birth", white, 250, 500)
                                    dateOfBirth=""
                            elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                dateOfBirth = dateOfBirth[:-1]
                                pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                                pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                            elif event.unicode!="":
                                dateOfBirth+=event.unicode
                            pygame.draw.rect(gameDisplay, black, (350, 50, 250, 35))
                            pygame.draw.rect(gameDisplay, white, (350, 50, 250, 35), 2)
                            messageDisplay(dateOfBirth, white, 360,60)
                            pygame.display.update()


def Instructions():
    """Displays the game instructions.
    Input: None
    Output: instructions
    Return: --
    """
    gameDisplay.fill(black)
    messageDisplay("Upon commencement of the game, the players will place a carrier (4units) and a submarine", white, 100,100,15)
    messageDisplay("(3units) on the playing board.", white, 100,115,15)
    messageDisplay("Players will take turns firing shots (by selecting a target coordinate) to attack the ", white, 100,170,15)
    messageDisplay("opponent's ships.", white, 100,185,15)
    messageDisplay("On your turn, enter the coordinates of attack. A 3x3 grid around that coordinate gets marked", white, 100,240,15)
    messageDisplay("on your targeting board, and the opponent's ship will be highlighted if it was hit.", white, 100,255,15)
    messageDisplay("On the computer’s turn, a random coordinate is targeted and the computer’s targeting ", white, 100,310,15)
    messageDisplay("board gets tagged similarly. ", white, 100,325,15)
    messageDisplay("The game ends when all the ships of one player are “tagged”.", white, 100,380,15)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Back", 700,10,30,20,buttonGrey,buttonLightGrey,'back')
        pygame.display.update()
        clock.tick(60)

def gameIntro():
    """Displays the intro screen of the game.
    Input: None.
    Output: Intro screen of the game.
    Return: --.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(introImg, (0, 0))
        button("Login", 200, 550, 80, 25, buttonGrey, buttonLightGrey, 'login')
        button("Create Account", 500, 550, 80, 25, buttonGrey, buttonLightGrey, 'create')
        button("Instructions", 350, 550, 80, 25, buttonGrey, buttonLightGrey, 'instructions')
        button("Quit", 760,10,30,20,buttonGrey,buttonLightGrey,'quit')
        pygame.display.update()
        clock.tick(60)

def displayGameboard():
    """Displays the battleship gameboard.
    Input: None.
    Output: Displays the board
    Return: --
    """
    pygame.draw.rect(gameDisplay, black, (0,0,800,75)) #displays the board
    pygame.draw.rect(gameDisplay, grey, (0,75,800,475))
    pygame.draw.rect(gameDisplay, white, (0,475,800,125))
    pygame.draw.rect(gameDisplay, lightBlue, (30,105,370,370))
    pygame.draw.rect(gameDisplay, darkBlue, (430,105,370,370))
    for i in range(30,400,37): #printing the grids
        pygame.draw.line(gameDisplay, buttonLightGrey,(i,105),(i,475))
    for i in range(430,800,37):
        pygame.draw.line(gameDisplay, buttonLightGrey,(i,105),(i,475))
    for i in range(105,505,37):
        pygame.draw.line(gameDisplay, buttonLightGrey,(30,i),(400,i))
    for i in range(105,505,37):
        pygame.draw.line(gameDisplay, buttonLightGrey,(430,i),(800,i))
    pygame.draw.line(gameDisplay, black, (400,75), (400,475))
    messageDisplay("BATTLESHIP", white, 260,17,45)
    messageDisplay("Surface (depth=1)", black,5,80,10)
    messageDisplay("Subsea (depth=0)", black,405,80,10)
    num=1
    for i in range(45,415,37):
        messageDisplay(str(num), black,i,95,10)
        num+=1
    num=1
    for i in range(445,815,37):
        messageDisplay(str(num), black, i,95,10)
        num+=1
    alph="A"
    for i in range(120,490,37):
        messageDisplay(alph,black,20,i,10)
        alph=chr(ord(alph)+1)
    alph="A"
    for i in range(120,490,37):
        messageDisplay(alph,black,420,i,10)
        alph=chr(ord(alph)+1)
    pygame.display.update()

    
def deployComp(compPlacement):
    """Deploys the ships randomly for the computer.
    Input: compPlacement (list): placement board for the computer
    Output: --
    Return: --
    """
    carrierDepth=1
    subDepth=random.randint(0,1)

    carrierLength=4
    subLength=3

    horiVert=random.randint(0,1) #0 is horizontal, 1 is vertical
    carrierOrient=horiVert
    horiVert=random.randint(0,1)
    subOrient=horiVert

    #placing submarine
    if subOrient==0: #horizontal
        subPosX=random.randint(0,7) #cannot be beyond column index 7
        subPosY=random.randint(0,9)
        for i in range(3):
            compPlacement[subDepth][subPosY][subPosX+i]=True
    else: #vertical
        subPosX=random.randint(0,9)
        subPosY=random.randint(0,7) #cannot be beyond row index 7
        for i in range(3):
            compPlacement[subDepth][subPosY+i][subPosX]=True
    
    #placing carrier
    if carrierDepth!=subDepth:
        if carrierOrient==0: #horizontal
            carrierPosX=random.randint(0,6) #cannot be beyond index 6
            carrierPosY=random.randint(0,9)
            for i in range(4):
                compPlacement[carrierDepth][carrierPosY][carrierPosX+i]=True
        else: #vertical
            carrierPosX=random.randint(0,9)
            carrierPosY=random.randint(0,6) #cannot be beyond index 6
            for i in range(4):
                compPlacement[carrierDepth][carrierPosY+i][carrierPosX]=True
    else:
        carrierPosX=0 #initialize so loop works
        carrierPosY=0
        if carrierOrient==0: #horizontal
            while True: 
                carrierPosX=random.randint(0,6) #cannot be beyond index 6
                carrierPosY=random.randint(0,9)
                if [compPlacement[carrierDepth][carrierPosY][carrierPosX],compPlacement[carrierDepth][carrierPosY][carrierPosX+1],
                   compPlacement[carrierDepth][carrierPosY][carrierPosX+2],compPlacement[carrierDepth][carrierPosY][carrierPosX+3]] ==[False,False,False,False]:
                    break
            for i in range(4):
                compPlacement[carrierDepth][carrierPosY][carrierPosX+i]=True
        else: #vertical
            while True:
                carrierPosX=random.randint(0,9)
                carrierPosY=random.randint(0,6) #cannot be beyond index 6
                if [compPlacement[carrierDepth][carrierPosY][carrierPosX],compPlacement[carrierDepth][carrierPosY+1][carrierPosX],
                   compPlacement[carrierDepth][carrierPosY+2][carrierPosX],compPlacement[carrierDepth][carrierPosY+3][carrierPosX]] ==[False,False,False,False]:
                    break
            for i in range(4):
                compPlacement[carrierDepth][carrierPosY+i][carrierPosX]=True

def userPlace(board, move,size):
    """Places ships for user and displays board.
    Input: board (list): user's placement board
           move (list): user's entered input
           size (int): size of ship
    Output: Display's user's placement board
    Return: ---
    """
    if move[3]==0: #updates user's placement board
        for i in range(size):
            board[move[0]][int(chr(ord(move[1])-17))][move[2]-1+i]=True
    else:
        for i in range(size):
            board[move[0]][int(chr(ord(move[1])-17))+i][move[2]-1]=True
    displayPlacementBoard(board) #displays it
    

def deployUser(board):
    """Deploys the ships for the user.
    Input: board (list): user's placement board
    Output: user input screen
    Return: --
    """
    messageDisplay("Enter coordinates for submarine (size 3) in the form (depth,row,column,orientation): ",black,50,500,17)
    messageDisplay("Orientation: horizontal=0, vertical=1",black,275,525,15)
    pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
    coord=''
    pygame.display.update()
    coordState=False
    subState=False
    
    while subState==False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if  525> mouse[0] > 275 and 575 > mouse[1] > 550: #input submarine coordinates
                if click[0] == 1:
                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                    pygame.display.update()
                    coordState = False
                    while coordState== False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                keyPressed = pygame.key.get_pressed()
                                if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                    try: #check if valid position
                                        move=coord.split(',')
                                        move[0]=int(move[0])
                                        move[1]=chr(ord(move[1]))
                                        move[2]=int(move[2])
                                        move[3]=int(move[3])
                                        if move[0] not in [0,1]:
                                            raise ValueError("incorrect depth")
                                        if move[3] not in [0,1]:
                                            raise Exception("")
                                        if move[3]==1:
                                            if move[2]<1 or move[2]>10:
                                                raise IndexError("out of bounds")
                                            if move[1]<'A' or move[1]>'G':
                                                raise IndexError("out of bounds")
                                        else:
                                            if move[2]<1 or move[2]>7:
                                                raise IndexError("out of bounds")
                                            if move[1]<'A' or move[1]>'J':
                                                raise IndexError("out of bounds")
                                    except IndexError:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Out of bounds.",black,575,550,15)
                                    except ValueError:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Incorrect depth.",black,575,550,15)
                                    except Exception:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Incorrect orientation.",black,575,550,15)
                                    except:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Not possible.",black,575,550,15)
                                    else:
                                        coordState = True
                                        pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                        pygame.draw.rect(gameDisplay, white, (570, 530, 250, 50))
                                        pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
                                        pygame.display.update()
                                        userPlace(board,move,3)
                                        subState=True
                                        break
                                elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                    coord = coord[:-1]
                                    pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                elif event.unicode!="":
                                    coord+=event.unicode
                                pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                messageDisplay(coord,black,290,555,13)
                                pygame.display.update()

        clock.tick(60)

    pygame.draw.rect(gameDisplay, white, (0,475,800,125))
    messageDisplay("Enter coordinates for carrier (size 4) (depth must be 1) in the form (depth,row,column,orientation): ",black,40,500,16)
    messageDisplay("Orientation: horizontal=0, vertical=1",black,275,525,15)
    pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
    coord=''
    pygame.display.update()
    coordState=False
    carrierState=False
    
    while carrierState==False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if  525> mouse[0] > 275 and 575 > mouse[1] > 550: #input carrier coordinates
                if click[0] == 1:
                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                    pygame.display.update()
                    coordState = False
                    while coordState== False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                keyPressed = pygame.key.get_pressed()
                                if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                    try: #check if valid position
                                        move=coord.split(',')
                                        move[0]=int(move[0])
                                        move[1]=chr(ord(move[1]))
                                        move[2]=int(move[2])
                                        move[3]=int(move[3])
                                        if move[0]!=1:
                                           raise ValueError("")
                                        if move[3] not in [0,1]:
                                            raise KeyError("")
                                        if move[3]==1:
                                            if move[2]<1 or move[2]>10:
                                                raise IndexError("")
                                            if move[1]<'A' or move[1]>'H':
                                                raise IndexError("")
                                            if ([board[1][int(chr(ord(move[1])-17))][move[2]-1],board[1][int(chr(ord(move[1])-17))+1][move[2]-1],
                                                board[1][int(chr(ord(move[1])-17))+2][move[2]-1],board[1][int(chr(ord(move[1])-17))+3][move[2]-1]] != [False,False,False,False]) and (move[0]==1):
                                                raise Exception("")
                                        else:
                                            
                                            if move[2]<1 or move[2]>8:
                                                raise IndexError("")
                                            if move[1]<'A' or move[1]>'J':
                                                raise IndexError("")
                                            if ([board[1][int(chr(ord(move[1])-17))][move[2]-1],board[1][int(chr(ord(move[1])-17))][move[2]],
                                                board[1][int(chr(ord(move[1])-17))][move[2]+1],board[1][int(chr(ord(move[1])-17))][move[2]+2]] != [False,False,False,False]) and (move[0]==1):
                                                raise Exception("") 
                                    except IndexError:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Out of bounds.",black,575,550,15)
                                    except ValueError:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Incorrect depth.",black,575,550,15)
                                    except KeyError:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Incorrect orientation.",black,575,550,15)
                                    except Exception:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Cannot overlap.",black,575,550,15)
                                    except:
                                        pygame.draw.rect(gameDisplay, white, (570,540, 250, 25))
                                        pygame.display.update()
                                        messageDisplay("Not possible.",black,575,550,15)
                                    else:
                                        coordState = True
                                        pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                        pygame.draw.rect(gameDisplay, white, (570, 530, 250, 50))
                                        pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
                                        pygame.display.update()
                                        userPlace(board,move,4)
                                        carrierState=True
                                        break
                                elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                    coord = coord[:-1]
                                    pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                elif event.unicode!="":
                                    coord+=event.unicode
                                pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                messageDisplay(coord,black,290,555,13)
                                pygame.display.update()

        clock.tick(60)

def displayPlacementBoard(board):
    """Displays the given placement board on the pygame window.
    Input: board (list): placement board
    Output: Displays the ships on the board
    Return: --
    """
    indexY=0 #display surface
    for row in board[1]:
        indexX=0
        for box in row:
            if box==True:
                pygame.draw.rect(gameDisplay, navyBlue, (30+(indexX*37),105+(indexY*37),37,37))
                pygame.display.update()
            indexX+=1
        indexY+=1

    indexY=0 #display subsea
    for row in board[0]:
        indexX=0
        for box in row:
            if box==True:
                pygame.draw.rect(gameDisplay, navyBlue, (430+(indexX*37),105+(indexY*37),37,37))
                pygame.display.update()
            indexX+=1
        indexY+=1

    pygame.display.update()

def displayTargetBoard(board):
    """Displays the target board.
    Input: board (list): the targeting board
    Output: targeting board is displayed in pygame
    Return: --
    """
    indexY=0 #display surface
    for row in board[1]:
        indexX=0
        for box in row:
            if box=="hit":
                pygame.draw.rect(gameDisplay, red, (30+(indexX*37),105+(indexY*37),37,37))
                pygame.display.update()
            elif box==True:
                pygame.draw.line(gameDisplay, red,(30+(indexX*37),105+(indexY*37)),(30+(indexX*37)+37,105+(indexY*37)+37))
                pygame.draw.line(gameDisplay, red,(30+(indexX*37),105+(indexY*37)+37),(30+(indexX*37)+37,105+(indexY*37)))
                pygame.display.update()
            indexX+=1
        indexY+=1

    indexY=0 #display subsea
    for row in board[0]:
        indexX=0
        for box in row:
            if box=="hit":
                pygame.draw.rect(gameDisplay, red, (430+(indexX*37),105+(indexY*37),37,37))
                pygame.display.update()
            elif box==True:
                pygame.draw.line(gameDisplay, red,(430+(indexX*37),105+(indexY*37)),(430+(indexX*37)+37,105+(indexY*37)+37))
                pygame.draw.line(gameDisplay, red,(430+(indexX*37),105+(indexY*37)+37),(430+(indexX*37)+37,105+(indexY*37)))
                pygame.display.update()
            indexX+=1
        indexY+=1

    pygame.display.update()

def attackUpdate(userTarget, compPlacement,move):
    """Updates the user's targeting board
    Input: userTarget (list): user's targeting board
           compPlacement (list): computer's placement board
           move (list): user's input
    Output: None
    Return: --
    """
    if move[1]in['A','J'] and move[2]in[1,10]: #special cases
        if move[1]=='A' and move[2]==1:
            userTarget[move[0]][0][0]=True
            userTarget[move[0]][1][0]=True
            userTarget[move[0]][1][1]=True
            userTarget[move[0]][0][1]=True
        elif move[1]=='A' and move[2]==10:
            userTarget[move[0]][0][9]=True
            userTarget[move[0]][0][8]=True
            userTarget[move[0]][1][9]=True
            userTarget[move[0]][1][8]=True
        elif move[1]=='J' and move[2]==1:
            userTarget[move[0]][9][1]=True
            userTarget[move[0]][8][1]=True
            userTarget[move[0]][9][0]=True
            userTarget[move[0]][8][0]=True
        elif move[1]=='J' and move[2]==10:
            userTarget[move[0]][9][9]=True
            userTarget[move[0]][8][8]=True
            userTarget[move[0]][9][8]=True
            userTarget[move[0]][8][9]=True

    elif move[1] in ['A', 'J']: 
        if move[1]=='A':
            userTarget[move[0]][0][move[2]-1]=True
            userTarget[move[0]][0][move[2]-2]=True
            userTarget[move[0]][0][move[2]]=True
            userTarget[move[0]][1][move[2]-1]=True
            userTarget[move[0]][1][move[2]-2]=True
            userTarget[move[0]][1][move[2]]=True
        elif move[1]=='J':
            userTarget[move[0]][9][move[2]-1]=True
            userTarget[move[0]][9][move[2]-2]=True
            userTarget[move[0]][9][move[2]]=True
            userTarget[move[0]][8][move[2]-1]=True
            userTarget[move[0]][8][move[2]-2]=True
            userTarget[move[0]][8][move[2]]=True

    elif move[2] in [1,10]:
        if move[2]==1:
            userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]]=True
        if move[2]==10:
            userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]-1]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-2]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]-2]=True
            userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]-2]=True

    else: #general case
        userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-1]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-2]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]-1]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]-2]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))-1][move[2]]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]-1]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]-2]=True
        userTarget[move[0]][int(chr(ord(move[1])-17))+1][move[2]]=True

    for i in range(10): #updating placement board
        for j in range(10):
            if compPlacement[move[0]][i][j]==True and userTarget[move[0]][i][j]==True:
                userTarget[move[0]][i][j]="hit"
                compPlacement[move[0]][i][j]="tagged"
            if compPlacement[move[0]][i][j]=="tagged" and userTarget[move[0]][i][j]==True:
                userTarget[move[0]][i][j]="hit"

    

        
def userTurn(userTarget,compPlacement):
    """Enables the user to play their turn
    Input: userTarget (list): user's targeting board
           compPlacement (list): computer's placement board
    Output: pygame screen for user to input
    Return: --
    """
    pygame.draw.rect(gameDisplay, white, (0,475,800,125))
    messageDisplay("Enter coordinates for attack in the form (depth,row,column): ",black,70,500,18)
    pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
    coord=''
    pygame.display.update()
    coordState=False
    turnOver=False
    
    while turnOver==False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if  525> mouse[0] > 275 and 575 > mouse[1] > 550: #input attack coordinates
                if click[0] == 1:
                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                    pygame.display.update()
                    coordState = False
                    while coordState== False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            if event.type == pygame.KEYDOWN:
                                keyPressed = pygame.key.get_pressed()
                                if keyPressed[pygame.K_KP_ENTER] or keyPressed[pygame.K_RETURN]:
                                    try: #check if valid position
                                        move=coord.split(',')
                                        move[0]=int(move[0])
                                        move[1]=chr(ord(move[1]))
                                        move[2]=int(move[2])
                                        if move[2]<1 or move[2]>10:
                                            raise Error("")
                                        if move[1]<'A' or move[1]>'J':
                                            raise Error("")
                                        if userTarget[move[0]][int(chr(ord(move[1])-17))][move[2]-1]==True:
                                            raise Error("")

                                    except:
                                        messageDisplay("Not possible. Enter again",black,575,550,15)
                                    else:
                                        coordState = True
                                        pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                        pygame.draw.rect(gameDisplay, white, (570, 530, 250, 50))
                                        pygame.draw.rect(gameDisplay, black, (275, 550, 250, 25), 2)
                                        pygame.display.update()
                                        attackUpdate(userTarget, compPlacement,move)
                                        displayTargetBoard(userTarget)
                                        turnOver=True
                                        break
                                elif keyPressed[pygame.K_BACKSPACE] or keyPressed[pygame.K_DELETE]:
                                    coord = coord[:-1]
                                    pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                    pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                elif event.unicode!="":
                                    coord+=event.unicode
                                pygame.draw.rect(gameDisplay, white, (275, 550, 250, 25))
                                pygame.draw.rect(gameDisplay, blue, (275, 550, 250, 25), 2)
                                messageDisplay(coord,black,290,555,13)
                                pygame.display.update()

        clock.tick(60)

    time.sleep(2)
    pygame.draw.rect(gameDisplay, white, (0,475,800,125))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check4=button("Continue", 325,540,150,30,buttonGrey,buttonLightGrey,'click')
        if check4==True:
            time.sleep(0.5)
            break
        pygame.display.update()
        clock.tick(60)

def checkWin(board):
    """Check if the user or the computer has won.
    Input: board (list): the board which has to be checked
    Output: none
    Return: True if won, False otherwise
    """
    win=True
    for i in range(10):
        for j in range(10): #if there is any unmarked ship
            if board[0][i][j]==True or board[1][i][j]==True:
                win=False
    return win

def compTurn(compTarget, userPlacement):
    """Randomly plays the computer's turn.
    Input: compTarget (list): computer's targeting board
           userPlacement (list): user's placement board
    Output: Shows the computer's targeting board
    Return: --
    """
    messageDisplay("Computer's turn",black,300 ,500,30)
    while True: #plays a random move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check4=button("Continue", 325,540,150,30,buttonGrey,buttonLightGrey,'click')
        if check4==True:
            time.sleep(0.5)
            break
        pygame.display.update()
        clock.tick(60)
    while True:
        compDepth=random.randint(0,1)
        compRow=random.randint(0,9)
        compCol=random.randint(0,9)
        if compTarget[compDepth][compRow][compCol]==False:
            break
    compCol+=1
    compRow=chr(17+ord(str(compRow)))
    move=[compDepth, compRow, compCol]
    attackUpdate(compTarget, userPlacement,move)
    displayTargetBoard(compTarget)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check4=button("Continue", 325,540,150,30,buttonGrey,buttonLightGrey,'click')
        if check4==True:
            time.sleep(0.5)
            break
        pygame.display.update()
        clock.tick(60)           
    
def winner(who):
    """Displays the game over screen
    Input: who (string): winner of the game
    Output: Displays whether the user won or lost
    Return:  --
    """
    gameDisplay.fill(black)
    if who=="user":
        messageDisplay("YOU WIN", white,170,150,75)
    else:
        messageDisplay("YOU LOSE", white, 170,150,75)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check=button("Play again", 200,540,75,30,buttonGrey,buttonLightGrey,'click')
        if check==True:
            gameIntro()
        check=button("Quit", 400,540,75,30,buttonGrey,buttonLightGrey,'click')
        if check==True:
            pygame.quit()
            quit()
        pygame.display.update()
        clock.tick(60)

def gamePlay():
    """Gameplay of battleship
    Input: none
    Output: intro screen of game and gameplay
    Return: --
    """
    displayGameboard()
    messageDisplay("Welcome to Battleship",black,225,500,30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check=button("Start", 375,540,50,30,buttonGrey,buttonLightGrey,'click')
        if check==True:
            break
        pygame.display.update()
        clock.tick(60)
    displayGameboard()
    W=False #No ship
    Ship=True #Ship

    userPlacement=[[[W for x in range(10)] for y in range(10)] for z in range(2)] #Accessed by userPlacement[depth][row][col]
    userTarget=[[[W for x in range(10)] for y in range(10)] for z in range(2)] #Accessed by userTarget[depth][row][col]
    compPlacement=[[[W for x in range(10)] for y in range(10)] for z in range(2)] #Accessed by compPlacement[depth][row][col]
    compTarget=[[[W for x in range(10)] for y in range(10)] for z in range(2)] #Accessed by compTarget[depth][row][col]

    deployComp(compPlacement) #randomly deploys ships for computer
    messageDisplay("Computer placement",black,225,500,30)
    displayPlacementBoard(compPlacement)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check2=button("Continue",375,540,50,30,buttonGrey,buttonLightGrey,'click')
        if check2==True:
            time.sleep(0.5)        
            break
        pygame.display.update()
        clock.tick(60)

    displayGameboard()
    messageDisplay("Place your ships",black,275 ,500,30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check3=button("Continue",375,540,50,30,buttonGrey,buttonLightGrey,'click')
        if check3==True:
            time.sleep(0.5)
            break
        pygame.display.update()
        clock.tick(60)
    displayGameboard()
    deployUser(userPlacement) #user input for user's ships
    pygame.draw.rect(gameDisplay, white, (0,475,800,125))
    messageDisplay("Ships placed",black,300 ,500,30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        check4=button("Play game", 325,540,150,30,buttonGrey,buttonLightGrey,'click')
        if check4==True:
            time.sleep(0.5)
            break
        pygame.display.update()
        clock.tick(60)

    displayGameboard()
    gameOver=False
    while gameOver==False:
        displayTargetBoard(userTarget)
        userTurn(userTarget, compPlacement)
        pygame.display.update()
        winOrNot=checkWin(compPlacement)
        if winOrNot==True:
            winner("user")
            gameOver=True
        displayGameboard()
        pygame.display.update()
        compTurn(compTarget, userPlacement)
        winOrNot=checkWin(userPlacement)
        if winOrNot==True:
            winner("comp")
            gameOver=True
        displayGameboard()
        pygame.display.update()
        
gameIntro()
pygame.quit()
quit()
