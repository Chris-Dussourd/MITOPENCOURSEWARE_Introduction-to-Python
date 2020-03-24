#Uses Bisection Search Algorithm to find the portion saved needed to buy your dream house in 36 months.
print("This python file calculates the percentage you should save monthly if you want to buy your dream house in 3 years.")
portion_down_payment=0.25 #down-payment needed on the house
current_savings=0 #savings in account
r = 0.04 #annual rate of return

annual_salary = float(input("Please type in your annual salary:  "))
total_cost = 10**6  #Your dream house costs a million dollars
semi_annual_raise = 0.07 #The raise you get in percent every 6 months
epsilon=100 #The amount saved can be within epsilon of the down payment on the house

months_to_save=36 #Number of months before you want to reach your down payment
down_payment=portion_down_payment*total_cost

def calc_monthly_savings(salary,rate_of_return,savings,portion_saved):
    """
        salary: yearly salary (calculated monthly)
        rate_of_return: annual rate of return of savings account (calculated monthly)
        savings: money  already in savings account
        portion_saved:  percent of money set aside from salary into savings
        Calculates how much more money is in the savings account at the end of the month.
    """
    return salary/12.0*portion_saved+savings*rate_of_return/12


def calc_savings(salary,raise_6months,rate_of_return,time_months,savings,portion_saved):
    """
        salary: yearly salary (calculated monthly)
        raise_6months:  percent salary raise every 6 months
        time_months:    the length of time in months that we run the calculation
        rate_of_return: annual rate of return of savings account (calculated monthly)
        savings: money  already in savings account
        portion_saved:  percent of money set aside from salary into savings
        Calculate the amount of money in the savings account over a particular time period
    """
    months=0
    for months in range(time_months):
        if months != 0 and months%6==0:
            salary*=1+raise_6months
        savings+=calc_monthly_savings(salary,rate_of_return,savings,portion_saved)
    return savings

#Define upper and lower bound for bisection search. Start with 100% saved and 0%. 
# Note: 100.00%=10000 because we want to prevent an infinite loop with the Bisection search. Restrict answers to two decimals after percent.
upper_bound = 10000
lower_bound = 0
steps=0 #Number of times to loop through search

portion_saved=1
#Check if you can't reach your goal even if you save 100% of your earnings
savings_100=calc_savings(annual_salary,semi_annual_raise,r,months_to_save,0,portion_saved)
#If you saved enough in 36 months by setting aside 100% of your income, then continue with the search
if savings_100>down_payment:
    # Run the loop until you find a savings amount within epsilon of the down paymnet
    while(abs(down_payment-current_savings)>epsilon):
        portion_saved=(upper_bound+lower_bound)/10**4/2.0
        current_savings=calc_savings(annual_salary,semi_annual_raise,r,months_to_save,0,portion_saved)

        #If no solution found and upper_bound==lower_bound, we cannot find an exact solution. Exit loop
        if (abs(down_payment-current_savings)>epsilon) and (upper_bound==lower_bound):
            down_payment=0
            current_savings=0
        #Reset upper or lower bounds for bisection search
        if current_savings>down_payment: #We've saved too much; set the new upper_bound to portion_saved
            upper_bound=int(round(portion_saved*10**4))
        else:                            #We haven't saved enough; set the new lower_bound to portion_saved
            lower_bound=int(round(portion_saved*10**4))
        steps+=1

    if down_payment !=0: #Solution found
        print("You need to set aside",'{:.2f}%'.format(portion_saved*100),"of your salary to save",'${:,.2f}'.format(current_savings),"in 3 years.")
        print("This is within",'${:,.2f}'.format(epsilon),"of the down payment on your dream house.")
        print("It took",steps,"loops to reach the answer.")
    else: #No solution found
        print("We were not able to find an exact solution. The closest answer we obtained to portion saved is",'{:.2f}%'.format(portion_saved*100),".")
        print("We need to calculate more than two decimal places in order to obtain an exact answer.")
else:
    print("You cannot save enough money for a down payment in 3 years with a salary of",'${:,.2f}'.format(annual_salary),".")
