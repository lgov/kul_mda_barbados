import os
import tempfile
import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd
from datetime import datetime

def parse_submission_xml_file(text):
    """
    Opens a file that was originally downloaded from the Edgar site and parse it.
    We assume that the file is a 13F-HR form
    :param file_name:
    :return: a dictionary with all relevant attributes from the document
    """

    # Cut the text into blocks (lines) that start right after the <XML> tag
    result = text.split('<XML>')
    # Remove spaces and newline character right before and after each line
    result = [line.strip() for line in result]
    # Keep only the lines that contain and xml document
    result = [line for line in result if line.startswith('<?xml version="1.0"')]
    # Cut of the unneeded text right after the xml document.
    result = [line.split("</XML>")[0].strip() for line in result]

    # Does the file contain any XML blocks?
    if len(result) == 0:
        return None

    # Combine the multiple xml documents into one:
    # <form>
    #    <edgarSubmission>...</edgarSubmission>
    #    <informationTable>...</informationTable>
    # </form>
    form_node = ET.fromstring("<form></form>")
    for line in result:
        form_node.insert(0, ET.fromstring(line))

    # parsed_data is an xml ElementTree element, so we can use xpath to browse the
    # tree
    ns = { "ns1": "http://www.sec.gov/edgar/thirteenffiler"}
    cik = form_node.find('.//ns1:edgarSubmission/ns1:headerData/ns1:filerInfo/ns1:filer/ns1:credentials/ns1:cik', ns).text

    reportCalendarOrQuarter = form_node.find('.//ns1:edgarSubmission/ns1:formData/ns1:coverPage/ns1:reportCalendarOrQuarter', ns).text
    report_end_date = parse_date_from_xml(reportCalendarOrQuarter)
    # List the companies the investment fund is investing in
    ns = {"ns1": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
    investment_els = form_node.findall('.//ns1:informationTable/ns1:infoTable', ns)

    investments = [parse_investment_from_xml(cik, report_end_date, i) for i in investment_els]

    return investments


def parse_cid_from_table(accession_number):
    """
    Parse the cik number from the accession_number.
    Example: 0000885709-12-000010 -> 0000885709
    :param accession_number:
    :return: <string> cik
    """
    # Strip spaces, then split the string on the '-' characters into a list
    # ["0000885709", "12", "000010"]
    # From that list, return the first element.
    return accession_number.strip().split('-')[0]


def parse_date_from_table(date_str):
    """
    Parse the data from the date string.
    Example: "20041026" -> date(2004, 10, 26)
    :param date_str:
    :return: <datetime.date> date
    """

    # Clean whitespaces first, then parse the date string as format "yyyymmdd".
    # Convert the datetime object to a date object (as we don't have hour/minute here)
    date_str = date_str.strip()
    return datetime.strptime(date_str, "%Y%m%d").date()

def parse_date_from_xml(date_str):
    """
    Parse the data from the date string.
    Example: "03-31-2019" -> date(2019, 03, 31)
    :param date_str:
    :return: <datetime.date> date
    """

    # Clean whitespaces first, then parse the date string as format "yyyymmdd".
    # Convert the datetime object to a date object (as we don't have hour/minute here)
    date_str = date_str.strip()
    return datetime.strptime(date_str, "%m-%d-%Y").date()

def parse_submission_table_file(text):
    table_lines = []
    reading_table = False
    table_df = None
    report_end_date = cik = None

    for line in text.splitlines():
        if line.startswith('<'):
            if reading_table:
                if line.startswith('<S>'):
                    continue
                # We were reading the lines of the fixed-width table
                # pandas.read_fwf can only read from a file, not from a text buffer.
                # write the text to a temp file first.
                fd, p = tempfile.mkstemp()
                with os.fdopen(fd, 'w') as f:
                    f.write('\n'.join(table_lines))
                    f.write('\n')
                table_df = pd.read_fwf(p)
                break
            continue

        if reading_table:
            table_lines.append(line)
            continue

        # Parse all the key:value pairs we are interested in
        comps = line.strip().split(':')
        if comps[0] == "ACCESSION NUMBER":
            cik = parse_cid_from_table(comps[1])
            continue
        elif comps[0] == "CONFORMED PERIOD OF REPORT":
            report_end_date = parse_date_from_table(comps[1])
            continue
        # Skip key:value pairs we are not interested in
        if len(comps) > 1:
            continue

        if len(comps) == 1 and \
            (comps[0].strip().startswith("SECURITY ") or
             comps[0].strip().startswith('Name of Issuer ')):

            reading_table = True
            # Add the header line
            table_lines.append(line)
            continue

    if not table_df is None:
        # Strip all unneeded spaces from the column names
        table_df.columns = [' '.join(col.strip().split()) for col in table_df.columns]
        # Try to identify unnamed columns
        unnamed_cols = [col for col in table_df.columns if col.startswith('Unnamed')]
        for col in unnamed_cols:
            if "SH" in table_df[col].to_list():
                table_df.rename({col:'sshPrnamtType'})

        if 'PRN AMT PRN' in table_df.columns:
            new = table_df['PRN AMT PRN'].str.split(' ', n = 1, expand = True)
            table_df['sshPrnamt'] = new[0]
            table_df['sshPrnamtType'] = new[1]

        # Now rename the columns to what we are using internally. This is a bit tricky,
        # as in some files there are extra unnamed columns.
        COL_LIST = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt',
                    'sshPrnamtType' ,'cik']
        table_df = table_df.rename(columns={"SECURITY":"nameOfIssuer",
                                            "Name of Issuer": "nameOfIssuer",
                                            "TYPE":"titleOfClass",
                                            "Class": "titleOfClass",
                                            "CUSIP":"cusip",
                                            "MARKET":"value",
                                            "(x$1000)": "value",
                                            "SHARES":"sshPrnamt",
                                            "OPTIONTYPE":"sshPrnamtType"})
        table_df = table_df.loc[:, table_df.columns.isin(COL_LIST)]
        table_df["cik"] = cik
        table_df["report_end_date"] = report_end_date

        # Delete the table header separator row.
        if 'titleOfClass' in table_df.columns:
            table_df = table_df[~table_df['titleOfClass'].astype(str).str.startswith('----')]
        else:
            print("Error: table not in recognized format!")
            return None

        return table_df.to_dict('records')

    return None


