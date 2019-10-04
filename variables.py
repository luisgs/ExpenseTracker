

#
# Default variables
#
username = "name"
email = "email@address.com"
clearPassword = "1234"
password = "81dc9bdb52d04dc20036dbd8313ed055"
defaultFilePath = 'C:\\Users\\gomezlui\\Documents\\Personal\\PythonPersonalProjects\\ExpenseTracker\\json\\example.json'
filepath = defaultFilePath

# All JSON file is read and stored in here in python format (jsonload)
jsonData = None

#
# JSON file definition
#
expenseID = "ID"
expenseName = "name"
qty = "qty"
frequency = "frequency"
category = "category"
date = "date"
income = "income"

# Tabs preffix keys to differenciate submnittted values.
T1_KEY = 'TAB_1'
T2_KEY = 'TAB_2'
T3_KEY = 'TAB_3'

CAT = "_CAT_"
FREQ = "_FREQ_"
DATE = "_DATE_"

#
# JSON file definition
#
expenseID = "ID"
expenseName = "name"
qty = "qty"
frequency = "frequency"
category = "category"
date = "date"
income = "income"
expense = [expenseID, expenseName, qty, frequency, category, date, income]

#
#
dictOfCategories = {'lodging': "Lodging",
                    'transport': "Transport",
                    'entertainemt': "Entertainemt",
                    'salary': "Salary",
                    'other': "Others"}
#
# Global variables
#
conversionDict = { T1_KEY+CAT+key:value for key, value in dictOfCategories.items()}
conversionDictPart1={T1_KEY+DATE: "date",
    T1_KEY+"_EXPENSENAME_": "Expense Name",
    T1_KEY+"_FREQ_Monthly": "Monthly",
    T1_KEY+"_FREQ_Yearly": "Yearly",
    T1_KEY+"_EXPENSE_": "Expense?",
    T1_KEY+"_QTY_": "qty"
}
conversionDict.update(conversionDictPart1)
