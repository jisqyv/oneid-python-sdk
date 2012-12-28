import urllib2
import datetime
import base64
import simplejson as json


class OneID:
    helper_server = ""
    oneid_script = ""
    oneid_form_script = ""

    def __init__(self, server_flag=""):
        self.helper_server = "https://keychain%s.oneid.com" % server_flag
        self.script_header = '<script src="https://api%s.oneid.com/js/includeexternal.js" type="text/javascript"></script>' % server_flag
        self.oneid_form_script = '<script src="https://api%s.oneid.com/form/form.js" type="text/javascript"></script>' % server_flag


    def _call_helper(self, method,data={}):
        url = "%s/%s" % (self.helper_server, method)

        #TODO: SSL certificate not verified by urllib2

        request = urllib2.Request(url)

        base64string = base64.encodestring('%s:%s' % (self.api_id, self.api_key)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        response = urllib2.urlopen(request, json.dumps(data))
        return json.loads(response.readline())

    def set_credentials(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key

    def validate_response(self,line):
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
        js = "<span class='oneid_quickfill_ctr'></span>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.accuFillButton('.oneid_quickfill_ctr'," + attrs +")"
        js+= "})"
        js+="</script>"

        print js

    def draw_provision_button(self, attrs):
        js = "<div class='oneid_create_ctr'></div>"
        js+= "<script type='text/javascript'>"
        js+= "OneIdExtern.registerApiReadyFunction(function(){"
        js+= "OneId.createOneIdButton('.oneid_create_ctr'," + json.dumps(attrs) +")"
        js+= "})"
        js+="</script>"

        print js

    def redirect(self, page, response):
        return '{"error":"'+response['error']+'","errorcode":"'+str(response['errorcode'])+'\
        ","url":"'+page+'","response":"'+json.dumps(response)+'"}'

    def success(self, response):
        return response["errorcode"] == 0

