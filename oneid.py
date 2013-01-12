#!/usr/bin/python

# OneID Python API Library
# Copyright 2013 by OneID

import urllib
import urllib2
import datetime
import base64
import simplejson as json
import pycurl
import StringIO
import os


class OneID:

    def __init__(self, server_flag=""):
        """server_flag should be (for example) "-test" when using a non-production server"""
        self.helper_server = "https://keychain%s.oneid.com" % server_flag
        self.script_header = '<script src="https://api%s.oneid.com/js/includeexternal.js" type="text/javascript"></script>' % server_flag
        self.oneid_form_script = '<script src="https://api%s.oneid.com/form/form.js" type="text/javascript"></script>' % server_flag
        self.creds_file = "api_key"+server_flag+".json"


    def _call_helper(self, method, data={}):
        """Call the OneID Helper Service. """
        url = "%s/%s" % (self.helper_server, method)
        base64creds = base64.encodestring('%s:%s' % (self.api_id, self.api_key)).replace('\n', '')

        #NOTE: SSL certificates are not verified by urllib2
        #urllib2 version of request - doesn't verify SSL certificates so not recommended!
        #        request = urllib2.Request(url)
        #        request.add_header("Authorization", "Basic %s" % base64creds)
        #        response = urllib2.urlopen(request, json.dumps(data))
        #        return json.loads(response.readline())

        response = StringIO.StringIO()
        request = pycurl.Curl()
        request.setopt(pycurl.URL, url)
        request.setopt(pycurl.WRITEFUNCTION, response.write)
        request.setopt(pycurl.USERPWD, '%s:%s' % (self.api_id,self.api_key))

        if data != "":
            request.setopt(pycurl.POST, 1)
            request.setopt(pycurl.POSTFIELDS, json.dumps(data))

        request.perform()

        return json.loads(response.getvalue())

    def set_credentials(self, api_id="", api_key=""):
        """Set the credentials used for access to the OneID Helper Service"""
        if api_id != "":
            self.api_id = api_id
            self.api_key = api_key
        else:
            f = open(self.creds_file,'r')
            creds = json.loads(f.read())
            f.close()
            self.api_id = creds["API_ID"]
            self.api_key = creds["API_KEY"]

    def validate(self,line):
        """Validate the data received by a callback"""
        resp = json.loads(line)
        valdata = dict([("nonces",resp["nonces"]),("uid",resp["uid"])])
        if "attr_claim_tokens" in resp:
            valdata["attr_claim_tokens"] = resp["attr_claim_tokens"]
        valresp = self._call_helper("validate",valdata)
        if (not self.success(valresp)):
            valresp["failed"] = "failed"
            return valresp

        for x in valresp:
            resp[x] = valresp[x]

        return resp

    def draw_signin_button(self, callback_url, attrs=""):
        """Create a OneID Sign In button on the web page"""
        params = json.dumps({
                "challenge" : {"attr" : attrs, "callback" : callback_url}
            }
        )
        js = "<span class='oneid_login_ctr'></span>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.loginButton('.oneid_login_ctr'," + params +")"
        js+= "})"
        js+="</script>"

        return js

    def draw_quickfill_button(self, attrs):
        """Create a OneID QuickFill button on the web page"""
        js = "<span class='oneid_quickfill_ctr'></span>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.accuFillButton('.oneid_quickfill_ctr'," + attrs +")"
        js+= "})"
        js+="</script>"

        return js

    def draw_provision_button(self, attrs):
        """Create a provision button on the web page"""
        js = "<div class='oneid_create_ctr'></div>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.createOneIdButton('.oneid_create_ctr'," + json.dumps(attrs) +")"
        js+= "})"
        js+="</script>"

        return js

    def redirect(self, page, response):
        """Create the JSON string that instructs the AJAX code to redirect the browser to the account"""
        if self.success(response):
            #Note that the "nonce" here is actually the b64 encoded JSON containing the nonce. But it's unique and good
            #enough to uniquely identify the session for passing attributes.
            suffix = "?uid="+urllib.quote(response["uid"])+"&nonce="+urllib.quote(self._getnonce(response))
        else:
            suffix = ""

        return json.dumps({"error":response['error'],"errorcode":str(response['errorcode']),\
                           "url":page + suffix})
        
    def success(self, response):
        """Check errorcode in a response"""
        return response["errorcode"] == 0

    def save_attributes(self, response):
        """Save attributes in a temporary file for account page"""
        noncefile = "/tmp/"+self._getnonce(response)
        f = open(noncefile, "w")
        f.write(json.dumps(response["attr"]))
        f.close()

    def get_attributes(self, nonce):
        """Retrieve attributes saved by validation page"""
        noncefile = "/tmp/"+nonce
        f = open(noncefile, "r")
        data = f.read()
        f.close()
        os.remove(noncefile)
        return json.loads(data)

    def _getnonce(self, response):
        """Extract base64-encoded nonce from JWT in a response"""
        return response["nonces"]["repo"]["nonce"].split('.')[1]

    
        
