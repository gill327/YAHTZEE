# Ethan Gillis
# COMP 150
# Yahtzee Game
# 12/6/2021

import csv
import random
from cImage import *
# This function creates a gif file by altering the colors of the starting dice image
# This will allow the function to show which dice have been clicked during a reroll
def createClicked():
    image = FileImage('dice.gif')
    width = image.getWidth()
    height = image.getHeight()
    newIm = EmptyImage(width, height)
    for row in range(height):
        for col in range(width):
            pixel1 = image.getPixel(col, row)
            red = pixel1.getRed()
            green = pixel1.getGreen()
            blue = pixel1.getBlue()
            newPixel = pixel1
            if (red == green == blue):
                if (red == 255):
                    newPixel = Pixel(51, 213, 102)
                elif (red == 0):
                    newPixel = Pixel(51, 213, 102)
            newIm.setPixel(col, row, newPixel)
    newIm.save('clicked.gif')

# The validate player function checks to make sure the player has entered a name
def validatePlayer(array, i):
    x = input("Player "+str(i+1)+"'s Name Here: ")
    if (x != ''):
        array.append(x)
        return array
    else:
        print('Please enter a player name.')
        return validatePlayer(array, i)
# This function is to be called after the initial input of the number of players
# it returns and array with everyone's name, which can then be used to make the score card
def initializePlayers(number):
    array = []
    for i in range(number):
        array = validatePlayer(array, i)
    return array

# First we initialize the scorecard for the upper scores
def initializeUpper(players):
    # We start by initializing a nested array, with the categories as the first row
    upper = [['Name','Ones','Twos','Threes','Fours','Fives','Sixes','Sum','Bonus']]
    # for loop allows the funciton to create arrays and empty scores for each player
    for j in range(len(players)):
        # first you append the empty list to upper
        upper.append([])
        # Then add a negative 1 to each section, because we can have a score of zero
        for i in range(len(upper[0])):
            upper[j+1].append(0)
        # This last step assigns the player's name to the first entry in their list, which matches up with the 'Name' title
        upper[j+1][0] = players[j]
    # finally, return the upper array to the variable it is assigned to
    return upper

# The lower scorecard can be initialized in the same way, with new categories
def initializeLower(players):
    # We start by initializing a nested array, with the categories as the first row
    lower = [['Name','Three of a kind','Four of a kind','Full House','Small Straight','Large Straight','Chance','YAHTZEE']]
    # for loop allows the funciton to create arrays and empty scores for each player
    for j in range(len(players)):
        # first you append the empty list to upper
        lower.append([])
        # Then add a negative 1 to each section, because we can have a score of zero
        for i in range(len(lower[0])):
            lower[j+1].append(0)
        # This last step assigns the player's name to the first entry in their list, which matches up with the 'Name' title
        lower[j+1][0] = players[j]
    # finally, return the upper array to the variable it is assigned to
    return lower

# The initialize options funciton initializes some nested dictionaries
# The initial keys are the players' names, which are linked to dictionaries
# containing each category and booleans to tell if the option has been used yet
def initializeOptions(players):
    global upper
    global lower
    options = {}
    for player in players:
        options.update({player:{}})
        for i in range(1, len(upper[0])-2):
            options[player].update({upper[0][i]:False})
        for i in range(len(upper[0])-2, len(upper[0])):
            options[player].update({upper[0][i]:True})
        for i in range(1, len(lower[0])):
            options[player].update({lower[0][i]:False})
    return options

# The initializeResume function uses a saved .csv file to initialize the players, upper, and lower lists and the totalOptions dictionary
def initializeResume(savedFile):
    global players, upper, lower, totalOptions
    upper = [['Name','Ones','Twos','Threes','Fours','Fives','Sixes','Sum','Bonus']]
    lower = [['Name','Three of a kind','Four of a kind','Full House','Small Straight','Large Straight','Chance','YAHTZEE']]
    totalOptions = {}
    rowCount = 0
    with open(savedFile, 'r') as file:
        csvReader = csv.reader(file)
        name = ''
        index = 1
        players = []
        for row in csvReader:
            if (len(row) > 0 and row[0] != 'Name'):
                if (row[0] not in players):
                    players.append(row[0])
                if (rowCount != 0):
                    if (row[0] == name):
                        totalOptions.update({row[0]:{}})
                        for i in range(1, len(row)):
                            if (i < len(upper[0])):
                                totalOptions[row[0]].update({upper[0][i]:bool(int(row[i]))})
                            else:
                                newI = i-len(row)
                                totalOptions[row[0]].update({lower[0][newI]:bool(int(row[i]))})
                    else:
                        upper.append([])
                        lower.append([])
                        upper[index].append(row[0])
                        lower[index].append(row[0])
                        for i in range(1, len(row)):
                            if (i < len(upper[0])):
                                upper[index].append(int(row[i]))
                            else:
                                lower[index].append(int(row[i]))
                        name = row[0]
                        index += 1
            rowCount+=1

