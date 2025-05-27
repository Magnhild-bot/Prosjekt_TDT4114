import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

project_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_dir / 'src'))
sys.path.insert(0, str(project_dir / 'notebooks'))

# Import the functions we will test
from Prediktivanalyse import predict_future
from Functions_FetchData import data_reader


# Unittest for the DataReader-function
class TestDataReader(unittest.TestCase):
    # Creates a temporary CSV file with the test data
    def setUp(self):
        self.test_csv = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv')
        self.test_csv.write("A,B,C\n1,2,3\n4,,6\n7,8,9\n-1,2,-3\n")
        self.test_csv.seek(0)
        self.test_csv.close()
        self.filename = self.test_csv.name
    # Deletes the temporary file after every test
    def delete_file(self):
        os.remove(self.filename)
    # Checks that a CSV-file is read correct and that the right messages is printed.
    def test_data_reader_valid(self):

        nanlimit = 20  # Allow up to 20% NaN.

        with StringIO() as buf, redirect_stdout(buf):
            df = data_reader(self.filename, nanlimit)
            output = buf.getvalue()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (4, 3))
        self.assertIn('The data reader code took ', output, ' seconds to run')

    # Makes sure the function exits when the file is not
    def test_data_reader_file_not_found(self):
        nanlimit = 10
        fake_filename = "non_existent_file.csv"

        with self.assertRaises(SystemExit):
            with StringIO() as buf, redirect_stdout(buf):
                data_reader(fake_filename, nanlimit)


# Unittest for the predict_future function
class TestPredictFuture(unittest.TestCase):
    # Simulated input data - linear trend from year 2000 to 2004
    def setUp(self):
        self.x = np.array([2000, 2001, 2002, 2003, 2004])
        self.y = np.array([10, 12, 14, 16, 18])

    # Check that prediction returns 24 future points - which is every month for 2 years.
    def test_predict_future_output(self):
        future_x, future_y = predict_future(self.x, self.y, years=2, label='Test', color='blue')

        self.assertEqual(len(future_x), 24)
        self.assertEqual(len(future_y), 24)
        self.assertTrue(np.all(future_x >= self.x[-1]))

    # Checks that empty input arrays gives a ValueError
    def test_predict_future_empty_input(self):
        with self.assertRaises(ValueError):
            predict_future(np.array([]), np.array([]))

    # Checks that empty input arrays gives a ValueError
    def test_predict_future_increasing(self):
        # Makes sure the predicted values increase over time
        future_x, future_y = predict_future(self.x, self.y, years=5)

        self.assertGreater(future_y[-1], future_y[0])


if __name__ == '__main__':
    unittest.main()
