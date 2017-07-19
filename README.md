[![Build Status](https://travis-ci.org/thomaslorentsen/ansible-todoist.svg?branch=master)](https://travis-ci.org/thomaslorentsen/ansible-todoist)
[![Ansible Role](https://img.shields.io/ansible/role/19334.svg)](https://galaxy.ansible.com/thomaslorentsen/todoist/)

Todoist
=========

This is an Ansible Module that integrates into the [Todoist](https://developer.todoist.com) api.
With this module you can automate adding todo items to your projects.

Requirements
------------

The Todoist Python module needs to be installed
```bash
pip install todoist-python
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
        - todo:
            api_key: your_todoist_api_key_here
            content: Added to Inbox
        
        - todo:
            api_key: your_todoist_api_key_here
            content: Added to Personal project
            project: Personal
          
        - todo:
            api_key: your_todoist_api_key_here
            content: Added to Inbox to be completed today
            date: today
          
        - todo:
            api_key: your_todoist_api_key_here
            content: A high priority task
            priority: 4
          
        - todo:
            api_key: your_todoist_api_key_here
            content: An indented task
            indent: 2

You will need to add this module to your modules path to run:
```bash
ansible-playbook --module-path /etc/ansible/roles/thomaslorentsen.todoist/library
```

License
-------

BSD

Author Information
------------------

- https://github.com/thomaslorentsen
