import logging
import unittest

from form_13f_parser import parse_submission_file, parse_investment


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
        ns = { "ns1": "http://www.sec.gov/edgar/thirteenffiler"}
        cik = parsed_data.find('.//ns1:edgarSubmission/ns1:headerData/ns1:filerInfo/ns1:filer/ns1:credentials/ns1:cik', ns).text
        self.assertEqual("0000102909", cik)

        # List the companies the investment fund is investing in
        ns = {"ns1": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
        investment_els = parsed_data.findall('.//ns1:informationTable/ns1:infoTable', ns)
        self.assertEqual(13483, len(investment_els))
        for investment_el in investment_els:
            investment = parse_investment(investment_el)
            print(investment)

        pass

