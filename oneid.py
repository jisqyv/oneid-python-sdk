import urllib2
import datetime
import json


class OneID:
    oneid_server = ""
    oneid_script = ""
    oneid_form_script = ""

    def __init__(self, server_flag):
        self.oneid_server = "https://keychain%s.oneid.com" % server_flag
        self.oneid_script = '<script src="https://api%s.oneid.com/js/includeexternal.js" type="text/javascript"></script>' % server_flag
        self.oneid_form_script = '<script src="https://api%s.oneid.com/form/form.js" type="text/javascript"></script>' % server_flag


    def _call_OneID(self, method,data={}):
        url = "%s/%s" % (oneid_server, method)

        request = urllib2.Request(url)
        api_id,api_key=""

        base64string = base64.encodestring('%s:%s' % (api_id, api_key)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        response = urllib2.urlopen(request, json.dumps(data))
        return json.loads(response)

    def set_oneid_credentials(self):
        pass

    def make_nonce(self):
        pass

    def parse_response(self):
        pass

    def draw_signin_button(self, callback_url, attrs="personal_info[email] personal_info[first_name] personal_info[last_name]"):
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
        js = "<span class='oneid_quickfill_ctr'></span>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.accuFillButton('.oneid_quickfill_ctr'," + attrs +")"
        js+= "})"
        js+="</script>"

        return js

    def draw_provision_button(self, attrs):
        js = "<div class='oneid_create_ctr'></div>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.createOneIdButton('.oneid_create_ctr'," + json.dumps(attrs) +")"
        js+= "})"
        js+="</script>"

        return js

    def do_redirect(self):
        pass

    def is_success(self):
        pass