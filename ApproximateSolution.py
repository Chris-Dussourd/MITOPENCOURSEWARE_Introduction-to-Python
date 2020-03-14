import math
#Function that checks parameter can be converted to float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#Approximate Solution Algorithm example for finding the cube root.
#Algorithm loops through guesses and increments guesses by the step variable until a solution is found (or no solution can be found).
print("This python file finds an approximate solution to the cube root of the user input.")
user_input=input("Please enter a number to find the approximate cube root:  ")
while not is_float(user_input) or math.isnan(float(user_input)):
    user_input=input("You did not enter a number. Please enter a number:  ")

user_val=float(user_input)
epsilon=0.01 #This is how close we would like to get to the user's input.
if user_val>0:
    step=0.01    #Step by this amount. Brute force test all numbers up until the user's input
else:
    step=-0.01   #User supplied a negative number
num_guesses=1  #First guess is zero.

if abs(user_val)>=1:
    number=1     #Number iterates up until finding a suitable cube root or doesn't find an answer
    #Loop until approximate solution is found or until abs(number) > abs(user_val) (no solution was found)
    while abs(number**3-user_val)>epsilon and abs(number)<=abs(user_val):
        number+=step
        num_guesses+=1
else: #If user value is within -1 and 1, the abs(number)>abs(user_val) if a solution is found (Ex: The cube root of .000125 = .05 and .05>.000125)
    number=0     #Number iterates up until finding a suitable cube root or doesn't find an answer
    #Loop until approximate solution is found or number greater than 1 or less than -1 (no solution was found)
    while abs(number**3-user_val)>epsilon and abs(number)<1:
        number+=step
        num_guesses+=1

if abs(number**3-user_val)<=epsilon:
    print("The number",format(number,'.2f'),"cubed is ",format(number**3,'.4f'),"which is within",abs(epsilon),"of your input.")
    print("It took",num_guesses,"guesses to get to the solution.")
else:
    print("We were not able to find a solution within",abs(epsilon),"of your input.")


