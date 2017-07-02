#!/usr/bin/python

from ansible.module_utils.basic import *

def main():
	fields = {
		"api_key": {"required": True, "type": "str"},
	}
	module = AnsibleModule(argument_spec=fields)
	response = {"hello": "world"}
	module.exit_json(changed=False, meta=module.params)


if __name__ == '__main__':
    main()
