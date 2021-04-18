import unittest
import logging
from src import form_13f_downloader as imp

class TestDownloadingSubmissionFile(unittest.TestCase):

    def test_get_cik_list_of_state(self):
        df = imp.get_cik_list_of_state('CA')
        self.assertEqual(len(df), 160)


if __name__ == '__main__':
    unittest.main()
