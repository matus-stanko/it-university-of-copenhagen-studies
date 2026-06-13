import random

#user and computer options (Without Quiting)
computer_options = ["R", "P", "S"]
user_options     = ["R", "P", "S", "W"]

#Function to check if user_input is valid, meaning that input is in user_options list
def is_valid(user_input):
    if user_input in user_options:
        return True

#welcoming message
print("Welcome to Rock, Paper, Scissors, Worldpeace!")   

#assign new variable user_input with empty string
user_input = ""

while user_input.upper() != "Q":    #check if user input (upper) is not Q
    user_input = input(("Rock, paper, scissors, worldpeace, or quit? (R, P, S, W, Q)"))  #ask for input
    user_input = user_input.upper()   #upper input

    if is_valid(user_input):  #check if user input is valid option
        computer_choice = random.choice(computer_options)   #let pc choose 
        
        #Now check for all possible options and write output
        if user_input == "R":                      
            if computer_choice == "R":
                print(f"{user_input}:{computer_choice} - it's a tie!")
            elif computer_choice == "P":
                print(f"{user_input}:{computer_choice} - you lose!")
            else:
                print(f"{user_input}:{computer_choice} - you win!")

        elif user_input == "P":
            if computer_choice == "P":
                print(f"{user_input}:{computer_choice} - it's a tie!")
            elif computer_choice == "S":
                print(f"{user_input}:{computer_choice} - you lose!")
            else:
                print(f"{user_input}:{computer_choice} - you win!")
        
        elif user_input == "S":
            if computer_choice == "S":
                print(f"{user_input}:{computer_choice} - it's a tie!")
            elif computer_choice == "R":
                print(f"{user_input}:{computer_choice} - you lose!")
            else:
                print(f"{user_input}:{computer_choice} - you win!")

        else:
            print("Worldpeace - you win!")
else:  #if Q/q was input then end game, else repeat
    print("Thanks for playing! The game is over now.")