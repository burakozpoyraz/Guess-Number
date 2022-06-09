# PACKAGES----------------------------------------------------------------
from datetime import datetime as dt
from termcolor import colored
from time import time
import pandas as pd
import numpy as np
import os.path
import random
import emoji
# ------------------------------------------------------------------------


# FUNCTIONS---------------------------------------------------------------
# ========================================================================
# 1) User Input
#
# ARGUMENT
# - text: Text message that is displayed to the user while waiting an input (Data Type: str)
#
# OUTPUT
# - input_val: Input value taken from the user (Data Type: str)
# ========================================================================
def UserInput(text):
    print(emoji.emojize(":arrow_right: ", language="alias"), end="")
    print(colored(text, "yellow", attrs=["bold", "underline"]), end="")
    input_val = input("")
    return input_val
# ========================================================================


# ========================================================================
# 2) Waiting Timer
#
# ARGUMENT
# - seconds: Time duration that the program will wait
# ========================================================================
def Wait(seconds):
    start_time = time()

    while True:
        current_time = time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            break
# ========================================================================


# ========================================================================
# 3) Game Loading Section
# ========================================================================
def Loading():
    Wait(1)
    print("Let's guess some numbers :)")
    Wait(1)
    print("Game is starting", end="")
    Wait(1)
    print(colored(".", "red"), end="")
    Wait(1)
    print(colored(".", "blue"), end="")
    Wait(1)
    print(colored(".", "green"))
    Wait(1)
    print()
# ========================================================================


# ========================================================================
# 4) Separator Line
# ========================================================================
def Separator():
    print(colored("\n ---------------------------------\
-------------------------------------------------------\
--------------------------- \n",
                  "magenta", attrs=["bold", "reverse"]))
# ========================================================================

# ========================================================================
# 5) Lower Value of Number Range
#
# OUTPUT
# - x_low: Lower value of number range taken by the user (Data Type: int)
# ========================================================================
def LowerValue():
    x_low_str = UserInput("Please enter the lower value of the number range: ")
    try:
        x_low = int(x_low_str)
        return x_low
    except ValueError:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" You entered a non-integer value! \n", "red", attrs=["bold", "reverse"]))
        return LowerValue()
    except:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" Something went wrong! \n", "red", attrs=["bold", "reverse"]))
        return LowerValue()
# ========================================================================


# ========================================================================
# 6) Upper Value of Number Range
#
# ARGUMENT
# - x_low: Lower value of number range taken by the user (Data Type: int)
#
# OUTPUT
# - x_up: Upper value of number range taken by the user (Data Type: int)
# ========================================================================
def UpperValue(x_low):
    x_up_str = UserInput("Please enter the upper value of the number range: ")
    try:
        x_up = int(x_up_str)
        if x_up <= x_low:
            print(emoji.emojize(":x: ", language="alias"), end="")
            print(colored(" Upper value should be greater than the lower value! \n", "red", attrs=["bold", "reverse"]))
            return UpperValue(x_low)
        else:
            return x_up
    except ValueError:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" You entered a non-integer value! \n", "red", attrs=["bold", "reverse"]))
        return UpperValue(x_low)
    except:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" Something went wrong! \n", "red", attrs=["bold", "reverse"]))
        return UpperValue(x_low)
# ========================================================================


# ========================================================================
# 7) Guess Limit
#
# OUTPUT
# - L: Guess limit to find the correct number taken from the user (Data Type: int)
# ========================================================================
def GuessLimit():
    L_str = UserInput("Please enter the guess limit as a number greater than 0, or enter 'inf' for no limit: ")
    if L_str == "inf":
        return 1e5
    
    try:
        L = int(L_str)
        if L < 1:
            print(emoji.emojize(":x: ", language="alias"), end="")
            print(colored(" Guess limit should be greater than 0! \n", "red", attrs=["bold", "reverse"]))
            return GuessLimit()
        else:
            return L
    except ValueError:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" You entered a non-integer value! \n", "red", attrs=["bold", "reverse"]))
        return GuessLimit()
    except:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" Something went wrong! \n", "red", attrs=["bold", "reverse"]))
        return GuessLimit()
