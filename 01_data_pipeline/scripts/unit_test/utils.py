##############################################################################
# Import necessary modules and files
##############################################################################


import pandas as pd
import os
import sqlite3
from sqlite3 import Error
from constants import *
from city_tier_mapping import city_tier_mapping


###############################################################################
# Define the function to build database
###############################################################################


def build_dbs():
    """
    This function checks if the db file with specified name is present
    in the /Assignment/01_data_pipeline/scripts folder. If it is not present it creates
    the db file with the given name at the given path.


    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should exist


    OUTPUT
    The function returns the following under the given conditions:
        1. If the file exists at the specified path
                prints 'DB Already Exists' and returns 'DB Exists'

        2. If the db file is not present at the specified loction
                prints 'Creating Database' and creates the sqlite db
                file at the specified path with the specified name and
                once the db file is created prints 'New DB Created' and
                returns 'DB created'


    SAMPLE USAGE
        build_dbs()
    """
    if os.path.isfile(DB_PATH + "/" + DB_FILE_NAME):
        print("DB Already Exsist")
        return "DB Exsists"
    else:
        print("Creating Database")
        """ create a database connection to a SQLite database """
        print(DB_PATH + "/" + DB_FILE_NAME)
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME)
            print("New DB Created")
        except Error as e:
            print("Error", e)
            return "Error"
        finally:
            if conn:
                conn.close()
                return "DB Created"


###############################################################################
# Define function to load the csv file to the database
###############################################################################


def load_data_into_db():
    """
    Thie function loads the data present in data directory into the db
    which was created previously.
    It also replaces any null values present in 'total_leads_droppped' and
    'referred_lead' columns with 0.


    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be
        DATA_DIRECTORY : path of the directory where 'leadscoring.csv'
                        file is present


    OUTPUT
        Saves the processed dataframe in the db in a table named 'loaded_data'.
        If the table with the same name already exsists then the function
        replaces it.


    SAMPLE USAGE
        load_data_into_db()
    """
    # read the data present in data directory
    df = pd.read_csv(DATA_DIRECTORY)

    # replace any null values present in 'total_leads_droppped' and
    # 'referred_lead' columns with 0
    df["total_leads_droppped"].fillna(0, inplace=True)
    df["referred_lead"].fillna(0, inplace=True)

    # save the processed dataframe in the db in a table named 'loaded_data'
    df.to_sql(
        "loaded_data",
        con=sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME),
        index=False,
        if_exists="replace",
    )

    print("Data loaded into db")
    return


###############################################################################
# Define function to map cities to their respective tiers
###############################################################################


def map_city_tier(DB_FILE_NAME, DB_PATH):
    """
    This function maps all the cities to their respective tier as per the
    mappings provided in the city_tier_mapping.py file. If a
    particular city's tier isn't mapped(present) in the city_tier_mapping.py
    file then the function maps that particular city to 3.0 which represents
    tier-3.


    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be
        city_tier_mapping : a dictionary that maps the cities to their tier


    OUTPUT
        Saves the processed dataframe in the db in a table named
        'city_tier_mapped'. If the table with the same name already
        exsists then the function replaces it.


    SAMPLE USAGE
        map_city_tier()

    """
    # read the city_tier_mapping.py file
    city_tier_mapping = pd.read_csv(
        "/mlflow-assignment/01_data_pipeline/scripts/city_tier_mapping.py"
    )

    # read the db file
    conn = sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME)
    df = pd.read_sql_query("SELECT * FROM loaded_data", conn)

    # create a new column 'city_tier'
    df["city_tier"] = df["city"].map(city_tier_mapping)

    # replace any null values present in 'city_tier' column with 3.0
    df["city_tier"].fillna(3.0, inplace=True)

    # save the processed dataframe in the db in a table named 'city_tier_mapped'
    df.to_sql(
        "city_tier_mapped",
        con=sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME),
        index=False,
        if_exists="replace",
    )
    return


###############################################################################
# Define function to map insignificant categorial variables to "others"
###############################################################################


def map_categorical_vars(
    DB_FILE_NAME, DB_PATH, list_platform, list_medium, list_source
):
    """
    This function maps all the insignificant variables present in 'first_platform_c'
    'first_utm_medium_c' and 'first_utm_source_c'. The list of significant variables
    should be stored in a python file in the 'significant_categorical_level.py'
    so that it can be imported as a variable in utils file.


    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be present
        list_platform : list of all the significant platform.
        list_medium : list of all the significat medium
        list_source : list of all rhe significant source

        **NOTE : list_platform, list_medium & list_source are all constants and
                 must be stored in 'significant_categorical_level.py'
                 file. The significant levels are calculated by taking top 90
                 percentils of all the levels. For more information refer
                 'data_cleaning.ipynb' notebook.


    OUTPUT
        Saves the processed dataframe in the db in a table named
        'categorical_variables_mapped'. If the table with the same name already
        exsists then the function replaces it.


    SAMPLE USAGE
        map_categorical_vars()
    """
    # read the db file
    conn = sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME)
    df = pd.read_sql_query("SELECT * FROM loaded_data", conn)

    # create a new column 'first_platform_c'
    df["first_platform_c"] = df["first_platform"].map(list_platform)

    # create a new column 'first_utm_medium_c'
    df["first_utm_medium_c"] = df["first_utm_medium"].map(list_medium)

    # create a new column 'first_utm_source_c'
    df["first_utm_source_c"] = df["first_utm_source"].map(list_source)

    # save the processed dataframe in the db in a table named
    # 'categorical_variables_mapped'
    df.to_sql(
        "categorical_variables_mapped",
        con=sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME),
        index=False,
        if_exists="replace",
    )
    return


##############################################################################
# Define function that maps interaction columns into 4 types of interactions
##############################################################################
def interactions_mapping(
    DB_FILE_NAME,
    DB_PATH,
    INTERACTION_MAPPING,
    INDEX_COLUMNS_TRAINING,
    INDEX_COLUMNS_INFERENCE,
    NOT_FEATURES,
):
    """
    This function maps the interaction columns into 4 unique interaction columns
    These mappings are present in 'interaction_mapping.csv' file.


    INPUTS
        DB_FILE_NAME: Name of the database file
        DB_PATH : path where the db file should be present
        INTERACTION_MAPPING : path to the csv file containing interaction's
                                   mappings
        INDEX_COLUMNS_TRAINING : list of columns to be used as index while pivoting and
                                 unpivoting during training
        INDEX_COLUMNS_INFERENCE: list of columns to be used as index while pivoting and
                                 unpivoting during inference
        NOT_FEATURES: Features which have less significance and needs to be dropped

        NOTE : Since while inference we will not have 'app_complete_flag' which is
        our label, we will have to exculde it from our features list. It is recommended
        that you use an if loop and check if 'app_complete_flag' is present in
        'categorical_variables_mapped' table and if it is present pass a list with
        'app_complete_flag' column, or else pass a list without 'app_complete_flag'
        column.


    OUTPUT
        Saves the processed dataframe in the db in a table named
        'interactions_mapped'. If the table with the same name already exsists then
        the function replaces it.

        It also drops all the features that are not requried for training model and
        writes it in a table named 'model_input'


    SAMPLE USAGE
        interactions_mapping()
    """