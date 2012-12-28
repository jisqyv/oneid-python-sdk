#!/usr/bin/python

from oneid import OneID

authn = OneID()

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>OneID Sign In</title>
</head>
<body>
"""

print authn.script_header

print "Click on this button to sign in:"

authn.draw_signin_button("validate.py")

print "</body></html>"