# ========================================================================


# ========================================================================
# 8) Guessing a Number
#
# ARGUMENTS
# 1-) x_low: Lower value of number range (Data Type: int)
# 2-) x_up: Upper value of number range (Data Type: int)
#
# OUTPUT
# - guess_num: Number that the user guesses (Data Type: int)
# ========================================================================
def GuessNumber(x_low, x_up):
    guess_num_str = UserInput("Please guess a number between " + str(x_low) + " and " + str(x_up) + ": ")
    try:
        if guess_num_str == "exit":
            return guess_num_str
        
        guess_num = int(guess_num_str)
        if guess_num < x_low or guess_num > x_up:
            print(emoji.emojize(":x: ", language="alias"), end="")
            print(colored(" You entered a value out of the range! \n", "red", attrs=["bold", "reverse"]))
            return GuessNumber(x_low, x_up)
        else:
            return guess_num
    except ValueError:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" You entered a non-integer value! \n", "red", attrs=["bold", "reverse"]))
        return GuessNumber(x_low, x_up)
    except:
        print(emoji.emojize(":x: ", language="alias"), end="")
        print(colored(" Something went wrong! \n", "red", attrs=["bold", "reverse"]))
        return GuessNumber(x_low, x_up)
# ========================================================================


# ========================================================================
# 9) Read Game Log Data from Excel
#
# DESCRIPTION: Game log data format ->
#              Date (Ex: 13 May 2022),
#              Starting Time (Ex: 15:38),
#              Difficulty (Ex: Child's Play),
#              Number Range (Ex: [0 10]),
#              Guess Limit (Ex: 5),
#              Result (Ex: Win or Loss)
#
# OUTPUT
# - game_log: Game log data (Data Type: numpy.ndarray | Shape: (num_data, 3))
# ========================================================================
def ReadGameLog():
    game_log = pd.read_excel("GuessNumberGameLog.xlsx", index_col=0).to_numpy()
    return game_log
# ========================================================================


# ========================================================================
# 10) Update Game Log Excel File
#
# ARGUMENT
# 1-) difficulty: Difficulty Level (Data Type: str)
# 2-) num_range: Range of number to be guessed (Data Type: str)
# 3-) guess_limit: Guess limit to find the correct number taken from the user (Data Type: str)
# 4-) result: Result of the game (Data Type: str)
# ========================================================================
def UpdateGameLog(difficulty, num_range, guess_limit, result):
    month_array = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    now = dt.now()
    curr_month = month_array[now.month - 1]
    date_str = str(now.day) + " " + curr_month + " " + str(now.year)
    time_str = str(now.hour) + ":" + str(now.minute)

    if os.path.isfile("GuessNumberGameLog.xlsx"):
        game_log_history = ReadGameLog()
        game_log_lst = [date_str, time_str, difficulty, num_range, guess_limit, result]
        game_log_updated = np.vstack((game_log_history, game_log_lst))
    else:
        game_log_updated = np.array([[date_str, time_str, difficulty, num_range, guess_limit, result]])
    
    game_log_df = pd.DataFrame(game_log_updated, columns=["Date","Time","Difficulty","Number Range","Guess Limit","Result"])
    game_log_df.to_excel("GuessNumberGameLog.xlsx")
# ========================================================================


# ========================================================================
# 11) CSS Style of Game Log Table's Difficulty Column
#
# ARGUMENT
# - df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# ========================================================================
def DifficultyBackgroundColor(df): 
    if df == "Custom":
        return "text-align: center; background-color: #B27DCE; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    elif df == "Child's Play (1/5)":
        return "text-align: center; background-color: #68B961; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    elif df == "Easy (2/5)":
        return "text-align: center; background-color: #71B4B1; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    elif df == "Medium (3/5)":
        return "text-align: center; background-color: #D3D1B3; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    elif df == "Hard (4/5)":
        return "text-align: center; background-color: #DD985F; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    else:
        return "text-align: center; background-color: #99534E; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
# ========================================================================


