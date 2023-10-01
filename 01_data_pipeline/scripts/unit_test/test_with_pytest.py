##############################################################################
# Import the necessary modules
##############################################################################
import pandas as pd
import os
import sqlite3
from sqlite3 import Error
from constants import *
from city_tier_mapping import city_tier_mapping
from utils import *
import unittest


###############################################################################
# Write test cases for load_data_into_db() function
# ##############################################################################
class TestMyModule(unittest.TestCase):
    def test_load_data_into_db(self):
        """_summary_
        This function checks if the load_data_into_db function is working properly by
        comparing its output with test cases provided in the db in a table named
        'loaded_data_test_case'

        INPUTS
            DB_FILE_NAME : Name of the database file 'utils_output.db'
            DB_PATH : path where the db file should be present
            UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

        SAMPLE USAGE
            output=test_get_data()

        """
        load_data_into_db()

        cnx = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        loaded_data = pd.read_sql("select * from loaded_data", cnx)

        cnx_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
        test_case = pd.read_sql("select * from loaded_data_test_case", cnx_ut)

        cnx.close()
        cnx_ut.close()

        self.assertTrue(test_case.equals(loaded_data))

    ###############################################################################
    # Write test cases for map_city_tier() function
    # ##############################################################################
    def test_map_city_tier(self):
        """_summary_
        This function checks if map_city_tier function is working properly by
        comparing its output with test cases provided in the db in a table named
        'city_tier_mapped_test_case'

        INPUTS
            DB_FILE_NAME : Name of the database file 'utils_output.db'
            DB_PATH : path where the db file should be present
            UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

        SAMPLE USAGE
            output=test_map_city_tier()

        """
        map_city_tier()

        conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        city_tier_mapped = pd.read_sql("select * from city_tier_mapped", conn)

        conn_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
        test_case = pd.read_sql("select * from city_tier_mapped_test_case", conn_ut)

        conn.close()
        conn_ut.close()

        self.assertTrue(test_case.equals(city_tier_mapped))

    ###############################################################################
    # Write test cases for map_categorical_vars() function
    # ##############################################################################
    def test_map_categorical_vars(self):
        """_summary_
        This function checks if map_cat_vars function is working properly by
        comparing its output with test cases provided in the db in a table named
        'categorical_variables_mapped_test_case'

        INPUTS
            DB_FILE_NAME : Name of the database file 'utils_output.db'
            DB_PATH : path where the db file should be present
            UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

        SAMPLE USAGE
            output=test_map_cat_vars()

        """
        map_categorical_vars()

        cnx = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        categorical_variable_mapped = pd.read_sql(
            "select * from categorical_variables_mapped", cnx
        )

        cnx_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
        test_case = pd.read_sql(
            "select * from categorical_variables_mapped_test_case", cnx_ut
        )

        print(categorical_variable_mapped.head())
        print(test_case.head())
        cnx.close()
        cnx_ut.close()

        self.assertTrue(test_case.equals(categorical_variable_mapped))

    ###############################################################################
    # Write test cases for interactions_mapping() function
    # ##############################################################################
    def test_interactions_mapping(self):
        """_summary_
        This function checks if test_column_mapping function is working properly by
        comparing its output with test cases provided in the db in a table named
        'interactions_mapped_test_case'

        INPUTS
            DB_FILE_NAME : Name of the database file 'utils_output.db'
            DB_PATH : path where the db file should be present
            UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

        SAMPLE USAGE
            output=test_column_mapping()

        """
        interactions_mapping()

        cnx = sqlite3.connect(DB_PATH + DB_FILE_NAME)
        interactions_mapped = pd.read_sql("select * from interactions_mapped", cnx)

        cnx_ut = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
        test_case = pd.read_sql("select * from interactions_mapped_test_case", cnx_ut)

        cnx.close()
        cnx_ut.close()

        self.assertTrue(test_case.equals(interactions_mapped))


if __name__ == "__main__":
    unittest.main()
