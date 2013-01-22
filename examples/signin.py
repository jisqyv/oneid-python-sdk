#!/usr/bin/python

from oneid import OneID

authn = OneID()

print """Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
  <title>OneID Sign In</title>
  <meta name="viewport" content="width=device-width"/>
</head>
<body>
<div align="center">
"""

print authn.script_header

print "Click on this button to sign in:"

print authn.draw_signin_button("validate.py","personal_info[first_name] personal_info[last_name]")

print "</div></body></html>"
