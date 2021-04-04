from sec_edgar_downloader import Downloader

loader = Downloader("./data")

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

download_form(102909)
