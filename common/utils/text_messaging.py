from unidecode import unidecode

import requests
from requests.auth import HTTPBasicAuth


def send_message(username, password, payload):
    """
    Method to send a single message to one or more recipients. It needs the Infobip credentials and a payload
    according to Infobip's standards: https://dev.infobip.com/docs/fully-featured-textual-message.
    From value (from, required) could be 'INFOsms' to send messages that can't receive a response.
    Recipient (to, required) can be a string for single value, or list for multiple values.
    Message (text, required) will be normalized for compatibility with network providers
    Returns the decoded Infobip response
    """
    
    #Normalize message string for compatibility
    payload['messages']['text'] = unidecode(payload['messages']['text'])

    url = "https://api.infobip.com/sms/1/text/advanced"
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username.strip(), password.strip()))

    return response.json()