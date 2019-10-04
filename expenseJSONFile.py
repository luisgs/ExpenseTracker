import json, sys
import hashlib
import datetime
import logging
import variables

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#
# Library for reading our JSON file
# We include all necessary functions and operation for that in here
#

#
# Global variables
#
conversionDict = {
    "TAB_1_CAT_Loging": "loging",
    "TAB_1_CAT_Transport": "Transport",
    "TAB_1_CAT_Entertainment": "Entertainment",
    "TAB_1_CAT_Salary": "salary",
    "TAB_1_DATE_": "date",
    "TAB_1_EXPENSENAME_": "Expense Name",
    "TAB_1_FREQ_Monthly": "Monthly",
    "TAB_1_FREQ_Yearly": "Yearly",
    "TAB_1_EXPENSE_": "Expense?",
    "TAB_1_QTY_": "qty",
}

# readJSON
# OUT: Open file (all granted) and return all file data
def readJSON(filepath):
    # parse file
    with open(filepath) as json_file:
        variables.jsonData = json.load(json_file)
        #logging.debug('Name: ' + data['name'])
        #for expense in data['expensesList']:
        #    logging.debug('ExpenseName: ' + expense['name'])
        #logging.debug(len(data['expensesList']))
    json_file.close()
    return variables.jsonData

#
# userAndPassCorrect
# return True if both password and user are mathcing with our file
def userAndPassCorrect(email, password, JSONemail, JSONpass):
    return ((email == JSONemail) and
        ((hashlib.md5(password.encode('utf-8')).hexdigest())==JSONpass))
    # Function that hash our password
    # hashlib.md5(password.encode('utf-8')).hexdigest()
#
# formatExpense
# formatting a new expense dict into our JSON key values dict
#
def formatExpense(newExpense):
    formattedExpense={}
    for key,value in newExpense.items():
        if ("_CAT_" in key):
            if (value):
                formattedExpense["category"] = variables.conversionDict[key]
            else:
                continue
        elif ("_FREQ_" in key):
            if (value):
                formattedExpense["frequency"] = variables.conversionDict[key]
            else:
                continue
        elif ("_QTY_" in key):
            formattedExpense[variables.conversionDict[key]] = int(value)
        else:
            formattedExpense[variables.conversionDict[key]] = value
    return formattedExpense

# writeExpense
# IN: we receive an expense dict and filename filepath
#       we append this new (already formatted) expense with the rest
# OUT: Return Expense (True) is all was good. False end other case
def writeExpense(filename, expense):
    # Create new ID for our new expense based on length
    expenseID = len(variables.jsonData['expensesList'])
    # We sort out our expense input and formatted
    newExpense = formatExpense(expense)
    # Update last time modified field
    variables.jsonData["modified"] = str(datetime.datetime.now())
    # adding it to our NewExpense
    newExpense.update({'expenseID':expenseID})
    # Appending our new expense to our LIST of expenses (if any)
    variables.jsonData['expensesList'].append(newExpense)
    logging.debug(variables.jsonData['expensesList'])
    try:
        with open(filename, 'w') as json_file:
            json.dump(variables.jsonData, json_file, indent=4, sort_keys=True)
        json_file.close()
        return True
    except:
        logging.error("Writting New Expense into file has failed!")
        return False
