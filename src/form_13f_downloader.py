import feedparser as fp
import re
import urllib3
import os


def download_13f_hr_files(state):
    """
    Summmary Downloads the filings from the sec archive of the investment companies from a given state.
    """
    i = 0
    max_companies = 200
    valid_file = True
    list_of_companies = []
    while len(set(list_of_companies)) < max_companies and valid_file:
        feed = fp.parse(
            f'https://www.sec.gov/cgi-bin/srch-edgar?text=Form-Type%3D13F-HR&start={80 * i + 1}&count={80 * (i + 1)}&first=2015&last=2021&output=atom')
        if len(feed.entries) == 0:
            # Checks if the RSS file is valid.
            valid_file = False
        for entry in feed.entries:
            # checks if the company is incorporated in the given state
            text_name = entry.link.replace("-index.htm", ".txt")
            http = urllib3.PoolManager()
            text = http.request('GET', text_name).data
            temp = re.search(f'STATE OF INCORPORATION:{state}', text.decode().replace("\t", ""))
            if (temp != None):
                #  make new directory given the file name and store filings in this directory.
                file_name = re.search("data/.*\.txt", text_name).group()
                if file_name != None:
                    try:
                        os.makedirs(f'{os.path.dirname(file_name)}', exist_ok=True)
                        with open(f'{file_name}', "wb") as f:
                            f.write(text)
                        company_name = entry.title.replace("13F-HR - ", "")
                        list_of_companies.append(company_name)
                        break
                    except Exception as e:
                        print(e)
        i += 1


download_13f_hr_files('CA')
