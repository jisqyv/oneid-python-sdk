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


class OneID:

    def __init__(self, server_flag=""):
        """server_flag should be (for example) "-test" when using a non-production server"""
        self.helper_server = "https://keychain%s.oneid.com" % server_flag
        self.script_header = '<script src="https://api%s.oneid.com/js/includeexternal.js" type="text/javascript"></script>' % server_flag
        self.oneid_form_script = '<script src="https://api%s.oneid.com/form/form.js" type="text/javascript"></script>' % server_flag


    def _call_helper(self, method, data={}):
        """Call the OneID Helper Service. """
        url = "%s/%s" % (self.helper_server, method)
        base64creds = base64.encodestring('%s:%s' % (self.api_id, self.api_key)).replace('\n', '')

        #TODO: SSL certificate not verified by urllib2
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

    def set_credentials(self, api_id, api_key):
        """Set the credentials used for access to the OneID Helper Service"""
        self.api_id = api_id
        self.api_key = api_key

    def validate_response(self,line):
        """Validate the data received by a callback"""
        resp = json.loads(line)
        valdata = dict([("nonces",resp["nonces"]),("attr_claim_tokens",resp["attr_claim_tokens"]),("uid",resp["uid"])])
        validate = self._call_helper("validate",valdata)
        if (not self.success(validate)):
            validate["failed"] = "failed"
            return validate

        for x in validate:
            resp[x] = validate[x]

        return resp

    def draw_signin_button(self, callback_url, attrs="personal_info[email] personal_info[first_name] personal_info[last_name]"):
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

        print js

    def draw_quickfill_button(self, attrs):
        """Create a OneID QuickFill button on the web page"""
        js = "<span class='oneid_quickfill_ctr'></span>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.accuFillButton('.oneid_quickfill_ctr'," + attrs +")"
        js+= "})"
        js+="</script>"

        print js

    def draw_provision_button(self, attrs):
        """Create a provision button on the web page"""
        js = "<div class='oneid_create_ctr'></div>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.createOneIdButton('.oneid_create_ctr'," + json.dumps(attrs) +")"
        js+= "})"
        js+="</script>"

        print js

    def redirect(self, page, response):
        """Create the JSON string that instructs the AJAX code to redirect the browser to the account"""
        if self.success(response):
            suffix = "?uid="+urllib.quote(response["uid"])+"&nonce="+urllib.quote(response["nonce"])
        else:
            suffix = ""

        return json.dumps({"error":response['error'],"errorcode":str(response['errorcode']),\
                           "url":page + suffix})
        
    def success(self, response):
        return response["errorcode"] == 0

