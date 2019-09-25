import json, sys
import hashlib
import datetime
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
    "TAB_1_EXPENSE_": "Expense?",
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
# userAndPassCorrect
# return True if both password and user are mathcing with our file
def userAndPassCorrect(email, password, JSONemail, JSONpass):
    logging.debug(email)
    logging.debug(password)
    logging.debug(JSONemail)
    logging.debug(hashlib.md5(password.encode('utf-8')).hexdigest())
    logging.debug(JSONpass)
    return ((email == JSONemail) and
        ((hashlib.md5(password.encode('utf-8')).hexdigest())==JSONpass))
    # Function that hash our password
    # hashlib.md5(password.encode('utf-8')).hexdigest()
#
# formatExpense
# formatting a new expense dict into our JSON key values dict
#
def formatExpense(newExpense):
    global conversionDict
    formattedExpense={}
    for key,value in newExpense.items():
        if ("_CAT" in key):
            if (value):
                formattedExpense["category"] = conversionDict[key]
            else:
                continue
        elif ("_FREQ" in key):
            if (value):
                formattedExpense["frequency"] = conversionDict[key]
            else:
                continue
        elif ("_QTY" in key):
            formattedExpense[conversionDict[key]] = int(value)
        else:
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
    # Update last time modified field
    data["modified"] = str(datetime.datetime.now())
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
