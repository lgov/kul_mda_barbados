import logging
import unittest

from form_13f_parser import parse_submission_file, parse_investment_from_xml, \
    parse_cid_from_table


class TestParseSubmissionFile(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')


    def test_parse_vanguard_2019_submision(self):
        """
        Submission file containing XML
        """
        file_name = "data/102909-full-submission.txt"
        investment_els = parse_submission_file(file_name)

        self.assertTrue(isinstance(investment_els, list))
        self.assertEqual(13483, len(investment_els))

        first_investment = investment_els[0]
        self.assertTrue(isinstance(first_investment, dict))
        self.assertEqual("0000102909", first_investment['cik'])

    def test_parse_table_submision(self):
        """
        Submission file containing fixed-width table
        """
        file_name = "data/885709-12-10-no-xml-full-submission.txt"
        investment_els = parse_submission_file(file_name)

        self.assertTrue(isinstance(investment_els, list))
        self.assertEqual(212, len(investment_els))

        first_investment = investment_els[0]
        self.assertTrue(isinstance(first_investment, dict))
        self.assertEqual("0000885709", first_investment['cik'])

    def test_parse_table_diff_layout_submision(self):
        """
        Submission file containing fixed-width table
        """
        file_name = "data/885709-11-55-no-xml-full-submission.txt"
        investment_els = parse_submission_file(file_name)

        self.assertTrue(isinstance(investment_els, list))
        self.assertEqual(253, len(investment_els))

        first_investment = investment_els[0]
        self.assertTrue(isinstance(first_investment, dict))
        self.assertEqual("0000885709", first_investment['cik'])

    def test_parse_table_diff_layout2_submision(self):
        """
        Submission file containing fixed-width table
        """
        file_name = "data/885709-01-04-no-xml-full-submission.txt"
        investment_els = parse_submission_file(file_name)

        self.assertTrue(isinstance(investment_els, list))
        self.assertEqual(79, len(investment_els))

        first_investment = investment_els[0]
        self.assertTrue(isinstance(first_investment, dict))
        self.assertEqual("0000885709", first_investment['cik'])

    def test_parse_table_cid_from_accession_number(self):
        accession_number = "0000885709-12-000010"
        self.assertEqual("0000885709", parse_cid_from_table(accession_number))
