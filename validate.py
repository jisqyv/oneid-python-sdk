#!/usr/bin/python

from oneid import OneID
import sys
import urllib
import simplejson as json

print """Content-Type: text/html
"""

authn = OneID()

f = open('api_key.json','r')
creds = json.loads(f.read())
authn.set_credentials(creds["API_ID"],creds["API_KEY"])
f.close()

line = sys.stdin.readline()

resp = authn.validate_response(line)

    #TODO: store the returned attributes, if any, in a temp file and put the name of the file
    #in the suffix

print authn.redirect('account.py',resp)

