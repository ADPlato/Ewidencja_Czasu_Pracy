import secure
import requests

LOGLIST_URL = "/logList.xml"
REMOVE_LOGS = "/msg.php?removeLog=1"

def do_xml_from_web():
    response = requests.get(secure.INPUT_READER_URL+LOGLIST_URL, auth=(secure.READER_LOGIN, secure.READER_PASSWORD))
    with open('Wyjscia.xml', 'wb') as file:
        file.write(response.content)
    response = requests.get(secure.OUTPUT_READER_URL+LOGLIST_URL, auth=(secure.READER_LOGIN, secure.READER_PASSWORD))
    with open('Wejscia.xml', 'wb') as file:
        file.write(response.content)

def clear_reader(reader_url):
    response = requests.get(reader_url+REMOVE_LOGS, auth=(secure.READER_LOGIN, secure.READER_PASSWORD))
    if response == 1:
        return "Clean complite"
    else:
        return "Clean NOT complite"
        #OR Exception
