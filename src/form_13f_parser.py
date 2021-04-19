import xml.etree.ElementTree as ET

def parse_submission_file(file_path):
    """
    Opens a file that was originally downloaded from the Edgar site and parse it.
    We assume that the file is a 13F-HR form
    :param file_name:
    :return: a dictionary with all relevant attributes from the document
    """

    # Read all file content in memory
    with open(file_path) as f:
        text = f.read()

    # Cut the text into blocks (lines) that start right after the <XML> tag
    result = text.split('<XML>')
    # Remove spaces and newline character right before and after each line
    result = [line.strip() for line in result]
    # Keep only the lines that contain and xml document
    result = [line for line in result if line.startswith('<?xml version="1.0"')]
    # Cut of the unneeded text right after the xml document.
    result = [line.split("</XML>")[0].strip() for line in result]

    # Combine the multiple xml documents into one:
    # <form>
    #    <edgarSubmission>...</edgarSubmission>
    #    <informationTable>...</informationTable>
    # </form>
    form_node = ET.fromstring("<form></form>")
    for line in result:
        form_node.insert(0, ET.fromstring(line))

    return form_node
