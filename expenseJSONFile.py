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

# JSON file that is filed with empty/default values.
jsonEmptyTemplate = {
  'name': variables.username,
  "email":variables.email,
  "password": variables.password,
  "modified":str(datetime.datetime.now()),
  "expensesList": []
  }

#
# Global variables
#
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
        if (variables.EXP in key):  # Expense Name
            formattedExpense[variables.conversionDict[key]] = value
        elif (variables.QTY in key):
            formattedExpense[variables.conversionDict[key]] = int(value)
        elif (variables.FREQ in key):
            if (value):
                formattedExpense[variables.frequency] = variables.conversionDict[key]
            else:
                continue
        elif (variables.CAT in key):
            if (value):
                formattedExpense[variables.category] = variables.conversionDict[key]
            else:
                continue
        else:
            formattedExpense[variables.conversionDict[key]] = value
    return formattedExpense

# writeExpense
# IN: we receive an expense dict and filename filepath
#       we append this expense with the rest.
#       if new we append, if not new -> we update its Expense values
# OUT: Return Expense (True) is all was good. False end other case
def writeExpense(expense):
    # Create new ID for our new expense based on length
    newExpenseID = len(variables.jsonData['expensesList'])
    logging.debug(expense)
    # We sort out our expense input and formatted
    newExpense = formatExpense(expense)
    # Update last time modified field
    variables.jsonData["modified"] = str(datetime.datetime.now())
    # adding it to our NewExpense
    newExpense.update({variables.expenseID:newExpenseID})
    # Appending our expense to our LIST of expenses (if any)
    variables.jsonData['expensesList'].append(newExpense)
    logging.debug(variables.jsonData['expensesList'])
    try:
        with open(variables.filepath, 'w') as json_file:
            json.dump(variables.jsonData, json_file, indent=4, sort_keys=True)
        json_file.close()
        return True
    except:
        logging.error("Writting New Expense into file has failed!")
        return False


#
# CREATE NEW EXFILE
# IN: folder path and file pathname,
# create file Name
def createNewExpenseFile():
    logging.debug(variables.username, variables.email, variables.password, variables.filepath)
    try:
        f= open(variables.filepath,"w+")
        jsonEmptyTemplate['name'] = variables.username
        jsonEmptyTemplate['email'] = variables.email
        jsonEmptyTemplate['password'] = variables.password
        jsonEmptyTemplate['modified'] = str(datetime.datetime.now())
        f.write(json.dumps(jsonEmptyTemplate))
        f.close()
    except:
        logging.error("Creating New File Expense HAS FAILED!")
        return False
    return True
