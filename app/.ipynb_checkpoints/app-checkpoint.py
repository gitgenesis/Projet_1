
#Import Modules:
import os
# Load .env file
load_dotenv('tiago_api.env')

# Set the variables for the Quandl API and secret keys
quandl_key = os.getenv("QUANDL_KEY")

# The `__main__` loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":

    # Database connection string to the clean NYSE database
    database_connection_string = 'sqlite:///../Resources/nyse.db'

    # Create an engine to interact with the database
    engine = sql.create_engine(database_connection_string)

    # Read the NYSE table into a dataframe called `nyse_df`
    nyse_df = pd.read_sql_table('NYSE', engine)

    # Get a list of the sector names from the `nyse_df` DataFrame
    # Be sure to drop n/a values and capture only unique values.
    # You will use this list of `sector` names for the user options in the report.
    sectors = nyse_df['Sector']
    sectors = sectors.dropna()
    sectors = sectors.unique()

    # Create a variable named running and set it to True
    running = True

    # While running is `True` call the `sector_report` function.
    # Pass the `nyse_df` DataFrame `sectors` and the database `engine` as parameters.
    while running:
        continue_running = sector_report(sectors, engine)
        if continue_running == 'y':
            running = True
        else:
            running = False