# The validateInt function checks to make sure a user is inputting an integer greater than 0
# otherwise it asks the user to try again and starts over.
def validateInt(message):
    statement = input(message)
    if (statement.isdigit()):
        if (int(statement) > 0):
            return int(statement)
        else:
            print("That's not a valid number, please answer again.\n")
            return validateInt(message)
    else:
        print("That's not a valid number, please answer again.\n")
        return validateInt(message)

# The bonus() function will be used to determine if any player gets a bonus on their upper score at the end of the game
def bonus():
    global upper
    # the first for loop loops through each player
    for i in range(1, len(upper)):
        # sum will be used to add all the numbers together
        sum = 0
        # the second for loop goes through the scores from ones to sixes, and adds their values to sum
        for j in range(1, 7):
            sum = sum + upper[i][j]
        # then this value is saved in the 'Sum' section of the list
        upper[i][7] = sum
        # if it is greater than or equal to 63, the bonus score field is filled with 35
        if sum >= 63:
            upper[i][8] = 35

# This next funciton defines a single dice roll using the random randint funciton from 1 to 6
def roll():
    return random.randint(1, 6)
# the drawDie function draws a single die
def drawDie(die, diceWidth, diceHeight, sourceImage):
    newDice = EmptyImage(diceWidth, diceHeight)
    beginning = (die-1)*diceWidth
    end = die * diceWidth
    widthNumber = []
    for i in range(6):
        for col in range(diceWidth):
            widthNumber.append(col)
    for row in range(diceHeight):
        for col in range(beginning, end): 
            sourcePixel = sourceImage.getPixel(col, row)
            newPixel = sourcePixel
            newDice.setPixel(widthNumber[col], row, newPixel)
    return newDice
# rollImage makes an image of a single die from the dice rolled
def rollImage(dice, prompt, clicks=0):
    sourceImage = FileImage('dice.gif')
    diceWidth = (sourceImage.getWidth())//6
    diceHeight = sourceImage.getHeight()
    finalWindow = ImageWin(prompt, diceWidth * 5, diceHeight)
    transform = 0
    for die in dice:
        newDice = drawDie(die, diceWidth, diceHeight, sourceImage)
        newDice.setPosition(diceWidth * transform, 0)
        newDice.draw(finalWindow)
        transform += 1
    if (not clicks):
        finalWindow.exitOnClick()
    else:
        # The else statement here uses clicks to allow the user to click on the dice they want to roll again
        rerollDice = []
        for i in range(clicks):
            pos = finalWindow.getMouse()
            x = pos[0]
            for j in range(1,7):
                # This loops through the position of each die
                if (diceWidth*(j-1) < x < diceWidth*j):
                    # The clicked.gif file allows the dice to show that it is selected in the window
                    checkedSource = FileImage('clicked.gif')
                    rerollDice.append(j-1)
                    checked = drawDie(j, diceWidth, diceHeight, checkedSource)
                    checked.setPosition(diceWidth*(j-1), 0)
                    checked.draw(finalWindow)
        finalWindow.exitOnClick()
        return rerollDice
# The function initialRoll will make an array with five random numbers, each representing one of the dice
def initialRoll(player):
    # We start by initializing a dice array
    dice = []
    # Then we can use a for loop that goes 5 times with the roll() function to roll 5 dice and add the numbers to the array
    for i in range(5):
        dice.append(roll())
    # These next statements print the results, labeling the dice 1 through 5
    print('First roll results:')
    for i in range(5):
        print('Dice '+str(i+1)+': '+str(dice[i]))
    transform = 0
    rollImage(dice, 'Initial Roll (Click on any dice to continue)')
    # The array is returned, to be used when rerolling or adding scores
    return dice

