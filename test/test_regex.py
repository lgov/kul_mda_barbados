import logging
import re
import unittest


class TestUseRegex(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')

    def test_parse_foundation_year_of_a_comp(self):
        """
        Extract the year a company was founded from the text.
        """

        text = """
        The Sherwin-Williams Company develops, manufactures, distributes, and sells paints, coatings, and related products to professional, industrial, commercial, and retail customers. It operates in three segments: The Americas Group, Consumer Brands Group, and Performance Coatings Group. The Americas Group segment offers architectural paints and coatings, and protective and marine products, as well as OEM product finishes and related products for architectural and industrial paint contractors, and do-it-yourself homeowners. The Consumer Brands Group segment provides branded and private-label architectural paints, stains, varnishes, industrial products, wood finishes products, wood preservatives, applicators, corrosion inhibitors, aerosols, caulks, and adhesives to retailers and distributors. The Performance Coatings Group segment develops and sells industrial coatings for wood finishing and general industrial applications, automotive refinish products, protective and marine coatings, coil coatings, packaging coatings, and performance-based resins and colorants. It serves retailers, dealers, jobbers, licensees, and other third-party distributors through its branches and direct sales staff, as well as through outside sales representatives. The company has operations primarily in North and South America, the Caribbean, Europe, Asia, and Australia. As of December 31, 2021, it operated 4,774 company-operated stores. The Sherwin-Williams Company was founded in 1866 and is headquartered in Cleveland, Ohio.
        """
        m = re.search(r'was founded in (\d{4}).*', text)
        self.assertIsNotNone(m)
        self.assertEqual("1866", m.group(1))

        text = """
        The Home Depot, Inc. operates as a home improvement retailer. It operates The Home Depot stores that sell various building materials, home improvement products, building materials, lawn and garden products, and dÃ©cor products, as well as provide installation, home maintenance, and professional service programs to do-it-yourself and professional customers. The company also offers installation programs that include flooring, cabinets and cabinet makeovers, countertops, furnaces and central air systems, and windows; and professional installation in various categories sold through its stores and in-home sales programs, as well as acts as a general contractor to provide installation services to its do-it-for-me customers through third-party installers. In addition, it provides tool and equipment rental services. The company primarily serves homeowners; and professional renovators/remodelers, general contractors, handymen, property managers, building service contractors, and specialty tradesmen, such as electricians, plumbers, and painters. It also sells its products online. As of January 31, 2021, the company operated 2,296 retail stores in the United States, including the Commonwealth of Puerto Rico, and the territories of the U.S. Virgin Islands and Guam; Canada; and Mexico. The Home Depot, Inc. was incorporated in 1978 and is based in Atlanta, Georgia.
        """
        m = re.search(r'was founded in (\d{4}).*|was incorporated in (\d{4}).*', text)
        self.assertIsNotNone(m)
        self.assertEqual("1978", m.group(2))

        text = """
        Blackrock Resources & Commodities Strategy Trust is a closed-ended equity mutual fund launched by BlackRock, Inc. It is co-managed by BlackRock Advisors, LLC and BlackRock International Limited. The fund invests in the public equity markets of the United States. It seeks to invest in stocks of companies operating in the commodities or natural resources sectors. The fund also invests through derivatives with exposure to commodity or natural resources companies, with an emphasis on option writing. Blackrock Resources & Commodities Strategy Trust was formed on March 30, 2011 and is domiciled in the United States.
        """
        m = re.search(r'was formed on [A-Za-z]+ \d+, (\d{4}).*', text)
        self.assertIsNotNone(m)
        self.assertEqual("2011", m.group(1))
        ''