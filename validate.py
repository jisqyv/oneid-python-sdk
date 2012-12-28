#!/usr/bin/python

from oneid import OneID
import sys
import urllib
import simplejson as json

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>OneID Validation</title>
</head>
<body>
"""

authn = OneID()

f = open('api_key.json','r')
creds = json.loads(f.read())
authn.set_credentials(creds["API_ID"],creds["API_KEY"])
f.close()

line = sys.stdin.readline()

#debugging
f = open('/tmp/validate','w')
f.write(line)
f.close()

resp = authn.validate_response(line)

#Perhaps consider putting suffix in the redirect code?
if authn.success(resp):
    suffix = "?uid="+urllib.quote(resp["uid"])
else:
    suffix = ""

    #TODO: store the returned attributes, if any, in a temp file and put the name of the file
    #in the suffix

redir = authn.redirect('account.py'+suffix,resp)

#debugging
f = open('/tmp/validate2','w')
f.write(json.dumps(redir))
f.close()

print redir