# The reRoll function lets the user reroll any dice they want to
def reRoll(diceRoll, dice):
    print('\nReroll Results: ')
    for index in diceRoll:
        dice[index] = roll()
        print('Dice '+str(index+1)+': '+str(dice[index]))
    print('\nCurrent dice values: ')
    for i in range(5):
        print('Dice '+str(i+1)+': '+str(dice[i]))
    rollImage(dice, 'Current Dice (Click on any dice to continue)')
    return dice

# The continue function determines if there are still 'empty scores' using the options dictionary, and returns true or false
def continueGame(players):
    global totalOptions
    newRound = False
    for player in players:
        for category in totalOptions[player]:
            if (totalOptions[player][category] == False):
                newRound = True
    return newRound

# The remaining scores function is called in the options funciton, to determine what the player has already called
def remainingScores(player):
    global totalOptions
    scoresRemaining = []
    for category in totalOptions[player].keys():
        if (totalOptions[player][category] == False):
            if (category != 'YAHTZEE'):
                scoresRemaining.append(category)
    return scoresRemaining

# The validateOption function makes sure not only that the option is an integer,
# but also that it is one of the remaining options
def validateOption(remains):
    option = validateInt('Choose a category: ')
    if option in range(1, len(remains)+1):
        option = remains[option-1]
    elif (option == 50):
        option = 'YAHTZEE'
    else:
        print('That is not a current option, please answer again.\n')
        return validateOption(remains)
    return option

# The options function uses the remaining scores function to display the remaining categories to the player, then has the player choose
def options(players, player):
    global upper
    global lower
    # callign this function returns all available categories
    remains = remainingScores(player)
    print('\nRemaining options for scoring: \n')
    # These two loops sort the categories by upper and lower combinations
    print('Upper Combinations: ')
    for option in remains:
        if option in upper[0]:
            print(option+' ('+str(remains.index(option)+1)+');', end=' ')
    print('\nLower Combinations: ')
    for option in remains:
        if option in lower[0]:
            print(option+' ('+str(remains.index(option)+1)+');', end=' ')
    # Since you can have multiple yahtzees, it is always displayed as an option
    print('YAHTZEE! (50);\n')
    print("Type the number in parentheses next to the option you want (YAHTZEE is always 50!)\n")
    option = validateOption(remains)
    return option

#upperScore is used to add up the score when a player uses an upper score combination
def upperScore(dice, number):
    total = 0
    for die in dice:
        if (die == number):
            total = total + die
    return total

# checkThree checks to see if there are three of the same dice
def checkThree(dice):
    # We can sort the array first, to make the equal dice next to each other
    dice.sort()
    # Then we check on both sides of the middle three dice, to see if the roll is three of a kind
    for i in range(1, len(dice)-1):
        if (dice[i] == dice[i-1] == dice[i+1]):
            return True
    return False

# checkFour is very similar to checkThree
# When you have four of a kind, and the array is sorted, it must either touch the first or last spot in the set of five dice
def checkFour(dice):
    dice.sort()
    if (dice[-1] == dice[-2] == dice[-3] == dice[-4]):
        return True
    elif(dice[0] == dice[1] == dice[2] == dice[3]):
        return True
    else:
        return False

# checkFullHouse checks if the user has a full house by sorting the array and checking both sides of the array
def checkFullHouse(dice):
    dice.sort()
    if (dice[0] == dice[1] and dice[2] == dice[3] == dice[4]):
        return True
    elif (dice[0] == dice[1] == dice[2] and dice[3] == dice[4]):
        return True
    else:
        return False

# The checkSmall function sorts the array and checks for a small straight
def checkSmall(dice):
    dice.sort()
    if (dice[4]-1 == dice[3] and dice[3]-1 == dice[2] and dice[2]-1 == dice[1]):
        return True
    elif(dice[3]-1 == dice[2] and dice[2]-1 == dice[1] and dice[1]-1 == dice[0]):
        return True
    else:
        return True

# Large a similar if statement to check for a large straight
def checkLarge(dice):
    dice.sort()
    if (dice[4]-1 == dice[3] and dice[3]-1 == dice[2] and dice[2]-1 == dice[1] and dice[1]-1 == dice[0]):
        return True
    else:
        return False

