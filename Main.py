# sqlite3 is a library that allows us to interact with a database
import sqlite3
# pygame is a library that allows us to interact with the pygame window
import pygame
# random is a library that allows us to generate random numbers
import random

# Following information is for SQLite3
# This is the connection to the database
connection = sqlite3.connect('test.sqlite3')
# This is the cursor that allows us to interact with the database
cursor = connection.cursor()
# This is the creation of the table if it doesn't already exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")
# Retrive all values from the table
select = cursor.execute("SELECT * FROM users")
allUsers = select.fetchall()

# Following information is for Pygame
# This is the initialization of pygame
pygame.init()
# This is the font that we will be using
pygame.font.init()
font = pygame.font.SysFont('Arial', 32)
# This is the window that we will be using
pygame.display.set_caption('PC | CSC235 | 8.1')
screen = pygame.display.set_mode((640, 480))

# Stats Variables:
name = ""
score = 0.0

# Current stage of game
inputingName = True
finishedGame = False
scoreAdded = False
returnID = False

# Possbile input types:
pg_delete = [pygame.K_BACKSPACE, pygame.K_DELETE] 
pg_enter = [pygame.K_RETURN, pygame.KSCAN_KP_ENTER, pygame.K_KP_ENTER, 13]

# function that displays the base screen
def baseScreen():
    # Fill the screen white
    screen.fill((255, 255, 255))

    # Create a text object using the font
    text = font.render("Please enter your name or ID", False, (0, 0, 0))
    # Add the text to the screen at the location (0,0)
    screen.blit(text, (0,0))
# Reset all variables
def reset():
    # Allow global varriables to be in scope
    global inputingName, finishedGame, scoreAdded, returnID, name, score, allUsers
    inputingName = True
    finishedGame = False
    scoreAdded = False
    returnID = False
    name = ""
    score = 0.0
# Run the base screen function
baseScreen()
while True:
    # For each event from pygame
    for event in pygame.event.get():
        # If the user is inputing a name
        if inputingName:
            # if the user presses a key
            if event.type == pygame.KEYDOWN:
                # Display the base screen
                baseScreen()
                # If the user presses a key that is an accepted delete key
                if event.key in pg_delete:
                    # Remove last character
                    name = name[:-1]
                # If the user presses a key that is an accepted enter key
                if event.key in pg_enter:
                    print('Finished')
                    # Check if user is in the Database
                    try:
                        for user in allUsers:
                            if user[0] == int(name):
                                returnID = user[0]
                                name = user[1]
                                break
                    except:
                        print("Invalid ID")
                    # Finish inputing name
                    inputingName = False
                else:
                    # Check if the user pressed a valid character that is a letter or a number
                    if event.unicode.isalpha() or event.unicode.isdigit():
                        # Add to name string
                        name += event.unicode
                # Display the name on the screen
                nameObject = font.render(name, True, (0, 0, 0))
                screen.blit(nameObject, (0, 64))
        # If the user is not inputing a name, and the game is not finished
        elif not finishedGame:
            if event.type == pygame.KEYDOWN:
                # If a valid enter key is pushed, finish the game
                if event.key in pg_enter:
                    print("Game Finished")
                    finishedGame = True
        elif finishedGame:
            # If score has not beed added
            if not scoreAdded:
                # Display congrats screen
                screen.fill((255, 255, 255))
                congrats = font.render("Congratulations " + name + "!", True, (0, 0, 0))
                screen.blit(congrats, (0, 0))
                score = round(score, 2)
                result = font.render("Your score was " + str(score), True, (0, 0, 0))
                screen.blit(result, (0, 64))
                highScoreMSG = ""
                # If this is a returning user
                if returnID:
                    # Display high score message
                    if score > int(user[2]):
                        highScoreMSG = "This is your new high score!"
                        cursor.execute("UPDATE users SET score = ? WHERE id = ?", (score, int(user[0])))
                    else:
                        highScoreMSG = "This is not your new high score."
                # If this is a new user, display the id of the user
                else:
                    highScoreMSG = "This is your first time playing! Your id is: " + str(len(allUsers) +1)
                    cursor.execute("INSERT INTO users (name, score) VALUES (?, ?)", (name, score))
                highScoreObj = font.render(highScoreMSG, True, (0, 0, 0))
                screen.blit(highScoreObj, (0, 128))
                allUsers.append((len(allUsers) + 1, name, score))
                connection.commit()
                scoreAdded = True
            # If the user wants to play again
            elif event.type == pygame.KEYDOWN:
                if event.key in pg_enter:
                    # Reset the values
                    # Display the base screen
                    reset()
                    baseScreen()
        # If the user wants to quit the game
        # This is a built in pygame event, rather than a keyboard
        # it is for when exiting the application
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # if the user is not inputing a name, and the game is not finished
    if not inputingName and not finishedGame:
        # fill the screen with a light blue color
        screen.fill((200, 200, 255))
        # Add a random ammount to the score
        # Display the score
        score += random.random() / 100
        scoreObject = font.render(str(round(score,2)), True, (0, 0, 0))
        screen.blit(scoreObject, (0, 0)) 
    # Update the display
    pygame.display.update()

    