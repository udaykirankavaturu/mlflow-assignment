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

        cnx = sqlite3.connect(DB_PATH + "/" + DB_FILE_NAME)
        loaded_data = pd.read_sql("select * from loaded_data", cnx)

        cnx_ut = sqlite3.connect(DB_PATH + "/" + UNIT_TEST_DB_FILE_NAME)
        test_case = pd.read_sql("select * from loaded_data_test_case", cnx_ut)

        cnx.close()
        cnx_ut.close()

        assert test_case.equals(loaded_data)
        self.assertEqual(loaded_data, test_case)


if __name__ == "__main__":
    unittest.main()


###############################################################################
# Write test cases for map_city_tier() function
# ##############################################################################
def test_map_city_tier():
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


###############################################################################
# Write test cases for map_categorical_vars() function
# ##############################################################################
def test_map_categorical_vars():
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


###############################################################################
# Write test cases for interactions_mapping() function
# ##############################################################################
def test_interactions_mapping():
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
