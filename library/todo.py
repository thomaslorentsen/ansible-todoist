#!/usr/bin/python

from ansible.module_utils.basic import *
import todoist
import todoist.models


def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
        "content": {"required": True, "type": "str"},
        "project": {"default": "Inbox", "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    doist = todoist.TodoistAPI(module.params['api_key'])
    response = sync(module, doist)

    project = get_project(module, doist)

    response = doist.items.add(module.params['content'], project['id'])
    doist.items.update(response['id'], date_string="today")

    response = {"response": response['id']}

    if module.check_mode:
        response = "Check mode enabled"
    else:
        response = doist.commit()

    module.exit_json(changed=True, meta=response)


def sync(module, api):
    # type: (AnsibleModule, todoist.TodoistAPI) -> object
    if module.check_mode:
        return False
    response = api.sync()
    if 'error' in response:
        module.fail_json(changed=False, msg=response['error'])
    return response


def get_project(module, api):
    # type: (AnsibleModule, todoist.TodoistAPI) -> todoist.models.Project
    if module.check_mode:
        return {'id': 1}
    projects = api.projects.all(lambda x: x['name'] == module.params['project'])
    return projects.pop()


if __name__ == '__main__':
    main()
