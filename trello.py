import requests
import sys

auth_params = {
    'key': "__Ваш ключ от api.trello",
    'token': "__Ваш токен от api.trello",
}

base_url = "https://api.trello.com/1/{}"
board_id = "__Ваш идентификатор доски__"


def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_counter = 0
        task_id = None
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            task_counter += 1

        print(column['name'] + ' (' + str(task_counter) + ')')
        if not task_data:
            print('\t' + 'Заданий нет')
        for task in task_data:
            task_id = str(task['id'])[-4:]
            print('\t' + task['name'] + ' | ID задачи: ' + str(task_id))

def create_task(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break
            
            
def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break
        elif column_name != column['name']:
            create_col(column_name)
            create_task(name, column_name)
            break
# python trello.py create "___Название задачи____" "___Название колонки____"


def get_task(task_id):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id_req = None
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            if task_id == str(task['id'])[-4:]:
                task_id_req = str(task['id'])

    task = requests.get(base_url.format('cards') + '/' + str(task_id_req), params=auth_params).json()
    print('\t' + task['name'])
# python trello.py get_task "__ID (4 символа)__"


def move_task(task_id, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id_req = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task_id == str(task['id'])[-4:]:
                task_id_req = str(task['id'])
                break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id_req + '/idList',
                         data={'value': column['id'], **auth_params})

# python trello.py move_task __task_id(4 symbols)__ "__Название колонки__"


def del_task(task_id):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id_req = None
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            if task_id == str(task['id'])[-4:]:
                task_id_req = str(task['id'])

    requests.delete(base_url.format('cards') + '/' + str(task_id_req), params=auth_params).json()
# python trello.py del_task __task_id (4 symb)__

def create_col(name):
    lists_url = base_url.format('boards') + '/' + board_id + '/lists'
    requests.post(lists_url, data={'name': name, **auth_params})

# python trello.py create_col "___Название колонки____"


def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
# python trello.py move "___Название задачи____" "___Название колонки____"


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_col':
        create_col(sys.argv[2])
    elif sys.argv[1] == 'get_task':
        get_task(sys.argv[2])
    elif sys.argv[1] == 'move_task':
        move_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'del_task':
        del_task(sys.argv[2])
