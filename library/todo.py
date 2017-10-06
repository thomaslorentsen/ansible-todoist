#!/usr/bin/python

from ansible.module_utils.basic import *
import todoist
import todoist.models


def main():
    fields = {
        "api_key": {"required": True, "type": "str"},
        "content": {"required": True, "type": "str"},
        "project": {"default": "Inbox", "type": "str"},
        "labels": {"default": [], "type": "list"},
        "date": {"default": "", "type": "str"},
        "priority": {"default": 1, "type": "int", "choices": [1, 2, 3, 4]},
        "indent": {"default": 1, "type": "int", "choices": [1, 2, 3, 4]},
    }
    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    doist = todoist.TodoistAPI(module.params['api_key'])
    response = sync(module, doist)

    project = get_project(module, doist)

    existing_item = item_exists(module.check_mode, doist, module.params['content'], project['id'])
    if existing_item:
        if False == item_changed(existing_item, module.params):
            module.exit_json(changed=False, meta=existing_item['id'])
        else:
            response = existing_item
    else:
        response = doist.items.add(module.params['content'], project['id'])

    if module.params['date'] is not "":
        doist.items.update(response['id'], date_string=module.params['date'])

    if module.params['priority'] > 1:
        doist.items.update(response['id'], priority=module.params['priority'])

    if module.params['indent'] > 1:
        doist.items.update(response['id'], indent=module.params['indent'])

    if type(module.params['labels']) is str:
        module.params['labels'] = [module.params['labels']]

    if module.params['labels'] is not []:
        labels = []
        for label in module.params['labels']:
            label = get_label(module, doist, label)
            labels.append(label['id'])
        doist.items.update(response['id'], labels=labels)

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


def get_label(module, api, label):
    # type: (AnsibleModule, todoist.TodoistAPI, str) -> todoist.models.Project
    """Gets a label from todoist api"""
    if module.check_mode:
        return {'id': 1}
    labels = api.labels.all(lambda x: x['name'] == label)
    return labels.pop()


def item_exists(check_mode, api, content, project):
    # type: (AnsibleModule, todoist.TodoistAPI, str, str) -> todoist.models.Project
    """Gets an item from todoist api"""
    if check_mode:
        return False
    items = api.items.all(lambda x: x['in_history'] == 0 and x['is_deleted'] == 0 and x['is_archived'] == 0 and x['project_id'] == project and x['content'] == content)
    if len(items) == 0:
        return False
    return items.pop()


def item_changed(existing_item, params):
    # type: (todoist.models.Project, AnsibleModule) -> bool
    """Checks if an item has changed"""
    if existing_item['priority'] != params['priority']:
        return True
    return False


if __name__ == '__main__':
    main()
