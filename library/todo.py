#!/usr/bin/python

from ansible.module_utils.basic import *
import todoist


def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
        "content": {"required": True, "type": "str"},
        "project": {"default": "Inbox", "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields)

    doist = todoist.TodoistAPI(module.params['api_key'])
    response = doist.sync(resource_types=['projects'])
    if 'error' in response:
        module.fail_json(changed=False, msg=response['error'])

    projects = doist.projects.all(lambda x: x['name'] == module.params['project'])
    project = projects.pop()

    response = doist.items.add(module.params['content'], project['id'])

    response = {"response": response['id']}

    response = doist.commit()

    module.exit_json(changed=True, meta=response)


if __name__ == '__main__':
    main()
