#!/usr/bin/env python3

import things
from datetime import datetime

def get_todo_keyword(task, suffix=' '):
    if task['type'] == 'project':
        return ''

    status = task['status']
    if status == 'incomplete':
        return 'TODO' + suffix
    elif status == 'completed':
        return 'DONE' + suffix
    elif status == 'canceled':
        return 'CANCELED' + suffix
    else:
        return ''

def get_checkbox(item):
    if item['status'] == 'incomplete':
        return '[ ]'
    else:
        return '[X]'

def date_to_org_date(date):
    parsed = datetime.strptime(date, '%Y-%m-%d')
    return parsed.strftime('<%Y-%m-%d %a>')

def print_task(task, level):
    print('{0} {1}{2}'.format(level, get_todo_keyword(task), task['title']))

    dates = []
    if 'start_date' in task and task['start_date'] != None:
        dates.append('SCHEDULED: {0}'.format(date_to_org_date(task['start_date'])))
    if 'deadline' in task and task['deadline'] != None:
        dates.append('DEADLINE: {0}'.format(date_to_org_date(task['deadline'])))

    if len(dates) > 0:
        print(' '.join(dates))

    if 'notes' in task:
        notes = task['notes'].strip()
        if len(notes) > 0:
            print(notes)

    if 'checklist' in task and len(task['checklist']) > 0:
        for item in task['checklist']:
            print('- {0} {1}'.format(get_checkbox(item), item['title']))

def print_tasks(tasks, level):
    for task in tasks:
        print_task(task, level)

tasks = things.inbox(include_items=True)
if len(tasks) > 0:
    print('* Inbox')
    print_tasks(tasks, '**')

tasks = things.todos(project=False, heading=False, area=False, start_date=True, include_items=True)
if len(tasks) > 0:
    print('* No Project')
    print_tasks(tasks, '**')

areas = things.areas()
for area in areas:
    print('* {0}'.format(area['title']))

    tasks = things.todos(area=area['uuid'], include_items=True)
    print_tasks(tasks, '**')

    projects = things.projects(area=area['uuid'])
    for project in projects:
        print_task(project, '**')

        tasks = things.todos(project=project['uuid'], include_items=True)
        print_tasks(tasks, '***')

        headings = things.tasks(type='heading', project=project['uuid'])
        for heading in headings:
            print('*** {0}'.format(heading['title']))

            tasks = things.todos(heading=heading['uuid'], include_items=True)
            print_tasks(tasks, '****')


