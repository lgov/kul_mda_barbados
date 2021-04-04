import logging
import unittest


def parse_submission_file(file_name):
    """
    Opens a file that was originally downloaded from the Edgar site and parse it.
    We assume that the file is a 13F-HR form
    :param file_name:
    :return: a dictionary with all relevant attributes from the document
    """
    # TODO: open file, parse it and return dictionary of data
    return {'cik': 'abcdef'}


class TestParseSubmissionFile(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')

    def test_parse_vanguard_2019_submision(self):
        """
        """
        file_name = "data/102909-full-submission.txt"
        parsed_data = parse_submission_file(file_name)
        self.assertEqual("102909", parsed_data['cik'])
