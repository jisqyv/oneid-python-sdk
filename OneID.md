## About

The OneID module implements a single class, OneID, which implements an
easy-to-use interface to the OneID identity service.

Implementing OneID sign in is a three-part process.  You will normally
create a page on your server corresponding to each part: 

* Reference Page (where OneID button(s) will be displayed)
* Validation Page (receives a callback from the user with the
authentication information and attempst to validate it)
* Account Page (receives a redirect from the Validation Page following
validation)

### `class OneID([server_flag])`

Creating an instance of the OneID class takes a single optional
parameter, the name of the OneID environment to be used, if
other than the default. Alternate OneID environments are used
for internal development, testing, and beta test purposes.
Contact OneID Support at support@oneid.com if you have a need to
use one of these environments.

The OneID class provides the following methods:
    
#### `set_credentials(api_id, api_key)`

Sets the credentials required by the OneID Helper Service.  The
Helper Service is used by the `validate()` method to check
The signatures provided in the authentication as well as
signatures on any requested attributes that are signed by
OneID. To use the Helper Service, you will need to obtain an API
Key from https://keychain.oneid.com/register and provide them via
this method prior to calling `validate()`. By downloading
an API Key you agree to the OneID Developer Agreement (URL
here). This method is normally only required when implementing the
Validation Page.

#### `validate(line)`

Calls the OneID Helper Service to validate the signatures on a
response received from the user. This method takes one parameter,
line, which is the string-format JSON response from the user's
agent (provided as POST data to the Validate page). `validate()` is
called by the Validation Page.

If validation is unsuccessful, `validate()` returns a dictionary
containing the following values: "failed": "failed" "errorcode":
numeric error code "error": textual error message

If successful, `validate()` returns a dictionary with the following values:
(fill in the format here)

#### `draw_signin_button(callback_url[, attrs])`

Generates and prints JavaScript that instantiates a OneID Sign In
button on the page. This method takes two parameters, the callback
URL (address of the Validation Page) and an optional
space-delimited list of optional attributes to be provided as part
of the authentication.  If no attr parameter is specified, no
attributes are supplied. This method is used on the Reference Page.
The JavaScript this method generates can alternatively be directly
embedded in an HTML web page.

#### `draw_quickfill_button(callback_url, attrs)`

Generates and prints JavaScript that instantiates a OneID QuickFill
button on the page.  This method takes two parameter, the callback
URL (address of the Validation Page) and a space-delimited list of
attributes to be obtained to fill in fields on the page.  Quickfill
buttons require additional JavaScript defining mapping between
OneID attribute names and form field names, as defined at **TBD**.
This method is used on the Reference Page.

#### `draw_provision_button(callback_url, attrs)`

Generates and prints JavaScript that instantiates a OneID QuickFill
button on the page.  This method takes two parameters, the callback
URL (address of the Validation Page) and a string containing a
space delimited list of user attributes **TBD**. This method is
used on the Reference Page.

#### `redirect(page, response, sessionid)`

Creates a JSON string, to be output by the Validation Page, to
cause the browser to redirect to the Account Page following
validation. It takes three parameters, the URL of the Account Page
to be redirected to, the response from the validation server, and a
session ID.  The session ID is a parameter to the redirect URL that
points to the session context for the redirected session.

#### `save_session(response)`

Saves the UID and attribute information from a validation response
in a temporary file for later retrieval by the Account Page. It
returns a string token referring to the session ID which can be
referenced in the redirect URL (see `redirect()` method).
    
#### `get_session(sessionid)`

Uses the sessionid to retrieve stored UID and attribute information
for the session. This method is typically used on the Account Page.
It returns a dictionary containing the UID ("uid") and attributes
("attr"), the latter of which is a dictionary of attributes
returned with the response.
