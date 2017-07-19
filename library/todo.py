#!/usr/bin/python

from ansible.module_utils.basic import *
import todoist
import todoist.models


def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
        "content": {"required": True, "type": "str"},
        "project": {"default": "Inbox", "type": "str"},
        "date": {"default": "", "type": "str"},
        "priority": {"default": 1, "type": "int", "choices": [1, 2, 3, 4]},
        "indent": {"default": 1, "type": "int", "choices": [1, 2, 3, 4]},
    }
    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    doist = todoist.TodoistAPI(module.params['api_key'])
    response = sync(module, doist)

    project = get_project(module, doist)

    response = doist.items.add(module.params['content'], project['id'])
    if module.params['date'] is not "":
        doist.items.update(response['id'], date_string=module.params['date'])

    if module.params['priority'] > 1:
        doist.items.update(response['id'], priority=module.params['priority'])

    if module.params['indent'] > 1:
        doist.items.update(response['id'], indent=module.params['indent'])


    if module.check_mode:
        response = "Check mode enabled"
    else:
        response = doist.commit()

    module.exit_json(changed=True, meta=response)


def sync(module, api):
    # type: (AnsibleModule, todoist.TodoistAPI) -> object
    """Syncs with todoist api"""
    if module.check_mode:
        return False
    response = api.sync()
    if 'error' in response:
        module.fail_json(changed=False, msg=response['error'])
    return response


def get_project(module, api):
    # type: (AnsibleModule, todoist.TodoistAPI) -> todoist.models.Project
    """Gets a project from todoist api"""
    if module.check_mode:
        return {'id': 1}
    projects = api.projects.all(lambda x: x['name'] == module.params['project'])
    return projects.pop()


if __name__ == '__main__':
    main()
