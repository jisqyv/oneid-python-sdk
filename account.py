import cgi

# Debugging
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
if "uid" not inform:
   print "<H1>Error</H1>"
   print "UID not found"
   return
print "<p>Welcome, UID=",form["uid"].value

