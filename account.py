#!/usr/bin/python

import cgi
from oneid import OneID

# Debugging
import cgitb
cgitb.enable()

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>Welcome</title>
</head>
<body>
"""


form = cgi.FieldStorage()
if "uid" not in form:
   print "<H1>Error</H1>"
   print "UID not found"
else:
   authn = OneID()
   attr = authn.get_attributes(form["nonce"].value)
   
   print "<p>Welcome, UID=",form["uid"].value,"<br />"
   print repr(attr)
   print "</p></body></html>"

