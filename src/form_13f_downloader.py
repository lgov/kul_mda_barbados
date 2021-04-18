from sec_edgar_downloader import Downloader
import pandas
from secedgar.filings import Filing, FilingType

loader = Downloader("../data")


def download_form(cik, form_type="13F-HR"):
    """
    Download the XML form from the Edgar website for company <cik>
    :param cik: integer id of company
    :param form_type: optional form type id
    :return:
    """
    # Pad number with zeroes up to 10 characters
    cik_str = f'{cik:010}'
    result = loader.get(form_type, cik_str)
    pass


def get_cik_list_of_state(state):
    """
        Reads the CIK_list,csv file and returns a pandas dataframe containing companies from state <state>
        :param state: the state of the investment company
        :return: dataframe containing data for investment companies from state <state>
        """
    df = pandas.read_csv('../data/CIK_list.csv')
    return df.loc[df['State'] == state]

def download_forms_from_cik(state):
    df = get_cik_list_of_state(state)
    for cik in df['CIK Number']:
        download_form(cik)
        print(f'downloaded cik: {cik}')

download_forms_from_cik('CA')
# download_form(102909)
