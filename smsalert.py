#!/usr/bin/env python

"""

Script      :  smsalert.py

Author      :  Jonathan Booth

Description     :  Command line tool for sending sms alert messages via IntelliSoftware SMS HTTPS gateway

"""

from optparse import OptionParser
import requests
import sys

username = '{ removed }'
password = '{ removed }'

code_dictionary = {"ID:": 0,
                   "ERR:LOGIN_INVALID": 1,
                   "ERR:INSUFFICIENT_CREDIT": 2,
                   "ERR:NO_": 3,
                   "ERR:INVALID_NUMBER": 4,
                   "ERR:INVALID_REQUEST": 5,
                   "ERR:GATEWAY_ERROR": 6,
                   "ERR:INTERNAL_ERROR": 7,
                   "INVALID_ARGUMENTS": 8}


def build_http_request(number, message):

    message = message.replace(" ", "+")

    output = 'http://www.intellisoftware.co.uk/smsgateway/sendmsg.aspx?username={0}&password={1}&to={2}&text={3}'\
        .format(username, password, number, message)

    return output

parser = OptionParser()
parser.add_option('-n', '--number', help='takes phone number', dest='number', action='store', type='string')
parser.add_option('-m', '--message', help='takes text message', dest='message', action='store', type='string')
parser.add_option('-b', '--balance', help='get remaining credit balance', dest='balance', action='store_true')

opts, args = parser.parse_args()

if opts.balance:
    balance_url = 'http://www.intellisoftware.co.uk/smsgateway/getbalance.aspx?username={0}&password={1}'\
        .format(username, password)

    r = requests.get(balance_url)
    print(r.text)

elif opts.message is None or opts.number is None:
    parser.print_help()
    sys.exit(code_dictionary["INVALID_ARGUMENTS"])

else:
    r = requests.get(build_http_request(opts.number, opts.message))
    sys.stderr.write(r.text)

    for key, value in code_dictionary.items():
        if key in r.text:
            sys.exit(str(value))