#checkYAHTZEE determines if the dice rolled were actually a yahtzee
def checkYAHTZEE(dice):
    dice.sort()
    total = 0
    for i in range(len(dice)):
        if (dice[0] == dice[i]):
            total = total +1
    if total == 5:
        return True
    else:
        return False

#lowerScore determines what score to return based on the category given
# Each category has a function to check if the category called is applicable, and returns 0 if they can't be scored
def lowerScore(dice, index):
    if index == 1:
        if (checkThree(dice)):
            total = 0
            for die in dice:
                total = total + die
            return total
        else:
            return 0
    if index == 2:
        if (checkFour(dice)):
            total = 0
            for die in dice:
                total = total + die
            return total
        else:
            return 0
    if index == 3:
        if (checkFullHouse(dice)):
            return 25
        else:
            return 0
    if index == 4:
        if (checkSmall(dice)):
            return 30
        else:
            return 0
    if index == 5:
        if (checkLarge(dice)):
            return 40
        else:
            return 0
    if index == 6:
        total = 0
        for die in dice:
            total = total + die
        return total
    if index == 7:
        if (checkYAHTZEE(dice)):
            return 50
        else:
            return 0

# The updateOptions function updates the categories available to the individual player
def updateOptions(category, player):
    global totalOptions
    totalOptions[player][category] = True

# the score function will use the dice to calculate the score for a player
def score(players, player, category, dice):
    global upper
    global lower
    wp = players.index(player)+1
    if category in upper[0]:
        wc = upper[0].index(category)
        # if the category is upper, then call the upper score function
        upper[wp][wc] = upperScore(dice, wc)
        print('Score added: '+str(upper[wp][wc]))
        # Finally, we update the options dictionary for this player using updateOptions()
        updateOptions(category, player)
    elif category in lower[0]:
        wc = lower[0].index(category)
        lower[wp][wc] = lowerScore(dice, wc)
        print('Score added: '+str(lower[wp][wc]))
        updateOptions(category, player)

# validateOneFive is a special validation function for rerolls, it checks for a valid integer that is between 1 and 5
def validateOneFive(message):
    number = validateInt(message)
    if number in range(1, 6):
        return number
    else:
        print('Make sure your number is in between 1 and 5!\n')
        return validateOneFive(message)
# The restart function asks the player if they want to quit or return to the title screen
# After a save or win
def restart():
    keepGoing = input('Type Q and press ENTER to quit,\nor press ENTER to return to the title screen: ')
    if (keepGoing.lower() == 'q'):
        print('\nThanks for playing!\n')
        print('Type YAHTZEE() and press ENTER or\nreload the program to get back to the Title Screen')
        for i in range(82):
            print('-', end = '')
        print('')
        return
    else:
        YAHTZEE()
# The checkScore function will return a dictionary with the players and their current scores
# it is used in combination with finalScore() at the end of the game, and can be called in between
# rounds if the players want to check the score
def checkScore():
    global upper
    global lower
    global players
    # The bonus function adds up the upper scores of the players to add 35 if they breached 63
    bonus()
    playerScore = {}
    for player in players:
        playerScore.update({player:int()})
    # Then we loop through the upper array, to count up the score for each player
    for i in range(1, len(upper)):
        total = 0
        player = upper[i][0]
        for j in range(7, 9):
            total = total + upper[i][j]
        playerScore[player] += total
    # we loop through the lower function to add up all the scores
    for i in range(1, len(lower)):
        total = 0
        player = lower[i][0]
        for j in range(1, len(lower[0])):
            total = total + lower[i][j]
        playerScore[player] += total
    return playerScore
# the finalScore function will count up the total for each player and tell who the winner is
def finalScore():
    global upper
    global lower
    global players
    # playerScore is a dictionary where players are the key for their scores
    playerScore = checkScore()
    # Then we print each player and their score
    print('\nFinal Scores:')
    for player, score in playerScore.items():
        print(player+': '+str(score))
    # Finally, we loop through the dictionary one more time, to determine who the winner is
    scores = list(playerScore.values())
    winningScore = max(scores)
    for player, score in playerScore.items():
        if score == winningScore:
            print('\n'+player+' is the winner!\n')
    print('Congratulations!\nType YAHTZEE() and press ENTER to play again!\n')
    for i in range(82):
        print('-', end = '')
    print('')
    restart()

