## Project code organisation

requirements.txt: all packages that need to be installed to run the downloader, parser and notebooks

* test/
Unit tests for the 13F form parser

* src/

form_13f_downloader.py: loads the 13F forms from the sec.gov website

form_13f_parser: parse both the XML and Tabular formatted 13F files, saves it contents in data/all_submission_files.xlsx

cusip_to_ticker_converter.py: uses api.openfigi.com and marketwatch.com to fetch for each cusip in the list the corresponding ticker symbol and extra information.
The ticker symbols will be stored in data/all_submission_files2.xlsx, all metadata will be stored in data/stock_info.json

clustering.py: supporting code for the kmeans clustering notebook.

* exploratory/

exploratory_data_analysis.ipynb: explores the 13F forms that we collected.

Read_the_extra_data.ipynb: reads data/stock_info.json, parses the company description to extract the year of foundation and saves all in data/investee_info.xlsx.

networkX.ipynb
networkX_community_detection.ipynb
networkX_community_detection_yearOfFoundation.ipynb
networkX_community_detection_sector.ipynb: 
Internmediary notebooks. Implements community detection using networkX respectively by
number of overlapping holdings, year of foundation of the investees and industry/sector of the investees.

