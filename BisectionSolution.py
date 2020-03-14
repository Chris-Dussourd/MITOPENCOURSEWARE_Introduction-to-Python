
#Function that checks parameter can be converted to float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

import math
#Use Bisection algorithm to find a solution to the cube root of a number
print("This python file uses a Bisection algorithm to find an approximate cube root of a number.")
#Get the user input:
user_input=input("Please enter a number to find the approximate cube root:  ")
while not is_float(user_input) or math.isnan(float(user_input)):
    user_input=input("You did not enter a number. Please try again:  ")

user_val=float(user_input)
num_guesses=1
epsilon=0.0001 #The solution cubed must be within epsilon of the user input

if abs(user_val)>1:
    #Upper and lower bounds of the solution (only calculate for positive, change the sign of number at the end)
    upper_val=abs(user_val) 
    lower_val=1
    number=1
    while abs(number**3-abs(user_val))>epsilon:
        number=(upper_val+lower_val)/2.0
        #If guessed number cubed is less than user input, then solution must be greater than the number. The new lower limit is the guessed number.
        if number**3<abs(user_val):
            lower_val=number 
        #If guessed number cubed is greater than user input, then solution much be less than the number. The new upper limit is the guessed number.
        else:
            upper_val=number
        num_guesses+=1
    number=math.copysign(number,user_val) #Change the sign of number to match the user input
#Upper and lower bounds are changed for user input between -1 and 1
else:
    #Upper and lower bounds
    upper_val=1
    lower_val=abs(user_val) #Lower val is user input because a number in between -1 and 1 is greater than itself cubed 
    #(Example: .5^3=.125, lower_val=.125, upper_val=1, .5 is between .125 and 1))
    number=lower_val
    while abs(number**3-abs(user_val))>epsilon:
        number=(upper_val+lower_val)/2.0
        #If guessed number cubed is less than user input, then solution must be greater than the number. The new lower limit is the guessed number.
        if number**3<abs(user_val):
            lower_val=number
        #If guessed number cubed is greater than user input, then solution much be less than the number. The new upper limit is the guessed number.
        else:
            upper_val=number
        num_guesses+=1
    number=math.copysign(number,user_val) #Change the sign of number to match the user input

print("The number",number,"cubed is",number**3,"which is within",abs(epsilon),"of your input.")
print("It took",num_guesses,"guesses to get to the solution.")