import json
import urllib.request

def cusip_to_symbol(cusip):
    with urllib.request.urlopen(
            f'https://d.yimg.com/autoc.finance.yahoo.com/autoc?query={cusip}&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback') as url:
        print("dd")
        #data = json.loads(url.read().decode())
        #print(data)
cusip_to_symbol("011642105")