#!/usr/bin/python

from ansible.module_utils.basic import *
from todoist import TodoistAPI

def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields)

    doist = TodoistAPI(module.params['api_key'])

    response = {"key": module.params['api_key']}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
