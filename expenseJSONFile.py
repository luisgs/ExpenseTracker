import json, sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#
# Library for reading our JSON file
#

#
# Global variables
#
conversionDict = {
    "TAB_1_CAT0_Loging": "loging",
    "TAB_1_CAT1_Transport": "Transport",
    "TAB_1_CAT2_Entertainment": "Entertainment",
    "TAB_1_CAT3_Salary": "salary",
    "TAB_1_DATE_": "date",
    "TAB_1_EXPENSENAME_": "Expense Name",
    "TAB_1_FREQ0_Monthly": "Monthly",
    "TAB_1_FREQ1_Yearly": "Yearly",
    "TAB_1_IN_": "income",
    "TAB_1_OUT_": "outcome",
    "TAB_1_QTY_": "qty",
}

# readJSON
# OUT: Open file (all granted) and return all file data
def readJSON(filepath):
    # parse file
    with open(filepath) as json_file:
        data = json.load(json_file)
        #logging.debug('Name: ' + data['name'])
        #for expense in data['expensesList']:
        #    logging.debug('ExpenseName: ' + expense['name'])
        #logging.debug(len(data['expensesList']))
    return data

#
# formatExpense
# formatting a new expense dict into our JSON key values dict
#
def formatExpense(newExpense):
    global conversionDict
    formattedExpense={}
    for key,value in newExpense.items():
        formattedExpense[conversionDict[key]] = value
    return formattedExpense

# writeExpense
# IN: we receive an expense dict and filename filepath
#       we append this new (already formatted) expense with the rest
# OUT: True is all was good. False end other case
def writeExpense(filename, expense):
    # We read it all again
    data = readJSON(filename)
    # Create new ID for our new expense based on length
    expenseID = len(data['expensesList'])
    # We sort out our expense input and formatted
    newExpense = formatExpense(expense)
    # adding it to our NewExpense
    newExpense.update({'expenseID':expenseID})
    # Appending our new expense to our LIST of expenses (if any)
    data['expensesList'].append(newExpense)
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, sort_keys=True)
        return True
    except:
        logging.error("Writting New Expense into file has failed!")
        return False

def passwordIsRight (file, password):
    return True
