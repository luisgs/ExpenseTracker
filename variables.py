

#
# Default variables
#
username = "name"
email = "email@address.com"
clearPassword = "1234"
password = "81dc9bdb52d04dc20036dbd8313ed055"
defaultFilePath = 'C:\\Users\\gomezlui\\Documents\\Personal\\PythonPersonalProjects\\ExpenseTracker\\json\\example.json'
# JSON file that contains our records!
filepath = defaultFilePath

# All JSON file is read and stored in here in python format (jsonload)
jsonData = None

# Tabs preffix keys to differenciate submnittted values.
T1_KEY = 'TAB_1'
T2_KEY = 'TAB_2'
T3_KEY = 'TAB_3'
# Additoinal keys for our categories
NAME = "_NAME_"
EMAIL = '_EMAIL_'
PASSWORD = '_PASSWORD_'
FILEPATH = '_FILEPATH_'
CAT = "_CAT_"
FREQ = "_FREQ_"
DATE = "_DATE_"
QTY = "_QTY_"
EXP = "_EXPENSENAME_"
SUBMIT = "_SUBMIT_"
UPDEXPS = "_UPDEXPS_"
ID = "_ID_"
INCOME = "_EXPENSE_"

#
# JSON file definition
#
expenseID = "ID"
expenseName = "expenseName"
qty = "qty"
frequency = "frequency"
category = "category"
date = "date"
income = "income"
dictJSON = {expenseName:EXP,
            expenseID:ID,
            expenseName:EXP,
            qty:QTY,
            frequency:FREQ,
            category:CAT,
            date:DATE,
            income:INCOME}
expense = [expenseID, expenseName, qty, frequency, category, date, income]
#
#
dictOfCategories = {'lodging': "Lodging",
                    'transport': "Transport",
                    'entertainemt': "Entertainemt",
                    'salary': "Salary",
                    'savings': "Savings",
                    'other': "Others"}
#
# Global variables
#
conversionDict = { T1_KEY+CAT+key:value for key, value in dictOfCategories.items()}
conversionDictPart1={T1_KEY+DATE: date,
    T1_KEY + EXP: expenseName,
    T1_KEY + FREQ + "Monthly": "Monthly",
    T1_KEY + FREQ + "Yearly": "Yearly",
    T1_KEY + "_EXPENSE_": income,
    T1_KEY+QTY: qty
}
conversionDict.update(conversionDictPart1)
