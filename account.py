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
if "sessionid" not in form:
   print "<H1>Error</H1>"
   print "Authentication failure - sessionid not found"
else:
   authn = OneID()
   sess = authn.get_session(form["sessionid"].value)
   
   print "<p>Welcome, UID=",sess["uid"],"<br />"
   print repr(sess["attr"])
   print "</p></body></html>"

