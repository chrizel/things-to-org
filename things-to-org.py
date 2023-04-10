#!/usr/bin/env python3

import things
import pandoc

from datetime import datetime

def get_todo_keyword(task, suffix=' '):
    # if task['type'] == 'project':
    #     return ''

    status = task['status']
    if status == 'incomplete':
        return 'TODO' + suffix
    elif status == 'completed':
        return 'DONE' + suffix
    elif status == 'canceled':
        return 'CANCELLED' + suffix
    else:
        return ''

def get_checkbox(item):
    if item['status'] == 'incomplete':
        return '[ ]'
    else:
        return '[X]'

def date_to_org_date(date):
    parsed = datetime.strptime(date, '%Y-%m-%d')
    return parsed.strftime('%Y-%m-%d %a')

def active_date(date):
    return '<' + date_to_org_date(date) + '>'

def inactive_date(date):
    return '[' + date_to_org_date(date) + ']'

def print_task(task, level):
    print('{0} {1}{2}'.format(level, get_todo_keyword(task), task['title']))

    dates = []
    if 'start_date' in task and task['start_date'] != None:
        dates.append('SCHEDULED: {0}'.format(active_date(task['start_date'])))
    if 'deadline' in task and task['deadline'] != None:
        dates.append('DEADLINE: {0}'.format(active_date(task['deadline'])))

    if len(dates) > 0:
        print(' '.join(dates))

    if 'stop_date' in task and task['stop_date'] != None:
        print('- Changed to "{0}": {1}'.format(get_todo_keyword(task), inactive_date(task['stop_date'])))

    if 'notes' in task:
        notes = task['notes']
        if not notes is None:
            if len(notes) > 0:
                doc = pandoc.read(notes, format='markdown', options=['--shift-heading-level-by={0}'.format(len(level))])
                print(pandoc.write(doc, format='org'))

    if 'checklist' in task and len(task['checklist']) > 0:
        for item in task['checklist']:
            print('- {0} {1}'.format(get_checkbox(item), item['title']))

def print_tasks(tasks, level):
    for task in tasks:
        print_task(task, level)

def print_projects(projects, level):
    for project in projects:
        print_task(project, level)

        #  Any todo in a project, not under a heading
        tasks = things.todos(project=project['uuid'], status=None, include_items=True)
        print_tasks(tasks, level + "*")

        headings = things.tasks(type='heading', project=project['uuid'], status=None)
        for heading in headings:
            print('{1} {0}'.format(heading['title'], level + "*"))

            # Any todo under the heading
            tasks = things.todos(heading=heading['uuid'], status=None, include_items=True)
            print_tasks(tasks, level + '**')

# Any todo in Inbox, including completed
tasks = things.inbox(status=None, include_items=True)
if len(tasks) > 0:
    print('* Inbox')
    print_tasks(tasks, '**')

# Any project not in an area
projects = things.projects(area=False, status=None)
if len(projects) > 0:
    print('* Projects outside area')
    print_projects(projects, "**")

# Any todo not in area and project
tasks = things.todos(area=False, project=False, status=None, include_items=True)
if len(tasks) > 0:
    print('* Todos outside area and project')
    print_tasks(tasks, '**')

areas = things.areas()
for area in areas:
    print('* {0}'.format(area['title']))

    # Any todo 
    tasks = things.todos(area=area['uuid'], status=None, include_items=True)
    print_tasks(tasks, '**')

    projects = things.projects(area=area['uuid'], status=None)
    print_projects(projects)
