import sys
import logging
import PySimpleGUI as sg
import datetime
import expenseJSONFile, variables

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#
# Default global variables
#
dictExpenses = {}

#
# First tab layaout
#
# we generate RADIO button sectoin for all our possible categories
#categories = [[sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key)]
#                                        for key, value in variables.dictOfCategories.items()
#                                        if key is not "other" else [sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key, Default=True)]]
categories = [[sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key)]
                if key is not "other" else [sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key, default=True)]
                    for key, value in variables.dictOfCategories.items()]

#
# CONTINUATION OF First tab layaout
# ..we use T1_key for labeling our inputs
tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)),
            sg.InputText('Expense Name', key=variables.T1_KEY+'_EXPENSENAME_')],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText(100, key=variables.T1_KEY + variables.QTY)],
          [sg.Text('Frequency', size=(15, 1)),
            sg.Radio('Monthly', "FREQ", key=variables.T1_KEY+variables.FREQ+"Monthly", default=True),
            sg.Radio('Yearly', "FREQ", key=variables.T1_KEY+variables.FREQ+"Yearly")],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText(str(datetime.date.today()), key=variables.T1_KEY + variables.DATE)],
          [sg.Text('Income/Outcome', size=(15, 1)),
            sg.Checkbox('Expense?', size=(10,1), default=True, key=variables.T1_KEY+"_EXPENSE_")],
          [sg.Submit(key=variables.T1_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T1_KEY+'_CANCEL_')]
         ]

#
# Second tab layaout
# WE HAVE TO USE KEY TAB_2
#
tab2_layout = [[sg.T('This is inside tab 2')], [sg.In(key=variables.T2_KEY+'_IN_')],
          [sg.Submit(key=variables.T2_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T2_KEY+'_CANCEL_')]]

#
# Third tab layaout
#
tab3_layout = [[sg.T('Please press refresh to update your values.')],
                      [sg.Submit('Refresh', key=variables.T3_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T3_KEY+'_CANCEL_')]]

# Unmodificable values
inmutableList = [variables.frequency, variables.category, variables.date]
    # 'expenseID', 'Expense?'
# Writable values
writableList = [variables.expenseName, variables.qty]

#
# ALL TABS' LAYOUTs TOGETHER
#
layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
            sg.Tab('Expense Report', tab2_layout),
            sg.Tab('List of Expenses', tab3_layout)]])]]

window = None

#
# printMatrixExpenses
# We print tab3 with all our file expenses.
def printMatrixExpenses():
    global dictExpenses
    global tab1_layout, tab2_layout, tab3_layout, layout
    global window
    global header, button, values
    global writableList, inmutableList

    dictExpenses = expenseJSONFile.readJSON(variables.filepath)['expensesList']

    header = [[sg.Text('  ')] + [sg.Text(key, size=(15,1)) for key in writableList]
                + [sg.Text(key, size=(15,1)) for key in inmutableList]]   # build header layout

    matrix = header

    for i in range(len(dictExpenses)):
        # current Expense in our dictionary
        expense = dictExpenses[i]
        row = [[sg.Text('  ')] + [sg.InputText(expense[writableList[elemKey]], key=writableList[elemKey]+"_"+str(i), size=(15,1)) for elemKey in range(len(writableList))]
                + [sg.Text(value, key=key+"_"+str(i), size=(15,1)) for key, value in dictExpenses[i].items() if key in inmutableList]]
        matrix = matrix + row

    tab3_layout = matrix + [[sg.Submit('Refresh', key=variables.T3_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T3_KEY+'_CANCEL_')]]

    # tab3_layout = header + input_rows
    layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
                sg.Tab('Expense Report', tab2_layout),
                sg.Tab('List of Expenses', tab3_layout)]])]]

    windowNew = sg.Window('ExpenseTracker has been refreshed!').Layout(layout)
    window.close()
    #button, values = windowNew.Read()
    window = windowNew

#
# valuesOfTab
# IN: We receive a tab preffix (string) and a dict of values (entries)
# OUT: We return ONLY a dict with key?values for this particular tab
def valuesOfTab(tab, allValues):
    #logging.debug(allValues)
    #logging.debug(tab)
    res = {key:val for key, val in allValues.items()
                            if key.startswith(tab)}
    return res

def main():
    # We bring global variables
    global dictExpenses
    global layout, window
    # call external function to read our file
    variables.jsonData = expenseJSONFile.readJSON(variables.filepath)
    # email and password is correct?
    if not (expenseJSONFile.userAndPassCorrect(variables.email, variables.clearPassword,
                                                    variables.jsonData["email"], variables.jsonData["password"])):
        sg.popup("USER AND/OR DO NOT MATCH!!!")
        exit()
    else:
        sg.popup("USER AND PASSWORD are MATCHING!")

    # send our window.layout out and wait for values
    window = sg.Window('Hello {}!! Please, type in all your expenses'.format(variables.username)).Layout(layout)

    while True:
        button, values = window.Read()
        dictExpenses = expenseJSONFile.readJSON(variables.filepath)['expensesList']
        # Depending on which SUBMIT (tab) is pressed, we act
        # First tab
        if (button == variables.T1_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 1")
            #expenseJSONFile.writeExpense(variables.filepath, jsonData, expense):
            # we get ONLY values of this tab1
            res = valuesOfTab(variables.T1_KEY, values)
            # We write OUR new Expense and RETURN all EXPENSE we have
            expenseJSONFile.writeExpense(res)
        elif (button == variables.T2_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 2")
            # we get ONLY values of this tab2
            res = valuesOfTab(variables.T2_KEY, values)
        elif (button == variables.T3_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 3")
            # we get ONLY values of this tab3
            res = valuesOfTab(variables.T3_KEY, values)
            printMatrixExpenses()
        elif ('_CANCEL_' in button ) or (button is None):
            # Cancel button is pressed
            logging.debug("Cancel button has been pressed!")
            break
        else:
            logging.error("Button has not been captured right")
            break
    window.close()
    exit()

if __name__=="__main__":
    # Call out our MAIN function
    main()
