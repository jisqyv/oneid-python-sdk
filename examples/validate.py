#!/usr/bin/python

from oneid import OneID
import sys
import urllib
try:
    import json
except ImportError:
    import simplejson as json

print """Content-Type: text/html
"""

authn = OneID()

authn.set_credentials()

line = sys.stdin.readline()

resp = authn.validate(line)

sessionid = authn.save_session(resp)

print authn.redirect('account.py', resp, sessionid)

