#!/usr/bin/python

from ansible.module_utils.basic import *
import todoist


def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
        "content": {"required": True, "type": "str"},
        "project": {"default": "Inbox", "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    doist = todoist.TodoistAPI(module.params['api_key'])
    response = doist.sync(resource_types=['projects'])
    if 'error' in response:
        module.fail_json(changed=False, msg=response['error'])

    projects = doist.projects.all(lambda x: x['name'] == module.params['project'])
    project = projects.pop()

    response = doist.items.add(module.params['content'], project['id'])
    doist.items.update(response['id'], date_string="today")

    response = {"response": response['id']}

    if module.check_mode:
        response = "Check mode enabled"
    else:
        response = doist.commit()

    module.exit_json(changed=True, meta=response)


if __name__ == '__main__':
    main()