# The saveGame function writes the players' scores and options into a save file
def saveGame():
    global players, upper, lower, totalOptions
    for i in range(82):
        print('-', end = '')
    print('')
    fileName = input('What would you like to name your game file? ')
    with open((fileName+'.csv'), 'w', newline = '') as newFile:
        fileSave = csv.writer(newFile)
        fileSave.writerow(upper[0]+lower[0][1:])
        for i in range(1, len(players)+1):
            fileSave.writerow(upper[i]+lower[i][1:])
            secondRow = [upper[i][0]]
            for value in list(totalOptions[upper[i][0]].values()):
                if (value == True):
                    secondRow.append(1)
                else:
                    secondRow.append(0)
            fileSave.writerow(secondRow)
    print('\n'+fileName+' has been saved!\n')
    print("Remember your game's name! You can use it to resume your game later!")
    for i in range(82):
        print('-', end = '')
    print('')
    restart()

# This function will play through rounds of rolling dice and scoring until the end of the game is reached
def yahtzeeRound(players):
    roundNumber = 0
    # This while loop calls the continueGame function to check for completed scorecards
    while (continueGame(players)):
        roundNumber += 1
        for i in range(82):
            print('_', end = '')
        print('\nRound '+str(roundNumber))
        save = input('Save or continue? (Type SAVE to save)')
        if 'save' in save.lower():
            return saveGame()
        # This input in between rounds allows users to check on the current scores of the game
        scoreCheck = input('Check current scores? (YES or NO) ')
        if ('yes' in scoreCheck.lower()):
            # It loops through the dictionary in a similar way to the finalScore() function
            scores = checkScore()
            print('\nCurrent Scores:')
            for player, current in scores.items():
                print(player+': '+str(current))
        for player in players:
            # Each round introduces the player, the initial roll, and asks which dice to reroll
            # They also have the option to save their game before each turn by typing 'save'
            input('\n'+player+"'s turn \n(press ENTER to continue) ")
            dice = initialRoll(player)
            reRollCount = 0
            while (reRollCount < 2):
                again = input('\nWould you like to reroll any dice? (YES or NO) ')
                if ('no' in again.lower()):
                    reRollCount = 2
                else:
                    diceAmnt = validateOneFive('How many dice would you like to reroll? (1-5) ')
                    # In this case for rollImage, I included diceAmnt as an optional variable, so that 
                    # you can click on which dice you want to reroll
                    diceRoll = rollImage(dice, 'Click on the dice you want to reroll:', diceAmnt)
                    dice = reRoll(diceRoll, dice)
                    reRollCount = reRollCount + 1
            # the options function will deterine available categories and return what the player chooses
            category = options(players, player)
            print(category)
            score(players, player, category, dice)
    for i in range(82):
        print('-', end = '')
    print('')
    finalScore()

# newGame is a function to help start over the game if you finish
# it reassigns all the originial variables using the global keyword and starting functions
def newGame():
    global players, upper, lower, totalOptions
    for i in range(82):
        print('-', end = '')
    print('')
    print('Welcome to Yahtzee!\n')
    new = input('Press ENTER to start a new game \nOR type LOAD to load a save file: ')
    if ('load' in new.lower()):
        return resumeGame()
    for i in range(82):
        print('-', end = '')
    print('')
    number = validateInt('How many players do you have? ')
    players = initializePlayers(number)
    upper = initializeUpper(players)
    lower = initializeLower(players)
    totalOptions = initializeOptions(players)
    yahtzeeRound(players)

# The resumeGame funciton is called if the user starts a game with a file parameter
def resumeGame():
    global players, upper, lower, totalOptions
    file = input('Type the name of your save file: ')
    fileName = file+'.csv'
    for i in range(82):
        print('-', end = '')
    print('\n'+file+' loaded!')
    initializeResume(fileName)
    yahtzeeRound(players)

# The YAHTZEE() function starts a game of Yahtzee
# It can be called with a file parameter to resume a previous game
def YAHTZEE():
    newGame()
createClicked()
YAHTZEE()
# Load the file into the IDLE shell to begin the game
# You can also run the program by itself, or use a different IDE
# Use full screen for the best results
# YAHTZEE() can be called to start a new game if you end in an IDE
# Otherwise, you can just run the program again to start or resume