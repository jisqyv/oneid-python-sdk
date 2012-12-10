import urllib2
import datetime
import json



def _call_OneID():
    pass

def set_oneid_credentials():
    pass

def make_nonce():
    pass

def parse_response():
    pass

def draw_signin_button(callback_url, attrs="personal_info[email] personal_info[first_name] personal_info[last_name]"):
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

def draw_quickfill_button(attrs):
    js = "<span class='oneid_quickfill_ctr'></span>"
    js+= "<script type='text/javascript'>"
    js+= "OneIdExtern.registerApiReadyFunction(function(){"
    js+= "OneId.accuFillButton('.oneid_quickfill_ctr'," + attrs +")"
    js+= "})"
    js+="</script>"
    
    return js

def draw_provision_button(attrs):
    js = "<div class='oneid_create_ctr'></div>"
    js+= "<script type='text/javascript'>"
    js+= "OneIdExtern.registerApiReadyFunction(function(){"
    js+= "OneId.createOneIdButton('.oneid_create_ctr'," + json.dumps(attrs) +")"
    js+= "})"
    js+="</script>"

    return js

def do_redirect():
    pass

def is_success():
    pass