import questionary
import sys

def simulation_info():
    #Create a questionaire to inquire about the number of years to run
    simulation_years = questionary.text("How many years do you want to simulate?").ask()

    #Validate the data is accurate to run the model
    simulation_years = float(simulation_years)
    if simulation_years <=0:
        sys.exit("Sorry, the number of years provided is not valid. Please insert a number above 1")

    #Create a questionaire to inquire about the number of simulations to run
    number_of_simulations = questionary.text("How many simulations do you want to run (min:500)?").ask()

    #Validate the data is accurate to run the model
    number_of_simulations = int(number_of_simulations)
    if number_of_simulations <500:
        sys.exit("Sorry, the number of simulations is not enough to draw a conclusion. Please insert a number above 500")

    #Create a questionaire to inquire about the amount to invest
    investment_amount = questionary.text("How much do you want to invest?").ask()

    #Validate the data is accurate to run the model
    investment_amount = float(investment_amount)
    if investment_amount <=0:
        sys.exit("Sorry, the amount submited is not correct. Please select a number >0")

    return simulation_years, number_of_simulations, investment_amount