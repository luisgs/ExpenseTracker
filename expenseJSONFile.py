import json, sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#
# Library for reading our JSON file
#

# readJSON
# Open file (all granted) and return all file data
def readJSON(filepath):
    # parse file
    with open(filepath) as json_file:
        data = json.load(json_file)
        logging.debug('Name: ' + data['name'])
        for expense in data['expensesList']:
            logging.debug('ExpenseName: ' + expense['name'])
        logging.debug(len(data['expensesList']))
    return data

def writeExpense(filename, data, expense):
    expenseID = len(listExpenses)
    # convert dict to json
    newExpense = json.dumps(expense)
    newExpense.append(expenseID)
    data['expensesList'].append(newExpense)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    return True

def passwordIsRight (file, password):
    return True
