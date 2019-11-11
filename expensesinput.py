import sys
import logging
import PySimpleGUI as sg
import numpy as np
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
categories = [[sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key)]
                if key is not "other" else [sg.Radio(value, "CAT", key=variables.T1_KEY+variables.CAT+key, default=True)]
                    for key, value in variables.dictOfCategories.items()]

#
# CONTINUATION OF First tab layaout
# ..we use T1_key for labeling our inputs
tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)),
            sg.InputText('Expense Name', key=variables.T1_KEY+variables.EXP)],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText(100, key=variables.T1_KEY + variables.QTY)],
          [sg.Text('Frequency', size=(15, 1)),
            sg.Radio('Monthly', "FREQ", key=variables.T1_KEY+variables.FREQ+"Monthly", default=True),
            sg.Radio('Yearly', "FREQ", key=variables.T1_KEY+variables.FREQ+"Yearly"),
            sg.Radio('Weekly', "FREQ", key=variables.T1_KEY+variables.FREQ+"Weekly", default=True)],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText(str(datetime.date.today()), key=variables.T1_KEY + variables.DATE)],
          [sg.Text('Income/Outcome', size=(15, 1)),
            sg.Checkbox('Expense?', size=(10,1), default=False, key=variables.T1_KEY+variables.INCOME)],
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
                      [sg.Submit('Refresh!', key=variables.T3_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T3_KEY+'_CANCEL_')]]

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

    # Unmodificable values
    inmutableList = [variables.category, variables.date, variables.frequency]
        # 'expenseID', 'Expense?'
    # Writable values
    writableList = [variables.expenseName, variables.qty]

    dictExpenses = variables.jsonData['expensesList']

    header = [[sg.Text('  ')] + [sg.Text(key, size=(15,1)) for key in writableList]
                + [sg.Text(key, size=(15,1)) for key in inmutableList]]   # build header layout

    matrix = header

    for i in range(len(dictExpenses)):
        # current Expense in our dictionary
        expense = dictExpenses[i]
        row = [[sg.Text('  ')] + [sg.InputText(expense[writableList[elemKey]], key=variables.T3_KEY+variables.dictJSON[writableList[elemKey]]+str(expense[variables.expenseID]), size=(15,1)) for elemKey in range(len(writableList))]
                + [sg.Text(value, key=variables.T3_KEY+variables.dictJSON[key]+str(expense[variables.expenseID]), size=(15,1)) for key, value in dictExpenses[i].items() if key in inmutableList]]
        matrix = matrix + row

    tab3_layout = matrix + [[sg.Submit('Update values!',
                                key=variables.T3_KEY+variables.UPDEXPS),
                                    sg.Cancel(key=variables.T3_KEY+'_CANCEL_')]]

    # tab3_layout = header + input_rows
    layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
                sg.Tab('Expense Report', tab2_layout),
                sg.Tab('List of Expenses', tab3_layout)]])]]

    windowNew = sg.Window('Hello {}!! Please, type in all your expenses'.format(variables.username)).Layout(layout)
    window.close()
    #button, values = windowNew.Read()
    window = windowNew


#
#
def updateExpenseData(tab3Data):
    # All expense list!
    for i in range(len(variables.jsonData['expensesList'])):
        # NAME
        variables.jsonData['expensesList'][i][variables.expenseName] = tab3Data[variables.T3_KEY+variables.EXP+str(i)]
        # QTY
        variables.jsonData['expensesList'][i][variables.qty] = tab3Data[variables.T3_KEY+variables.QTY+str(i)]
    expenseJSONFile.writeExpensesList()

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

#
# thirtyDaysExpenseList
# Functioan that is used for our second tab
#
def thirtyDaysExpenseList():
    # listExpenses = [{'ID': 0, 'category': 'loging', 'date': '1-1-1980', 'expenseName': 'Deleteme!', 'frequency': 'Monthly', 'in': False, 'qty': '10000'}]
    listExpenses = variables.jsonData['expensesList']
    result = {}
    logging.debug(listExpenses)
    for i in range(len(listExpenses)):
        # How many times is repeated monthly!
        if (listExpenses[i][variables.category] == "Yearly"):
            frequency = 12
        elif (listExpenses[i][variables.category] == "Weekly"):
            frequency = 0.25
        else:   # motnhly!
            frequency=1

        # Amount is positive or negative
        # qty of our Expense:
        value = int(listExpenses[i][variables.qty])
        logging.debug("ASDASDASDA")
        logging.debug(listExpenses[i][variables.income])
        logging.debug(listExpenses[i][variables.qty])
        # if it is an expense then it is negative!
        if (listExpenses[i][variables.income] is False):
            value = -int(listExpenses[i][variables.qty])

        # Get day of a string datetime!
        day = int(datetime.datetime.strptime(listExpenses[i][variables.date], '%Y-%m-%d').strftime("%d"))
        # {day:qty.freq}
        tuple = {day:(value/frequency)}

        # Create and update dictionary
        # sum the values with same keys
        result[day] = result.get(day, 0) + tuple[day]
    return result

