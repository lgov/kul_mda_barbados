## Project code organisation

requirements.txt: all packages that need to be installed to run the downloader, parser and notebooks

**test/**
Unit tests for the 13F form parser

**src/**

_form_13f_downloader.py_: loads the 13F forms from the sec.gov website

_form_13f_parser_: parse both the XML and Tabular formatted 13F files, saves it contents in data/all_submission_files.xlsx

_cusip_to_ticker_converter.py_: uses api.openfigi.com and marketwatch.com to fetch for each cusip in the list the corresponding ticker symbol and extra information.
The ticker symbols will be stored in data/all_submission_files2.xlsx, all metadata will be stored in data/stock_info.json

_clustering.py_: supporting code for the kmeans clustering notebook.

**exploratory/**

_exploratory_data_analysis.ipynb_: explores the 13F forms that we collected.

_Read_the_extra_data.ipynb_: reads data/stock_info.json, parses the company description to extract the year of foundation and saves all in data/investee_info.xlsx.

_networkX.ipynb, networkX_community_detection.ipynb, networkX_community_detection_yearOfFoundation.ipynb, networkX_community_detection_sector.ipynb: 
Intermediary notebooks. Implements community detection using networkX_ respectively by
number of overlapping holdings, year of foundation of the investees and industry/sector of the investees.

_Clustering analysis and community detection.ipynb_: Combination notebook, the **final notebook** that combines all intermediary work.
