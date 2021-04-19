import logging
import unittest
import xml.etree.ElementTree as ET

from form_13f_parser import parse_submission_file


class TestParseSubmissionFile(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')

    def test_parse_vanguard_2019_submision(self):
        """
        """
        file_name = "data/102909-full-submission.txt"
        parsed_data = parse_submission_file(file_name)
        # ET.dump(parsed_data)

        # parsed_data is an xml ElementTree element, so we can use xpath to browse the
        # tree
        ns = { "ns2": "http://www.sec.gov/edgar/thirteenffiler"}
        value = parsed_data.find('.//ns2:edgarSubmission/ns2:headerData/ns2:filerInfo/ns2:filer/ns2:credentials/ns2:cik', ns).text
        self.assertEqual("0000102909", value)
