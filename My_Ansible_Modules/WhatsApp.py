#!/usr/bin/python
"""Send text to WhatsApp API"""

# Copyright: (c) 2024, Harry Zijlmans <zijlmansh@hmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type



DOCUMENTATION = r"""
---
module: WhatsApp

short_description: Send messages to WhatsApp

version_added: "1.0.0"

description: Use Free API to Send Whatsapp Messages

            See https://www.callmebot.com/blog/free-api-whatsapp-messages/

            Setup:

            You need to get the apikey form the bot before using the API:

            1. Add the phone number +34 611 021 695 into your Phone Contacts. (Name it it as you wish)

                Send this message "I allow callmebot to send me messages" to the new Contact created (using WhatsApp of course)
                Wait until you receive the message "API Activated for your phone number. Your APIKEY is 123123" from the bot.
                Note: If you don't receive the ApiKey in 2 minutes, please try again after 24hs.
                The WhatsApp message from the bot will contain the apikey needed to send messages using the API.

            You can send text messages using the API after receiving the confirmation.

options:
    apikey:
        description: Api key .
        required: true
        type: str
    phone:
        description: Your phone number used in your WhatsApp contacts (see above)
        required: true
        type: str 

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Harry Zijlmans
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.WhatsApp:
    phone: 311234567 
    apikey: 87654321 
    text: A TEST MESSAGE
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
ok: [localhost] => {
    "out": {
        "WhatsApp_text": "<p>Message to: +311234567<p>Text to send: A TEST MESSAGE <p><b>Message queued.</b> You will receive it in a few seconds.",
        "changed": false,
        "failed": false
    }
}
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def send_message(phone, apikey, text):
    """Send text to whatsapp bot"""

    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={text}&apikey={apikey}"
    r = requests.get(url)

    # check if it was successful
    if r.status_code == 200:
        return r.text

    raise Exception(f"{r.text}")


def run_module():
    """start of ansible helper"""
 
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        phone=dict(type="str", required=True),
        apikey=dict(type="str", required=True),
        text=dict(type="str", required=True),
    )

    # seed the result dict in the object
    result = dict(changed=False, WhatsApp_text="")

    # instantiation
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Also in chech_mode return WhatsApp_text
    # changed always False
    result["changed"] = False
    result["WhatsApp_text"] = module.params["text"]

    # What do we return in check_mode ?
    if module.check_mode:
        module.exit_json(**result)

    # call api
    try:
        result["WhatsApp_text"] = send_message(
            module.params["phone"], module.params["apikey"], module.params["text"]
        )
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    # Normal exit
    module.exit_json(**result)


def main():
    """Entry point"""
    run_module()


if __name__ == "__main__":
    main()
