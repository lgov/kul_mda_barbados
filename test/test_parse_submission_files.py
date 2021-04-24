import logging
import unittest
from datetime import date

from form_13f_parser import parse_submission_file, parse_date_from_table, parse_date_from_xml,\
    parse_cid_from_table, parse_amount_times_1000


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
        self.assertEqual(date(2019, 3, 31), first_investment['report_end_date'])
        self.assertEqual(237000, first_investment['value'])
        self.assertEqual("1347 PPTY INS HLDGS INC", first_investment['nameOfIssuer'])

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
        self.assertEqual(date(2011,12,31), first_investment['report_end_date'])
        self.assertEqual(1774000, first_investment['value'])
        self.assertEqual("AT&T", first_investment['nameOfIssuer'])

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
        self.assertEqual(date(2011,9,30), first_investment['report_end_date'])
        self.assertEqual(35000, first_investment['value'])
        self.assertEqual("3M COMPANY", first_investment['nameOfIssuer'])

    def test_parse_table_diff_layout2_submision(self):
        """
        Submission file containing fixed-width table. Value x 1000
        """
        file_name = "data/885709-01-04-no-xml-full-submission.txt"
        investment_els = parse_submission_file(file_name)

        self.assertTrue(isinstance(investment_els, list))
        self.assertEqual(79, len(investment_els))

        first_investment = investment_els[0]
        self.assertTrue(isinstance(first_investment, dict))
        self.assertEqual("0000885709", first_investment['cik'])
        self.assertEqual(date(2001,3,31), first_investment['report_end_date'])
        self.assertEqual(160000, first_investment['value'])
        self.assertEqual("ACACIA RESEARCH CORP", first_investment['nameOfIssuer'])

    def test_parse_table_cid_from_accession_number(self):
        accession_number = "0000885709-12-000010"
        self.assertEqual("0000885709", parse_cid_from_table(accession_number))

    def test_parse_table_date(self):
        date_str = "20041026"
        self.assertEqual(date(2004, 10, 26), parse_date_from_table(date_str))

        # Test that whitespaces are stripped first.
        date_str = " 20041026"
        self.assertEqual(date(2004, 10, 26), parse_date_from_table(date_str))

    def test_parse_xml_date(self):
        date_str = "03-31-2019"
        self.assertEqual(date(2019, 3, 31), parse_date_from_xml(date_str))

        # Test that whitespaces are stripped first.
        date_str = " 03-31-2019"
        self.assertEqual(date(2019, 3, 31), parse_date_from_xml(date_str))

    def test_parse_amount_times_1000(self):
        value_str = "$   160"
        self.assertEqual(160000, parse_amount_times_1000(value_str))

        value_str = "--------"
        self.assertIsNone(parse_amount_times_1000(value_str))

        value_str = "1,774"
        self.assertEqual(1774000, parse_amount_times_1000(value_str))
