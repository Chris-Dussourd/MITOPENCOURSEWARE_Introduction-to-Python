print("This python file calculates how long it will take for you to save for your dream house.")
portion_down_payment=0.25 #down-payment needed on the house
current_savings=0 #savings in account
r = 0.04 #annual rate of return

annual_salary = float(input("Please type in your annual salary:  "))
portion_saved = float(input("Please type in the portion you will keep in savings (decimal percent):  "))
total_cost = float(input("Please type in the price of your dream house:  "))
semi_annual_raise = float(input("Please type in the raise you get bi-annually (decimal percent):"))

def calc_monthly_savings(annual_salary,portion_saved,current_savings,rate_of_return):
    """
        annual_salary: yearly salary (calculated monthly)
        portion_saved: percent of money set aside from salary into savings
        current_savings: amount of money currently in savings
        rate_of_return: annual rate of return (calculated monthly)
        Calculates how much more money is in the savings account at the end of the month.
    """
    return annual_salary/12.0*portion_saved+current_savings*rate_of_return/12

months=0
# Run the loop until the current savings is enough to pay the down payment on the house
# Each run of the loop in a new month
while(total_cost*portion_down_payment>current_savings):
    current_savings+=calc_monthly_savings(annual_salary,portion_saved,current_savings,r)
    months+=1
    if months%6==0:
        annual_salary*=1+semi_annual_raise

print("It will take you",months,"months to save for the down payment on your dream house.")