# ========================================================================
# 12) CSS Style of Game Log Table's Result Column
#
# ARGUMENT
# - df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# ========================================================================
def ResultBackgroundColor(df):
    if df == "Win":
        return "text-align: center; background-color: green; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
    elif df == "Loss":
        return "text-align: center; background-color: red; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
# ========================================================================


# ========================================================================
# 13) CSS Style of Game Log Table's Rows with Even Index
#
# ARGUMENT
# - df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# ========================================================================
def EvenBackgroundColor(df):
    return "text-align: center; background-color: #DAEAF1; color: #323232; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
# ========================================================================


# ========================================================================
# 14) CSS Style of Game Log Table's Rows with Odd Index
#
# ARGUMENT
# - df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# ========================================================================
def OddBackgroundColor(df):
    return "text-align: center; background-color: #C6DCE4; color: #323232; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
# ========================================================================


# ========================================================================
# 15) CSS Style of Game Log Table's Rows with Even Index
#
# ARGUMENT
# - df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# ========================================================================
def TitleBackgroundColor(df):
    return "text-align: center; background-color: #323232; color: white; font-family: Avanta Garde; font-size: 15px; font-weight: bold"
# ========================================================================


# ========================================================================
# 16) Display Game Log
#
# ARGUMENT
# 1-) df: Pandas data frame that stores the game log history (Data Type: pandas.core.frame.DataFrame)
# 2-) num_game_log: Number of total games in the database (Data Type: int)
# ========================================================================
def DisplayDataFrame(df, num_game_log):
    return df.style.applymap(DifficultyBackgroundColor, subset="Difficulty")\
                   .applymap(ResultBackgroundColor, subset="Result")\
                   .applymap(EvenBackgroundColor,
                             subset=(slice(0, num_game_log, 2), ["Date","Time","Number Range","Guess Limit"]))\
                   .applymap(OddBackgroundColor,
                             subset=(slice(1, num_game_log, 2), ["Date","Time","Number Range","Guess Limit"]))\
                   .applymap_index(TitleBackgroundColor)\
                   .applymap_index(TitleBackgroundColor, axis="columns")
# ========================================================================
# ------------------------------------------------------------------------


# TITLE-------------------------------------------------------------------
print(emoji.emojize(":star: :1234: ", language="alias"), end="")
print(colored(" WELCOME TO GUESS NUMBER GAME ", "red", attrs=["bold", "reverse"]), end="")
print(emoji.emojize(" :1234: :star:\n", language="alias"))
# ------------------------------------------------------------------------

# DESCRIPTION-------------------------------------------------------------
print(emoji.emojize(":information_source: ", language="alias"), end="")
print(colored("GAME DESCRIPTION:", "yellow", attrs=["bold", "reverse"]), end="")
print(colored(" In this game, you will try to guess the correct number \
picked from a specific range. The range and the prediction limit varies \
according to the difficulty level you choose, where you can also set a custom \
range and limit. During the game, you will be informed about your guess if it is \
smaller or greater than the correct number. Have fun ", "yellow", attrs=["reverse"]), end="")
print(colored(emoji.emojize(":blush: \n", language="alias"), "yellow", attrs=["reverse"]))
# ------------------------------------------------------------------------

