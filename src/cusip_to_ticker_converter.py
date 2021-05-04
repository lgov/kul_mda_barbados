from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_company_info_from_cusip(ListOfCusip):
    """

    :param ListOfCusip: a list of CUSIP identifiers.
    :return: returns a json object that contains information for each company, such as the ticker.
    """
    openfigi_url = 'https://api.openfigi.com/v1/mapping'
    openfigi_headers = {'Content-Type': 'text/json'}
    openfigi_headers['X-OPENFIGI-APIKEY'] = '59899e2c-d64a-42cc-b2fa-fd1c26a53b92'
    new_list = [{"idType":"ID_CUSIP","idValue":cusip} for cusip in ListOfCusip]
    response = requests.post(url=openfigi_url, headers=openfigi_headers,
                             json=new_list)
    return response.json()

def get_cusip_and_ticker_dict(path):
    """
    :param path: The path to the file containing the data
    :return: returns a dictionary with as key's the cusip and as value their ticker, if the ticker couldn't be found, then the value is None.
    """
    df = pd.read_excel(path)
    unique_list_cusip = list(dict.fromkeys(df['cusip']))
    unique_lists_cusip = [unique_list_cusip[x:x+100] for x in range(0, len(unique_list_cusip), 100)]
    cusip_and_ticker = dict()

    for i,li in enumerate(unique_lists_cusip):
        list_of_ticker = get_company_info_from_cusip(li)
        j = 0
        for cusip, result in zip(li, list_of_ticker):
            print(f'{i*100 + j}/{len(unique_list_cusip)}')
            temp = result.get("data",[])
            if len(temp) > 0:
                ticker = result.get("data",[])[0]["ticker"]
                cusip_and_ticker[cusip] = ticker
            else:
                company_name = df.loc[df['cusip'] == cusip, 'nameOfIssuer'].values[0]
                cusip_and_ticker[cusip] = get_ticker_from_company_name(company_name)
                #cusip_and_ticker[cusip] = None
            j +=1
    return cusip_and_ticker

def get_ticker_from_company_name(companyName):
    try:
        html_text = requests.get(
            f'https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup={companyName}&Country=all&Type=All',timeout=1).text
        soup = BeautifulSoup(html_text,'lxml')
        temp = soup.find('td', class_='bottomborder')
        temp2 = temp.find('a').text
        return temp2
    except:
        return None

def write_ticker_to_new_submission_files():
    dict = get_cusip_and_ticker_dict(r'../data/all_submission_files.xlsx')
    df = pd.read_excel(r'../data/all_submission_files.xlsx')
    df['ticker'] = [dict[cusip] for cusip in df['cusip']]
    df.to_csv(r'../data/all_submission_files2.csv')

write_ticker_to_new_submission_files()