#
#
#
def showMonthlyGraph():
    global tab1_layout, tab2_layout, tab3_layout, layout
    global window
    global header, button, values
    # We calculate expenses in a mont bases
    dailyExpense = thirtyDaysExpenseList()  # result = {'21': 5900.0, '22': -700.0}
    logging.debug(dailyExpense)
    # SumALL POSITIVEs and ALL Expenses in different Varibles
    allIncome=sum(value for value in dailyExpense.values() if value>0)
    allOutcome=sum(value for value in dailyExpense.values() if value<0)

    # Varibles about Income Outcome
    maxABSValue=max(max(dailyExpense.values()), abs(min(dailyExpense.values())))
    # maxIncome = max(dailyExpense.values())
    # minIncome = min(dailyExpense.values())
    maxIncome = maxABSValue
    minIncome = -maxABSValue
    # Canvas canvas_size
    wide = 650  # x
    tall = 400  # y

    # Graph Starting Point
    xZero = int(wide*-0.85)
    xEnd = abs(xZero)
    yZero = int(tall*(-0.8))
    yEnd = abs(yZero)
    tab2_layout = [[sg.T('Your Monthly Expenses graph!')],
            [sg.Graph(canvas_size=(wide, tall),
                                    graph_bottom_left=(-wide, -tall),
                                    graph_top_right=(wide, tall),
                                    background_color='white', key='graph',
                                    tooltip='Your daily account status!')],
            [sg.Text("Total Income: "+ str(allIncome))],[sg.Text("Total Outcome: "+ str(allOutcome))],
            [sg.Submit(key=variables.T2_KEY+'_SUBMIT_'), sg.Cancel(key=variables.T2_KEY+'_CANCEL_')]]

    layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
                sg.Tab('Expense Report', tab2_layout),
                sg.Tab('List of Expenses', tab3_layout)]])]]

    windowNew = sg.Window('Hello {}!! Please, type in all your expenses'.format(variables.username)).Layout(layout).Finalize()
    window.close()
    #button, values = windowNew.Read()
    window = windowNew
    graph = window.Element('graph')

    # Horizontal line with days of a Month!
    graph.DrawLine((xZero, yZero), (xEnd, yZero))
    # One bracket per day of month
    day = 0
    for x in range(xZero, xEnd, 35):
        graph.DrawLine((x,yZero-5), (x,yZero+5))
        graph.DrawText(day, (x,yZero-20), color='green')
        day += 1

    # Vertical line for Expense price
    graph.DrawLine((xZero, yZero + 25), (xZero, yEnd-25))
    graph.DrawLine((xZero-5, 0), (xZero+5, 0))
    graph.DrawText(0, (xZero-20,0), color='green')
    for y in range(yZero, yEnd-25, 50):
        graph.DrawLine((xZero-5, y), (xZero+5, y))
        graph.DrawText(int(y*maxIncome/yEnd), (xZero-30,y), color='green')

    # HOrizontal line for Expense price
    graph.DrawLine((xZero, 0), (xEnd, 0))
    for x in range(xZero, xEnd, 35):
        graph.DrawLine((x,-5), (x,+5))

    # Origin of line!
    pointA_X=xZero
    pointA_Y=0
    currentStatus=0
    for key in range(1,31):
        if key in dailyExpense:
            logging.debug(key)
            logging.debug(dailyExpense[key]*yEnd/maxIncome)
            xValue=(2*xEnd/32) * (key - 15)
            currentStatus=currentStatus+dailyExpense[key]
            logging.debug(xValue)
            logging.debug(currentStatus)
            graph.DrawCircle((xValue, currentStatus*yEnd/maxIncome), 3,
                                fill_color='black',
                                line_color='black')
            if dailyExpense[key]>0:
                graph.DrawText(dailyExpense[key],
                                (xValue+40, currentStatus*yEnd/maxIncome),
                                 color='green')
            else:
                graph.DrawText(dailyExpense[key],
                                (xValue+40, currentStatus*yEnd/maxIncome),
                                color='red')

            graph.DrawLine((pointA_X, pointA_Y),
                                (xValue, currentStatus*yEnd/maxIncome))
            pointA_X = xValue
            pointA_Y = currentStatus*yEnd/maxIncome

    graph.DrawLine((pointA_X, pointA_Y), (xEnd, pointA_Y))

    return dailyExpense


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
    printMatrixExpenses()
    showMonthlyGraph()
    while True:
        button, values = window.Read()
        dictExpenses = expenseJSONFile.readJSON(variables.filepath)['expensesList']
        # Depending on which SUBMIT (tab) is pressed, we act
        # First tab
        if (button == variables.T1_KEY+'_SUBMIT_'):         # FIRST TAB
            #expenseJSONFile.writeExpense(variables.filepath, jsonData, expense):
            # we get ONLY values of this tab1
            res = valuesOfTab(variables.T1_KEY, values)
            # We write OUR new Expense and RETURN all EXPENSE we have
            if expenseJSONFile.writeExpense(res):
                sg.popup("New Expense created succesfuly!")
            else:
                sg.PopupError("Error creating new Expense!")
            printMatrixExpenses()
            showMonthlyGraph()
        elif (button == variables.T2_KEY+'_SUBMIT_'):       # SECOND TAB
            # we get ONLY values of this tab2
            res = valuesOfTab(variables.T2_KEY, values)
            showMonthlyGraph()
        elif (button == variables.T3_KEY+'_SUBMIT_'):       # THIRD TAB
            # we get ONLY values of this tab3
            res = valuesOfTab(variables.T3_KEY, values)
            printMatrixExpenses()
            showMonthlyGraph()
        elif (button == variables.T3_KEY+variables.UPDEXPS):# THIRD TAB
            # logging.debug("Refresh update values")
            # logging.debug(values) # All values!
            res = valuesOfTab(variables.T3_KEY, values)
            # We write OUR new Expense and RETURN all EXPENSE we have
            # expenseJSONFile.writeExpense(res)
#            printMatrixExpenses()
            updateExpenseData(res)
            printMatrixExpenses()
            showMonthlyGraph()
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