# GAME--------------------------------------------------------------------
while True:
    print(colored(" 1 - New Game:", "blue", attrs=["bold", "reverse"]) + " Starts a new game")
    print(colored(" 2 - Game Log:", "blue", attrs=["bold", "reverse"]) + " Lists all games played so far")
    print(colored(" 3 - Game Statistics:", "blue", attrs=["bold", "reverse"]) +
          " Shows the number of games, wins, losses, and win rate")
    print(colored(" 4 - Exit:", "blue", attrs=["bold", "reverse"]) + " Exits the game")

    option = UserInput("Please select an option from the list above to continue: ")
    while option != "1" and option != "2" and option != "3" and option != "4":
        print(emoji.emojize(":x: ", language="alias"), end="")
        option = UserInput(" You entered a non-existent option! Please select an option from the list above: ")
    print()
        
    if option == "1":
        Loading()

        print(colored(" 0 - Custom", "magenta", attrs=["bold", "reverse"]))
        print(colored(" 1 - Child's Play:", "green", attrs=["bold", "reverse"]) +
              " Range: [0 10] - Limit: Infinity Guess")
        print(colored(" 2 - Easy:", "cyan", attrs=["bold", "reverse"]) +
              " Range: [0 10] - Limit: 6 Guess")
        print(colored(" 3 - Medium:", "blue", attrs=["bold", "reverse"]) +
              " Range: [0 50] - Limit: 5 Guess")
        print(colored(" 4 - Hard:", "yellow", attrs=["bold", "reverse"]) +
             " Range: [0 100] - Limit: 4 Guess")
        print(colored(" 5 - Master Degree:", "red", attrs=["bold", "reverse"]) +
             " Range: [0 500] - Limit: 3 Guess")

        difficulty = UserInput("Please select a difficulty level from the list above: ")
        while difficulty != "0" and difficulty != "1" and difficulty != "2" and difficulty != "3" and difficulty != "4" and difficulty != "5":
            print(emoji.emojize(":x: ", language="alias"), end="")
            difficulty = UserInput("You entered a non-existent difficulty level! Please select a difficulty level from the list above: ")

        if difficulty == "0":
            print()
            difficulty = "Custom"
            x_low = LowerValue()
            x_up = UpperValue(x_low)
            num_range = "[" + str(x_low) + " " + str(x_up) + "]"
            L = GuessLimit()
            print("\nDifficulty level is " +
                 colored("Custom", "magenta", attrs=["bold", "reverse"]))
            if L == 1e5:
                guess_limit = "No Limit"
                print("Range: [" + str(x_low) + " " + str(x_up) + "] - Limit: Infinity Guess\n")                
            else:
                guess_limit = str(L)
                print("Range: [" + str(x_low) + " " + str(x_up) + "] - Limit: " + str(L) + " Guess\n")
        elif difficulty == "1":
            difficulty = "Child's Play (1/5)"
            num_range = "[0 10]"
            guess_limit = "No Limit"
            x_low = 0
            x_up = 10
            L = 1e5
            print("\nDifficulty level is " +
                  colored("Child's Play", "green", attrs=["bold", "reverse"]))
            print("Range: [0 10] - Limit: Infinity Guess\n")
        elif difficulty == "2":
            difficulty = "Easy (2/5)"
            num_range = "[0 10]"            
            x_low = 0
            x_up = 10
            L = 6
            guess_limit = str(L)            
            print("\nDifficulty level is " +
                 colored("Easy", "cyan", attrs=["bold", "reverse"]))
            print("Range: [0 10] - Limit: 6 Guess\n")
        elif difficulty == "3":
            difficulty = "Medium (3/5)"
            num_range = "[0 50]"            
            x_low = 0
            x_up = 50
            L = 5
            guess_limit = str(L)            
            print("\nDifficulty level is " +
                 colored("Medium", "blue", attrs=["bold", "reverse"]))
            print("Range: [0 50] - Limit: 5 Guess\n")        
        elif difficulty == "4":
            difficulty = "Hard (4/5)"     
            num_range = "[0 100]"
            x_low = 0
            x_up = 100
            L = 4
            guess_limit = str(L)            
            print("\nDifficulty level is " +
                 colored("Hard", "yellow", attrs=["bold", "reverse"]))
            print("Range: [0 100] - Limit: 4 Guess\n")
        else:
            difficulty = "Master Degree (5/5)"
            num_range = "[0 500]"            
            x_low = 0
            x_up = 500
            L = 3
            guess_limit = str(L)            
            print("\nDifficulty level is " +
                 colored("Master Degree", "red", attrs=["bold", "reverse"]))
            print("Range: [0 500] - Limit: 3 Guess\n")

        Wait(1)
        print("Random number is picked...")
        Wait(1)
        print("Let's play the game!")
        Wait(1)
        print(emoji.emojize(":information_source: ", language="alias"), end="")
        print(colored("EXIT INFO:", "yellow", attrs=["bold", "reverse"]), end="")
        print(colored("If you would like to exit the game at any time \
just enter 'exit'.\n", "yellow", attrs=["reverse"]))
        Wait(2)

        rand_num = random.randint(x_low, x_up)
        true_guess = False
        guess_count = 1
        while guess_count <= L and true_guess == False:
            if guess_count == 1:
                print(colored(" This is your first guess ", "yellow", attrs=["reverse"]))
            elif guess_count == L:
                print(colored(" This is your last guess, be careful...", "yellow", attrs=["reverse"]))
            else:
                print(colored(" This is guess " + str(guess_count), "yellow", attrs=["reverse"]))

            guess_num = GuessNumber(x_low, x_up)
            if guess_num == "exit":
                break
            elif guess_num == rand_num:
                true_guess = True
                print(colored(" Perfect! Your guess is correct " +
                              emoji.emojize(":white_check_mark: ", language="alias"), "green", attrs=["reverse"]) + "\n")
            elif guess_num < rand_num:
                x_low = guess_num + 1
                if guess_count < L:
                    print(colored(" Nope! You should go up " +
                              emoji.emojize(":arrow_up: ", language="alias"), "blue", attrs=["reverse"]) + "\n")
            else:
                x_up = guess_num - 1
                if guess_count < L:
                    print(colored(" Nope! You should go down " +
                              emoji.emojize(":arrow_down: ", language="alias"), "magenta", attrs=["reverse"]) + "\n")

            guess_count += 1
            
        if guess_num == "exit":
            print("\nSee you later... Good bye" + emoji.emojize(":wave: ", language="alias"))
            print(emoji.emojize(":crystal_ball: ", language="alias") +
                  "Mischief Managed " +
                  emoji.emojize(":crystal_ball: ", language="alias"))
            break
            
        if true_guess:
            result = "Win"
        else:
            result = "Loss"
            print(colored(" Correct Number: " + str(rand_num) + ", Game Over " +
                      emoji.emojize(":confused: ", language="alias"), "red", attrs=["reverse"]) + "\n")
            
        UpdateGameLog(difficulty, num_range, guess_limit, result)
        Wait(1)
        print("Game log is perfectly uploaded to excel file...")
        Wait(1)
            
        Separator()
    elif option == "2":
        if os.path.isfile("GuessNumberGameLog.xlsx"):
            game_log_np = ReadGameLog()
            num_game_log = game_log_np.shape[0]
            game_log_df = pd.DataFrame(game_log_np, columns = ["Date","Time","Difficulty","Number Range","Guess Limit","Result"])
            display(DisplayDataFrame(game_log_df, num_game_log))
        else:
            print(colored(" There is no game log " +
                      emoji.emojize(":pensive: ", language="alias"), "red", attrs=["reverse"])) 
        Separator()
    elif option == "3":
        if os.path.isfile("GuessNumberGameLog.xlsx"):
            game_log_np = ReadGameLog()
            num_win = len(np.where(game_log_np == "Win")[0])
            num_loss = len(np.where(game_log_np == "Loss")[0])
            num_game = num_win + num_loss
            win_rate = num_win / num_game
            print(colored(" Number of Games:", "yellow", attrs=["bold", "reverse"]) + " " + str(num_game))
            print(colored(" Number of Wins:", "green", attrs=["bold", "reverse"]) + " " + str(num_win))
            print(colored(" Number of Losses:", "red", attrs=["bold", "reverse"]) + " " + str(num_loss))
            print(colored(" Win Rate:", "magenta", attrs=["bold", "reverse"]) + " %" + str(int(win_rate * 100))) 
        else:
            print(colored(" There is no game log " +
                      emoji.emojize(":pensive: ", language="alias"), "red", attrs=["reverse"]))        
        Separator()
    else:
        print("See you later... Good bye" + emoji.emojize(":wave: ", language="alias"))
        print(emoji.emojize(":crystal_ball: ", language="alias") +
              "Mischief Managed " +
              emoji.emojize(":crystal_ball: ", language="alias"))
        break
# ------------------------------------------------------------------------