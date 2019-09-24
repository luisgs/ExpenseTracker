import json



def readJSON(filepath):
    # parse file
    contain = json.loads()
    with open(filepath) as json_file:
    data = json.load(json_file)
    print('Name: ' + data['name'])
    for expense in data['expensesList']:
        print('ExpenseName: ' + expense['name'])

def passwordIsRight (file, password):
    return True
