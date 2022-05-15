
#Import Modules:
import os
from sympy import re, simplify_logic
from actions.load_data import load_data
from actions.run_model import MC_run
from actions.initial_questions import simulation_info
import questionary
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")

#Create a function called 'running_app' that will generate all calculations based on the parameters
# This function will be called from the `__main__` loop.

def running_app(df):

    # Print a welcome message for the application
    print("\n......Welcome to WB Method App.....\n")
    print("This report will calculate the return of the S&P 500 based on the earnings it has generated.\n")

    #Getting the initial variables out of questionaire
    simulation_years, number_of_simulations, investment_amount = simulation_info()

    print("Running report ...")
    
    #run the model calculation based on the inputs
    ci_lower_price , ci_upper_price, mean_price = MC_run(df, number_of_simulations,simulation_years)
    
    return_price = mean_price / df.iloc[-1,1]


    # Create a statement that displays the results of the simulation.
    results = f"With 95% of confindence SPI prices will land between {ci_lower_price} and {ci_upper_price} in {simulation_years} years.\nIf you invest {investment_amount} you would expect to reach on average {round(investment_amount * return_price,2)}.\n Do you want to run another simulation?"

    # Using the `results` statement created above,
    # prompt the user to run the report again (`y`) or exit the program (`n`).
    continue_running = questionary.select(results, choices=['y', 'n']).ask()

    # Return the `continue_running` variable from the `sector_report` function
    return continue_running

# The `__main__` loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":

    # Load .env file
    load_dotenv('Resources/quandl_key.env')

    # Set the variables for the Quandl API and secret keys
    quandl_key = os.getenv("QUANDL_API_KEY")

    # Load all data to the APP
    df = load_data(quandl_key)

    # Create a variable named running and set it to True
    running = True

    # While running is `True` call the `sector_report` function.
    # Pass the `nyse_df` DataFrame `sectors` and the database `engine` as parameters.
    while running:
        continue_running = running_app(df)
        if continue_running == 'y':
            running = True
        else:
            running = False