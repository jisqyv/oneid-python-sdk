#!/usr/bin/python

from oneid import OneID
import sys
import urllib
import simplejson as json

print """Content-Type: text/html
"""

authn = OneID()

authn.set_credentials()

line = sys.stdin.readline()

resp = authn.validate(line)

f=open("/tmp/response","w")
f.write(repr(resp))
f.close()

authn.save_attributes(resp)

print authn.redirect('account.py',resp)

