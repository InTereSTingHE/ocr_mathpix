import os
import base64
import requests
import json
from PIL import ImageGrab
#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py 
#

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID', 'ID'), # ID for your ID
    'app_key': env.get('APP_KEY', 'KEY'), # KEY for your KEY
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'

#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)


def mathpix_clipboard(): # get clipboard
    im = ImageGrab.grabclipboard()
    im.save('equa.png','PNG')
    r = latex({
        'src': image_uri("equa.png"),
        'formats': ['mathml'],# or 'text' for latex...see API doc, change with print
        'data_options': {
            'include_mathml': True
            }
    })

    mlout = '<math xmlns="http://www.w3.org/1998/Math/MathML">' + r['mathml'][6:] # copy to microsoft word
    print(r['mathml']) # change with formats
    print(mlout)

if __name__ == '__main__':
    mathpix_clipboard()