def parse_submission_file(file_path):
    # Read all file content in memory
    with open(file_path) as f:
        text = f.read()

    if '<?xml version="1.0"' in text:
        return parse_submission_xml_file(text)
    else:
        return parse_submission_table_file(text)


def parse_investment_from_xml(cik, report_end_date, investment_el):
    """
    Parse an informationTable/infoTable xml element in a dictionary with the values
    we will use as elements.

    :param cik: <string> same cik for all investiments
    :param report_end_date:<date> same reportCalendarOrQuarter for all investiments
    :param investment_el: ElementTree element
    :return: dictionary
    """
    ns = {"ns1": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
    nameOfIssuer = investment_el.find('ns1:nameOfIssuer', ns).text
    titleOfClass = investment_el.find('ns1:titleOfClass', ns).text
    cusip = investment_el.find('ns1:cusip', ns).text
    value = investment_el.find('ns1:value', ns).text
    sshPrnamt = investment_el.find('ns1:shrsOrPrnAmt/ns1:sshPrnamt', ns).text
    sshPrnamtType = investment_el.find('ns1:shrsOrPrnAmt/ns1:sshPrnamtType', ns).text
    return {"report_end_date": report_end_date,
            "cik": cik,
            "nameOfIssuer": nameOfIssuer,
            "titleOfClass": titleOfClass,
            "cusip": cusip,
            "value": value,
            "sshPrnamt": sshPrnamt,
            "sshPrnamtType": sshPrnamtType
            }


def parse_all_13f_submission_files(root_folder):
    lst = []
    for subm_file in glob(os.path.join(root_folder, '**/*.txt'), recursive=True):
        print("Parsing file %s" % subm_file)
        investments = parse_submission_file(subm_file)
        if investments is None:
            print("  Skip file, no xml blocks found!")
            continue

        lst += investments

    return pd.DataFrame(lst)


# Execute this code only when running the python file as program, not when importing
# it from e.g. the unit test code.
if __name__ == '__main__':
    df = parse_all_13f_submission_files(root_folder="data/data_MDA/data")
    df.to_excel("data/all_submission_files.xlsx", index=False)
