import sys
import logging
import PySimpleGUI as sg
import datetime
import expenseJSONFile

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

tab1_layout =  [[sg.T('This is inside tab 1')]]

# Unmodificable values
inmutableList = ['expenseID', 'frequency', 'category', 'date', 'Expense?']
# Writable values
writableList = ['Expense Name', 'qty']

dictExpenses = [{'Expense Name': 'Expense Name', 'qty': 100,
                    'frequency': 'Monthly', 'category': 'loging',
                    'date': '2019-09-26', 'Expense?': True, 'expenseID': 2},
                {'Expense Name': 'CARACOLA!', 'qty': 999,
                                    'frequency': 'Monthly', 'category': 'loging',
                                    'date': '2019-09-26', 'Expense?': True, 'expenseID': 3}]

tab3_layout =  [[sg.T('Empty HEader')], [sg.Submit(key='_REFRESH_')]]
# input_rows = [[sg.Input(size=(15,1), pad=(0,0)) for col in range(4)] for row in range(10)]

layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 3', tab3_layout)]])],
              [sg.Button('Read')]]
window = sg.Window('Hello hola!! Please, type in all your expenses').Layout(layout)

def printMatrixExpenses():
    global dictExpenses
    global header, button, values
    global tab1_layout, tab3_layout, window
    global writableList, inmutableList

    header = [[sg.Text('  ')] + [sg.Text(key, size=(15,1)) for key, value in dictExpenses[0].items() if key in writableList]
                + [sg.Text(key, size=(15,1)) for key, value in dictExpenses[0].items() if key in inmutableList]]   # build header layout

    tab3_layout = header
    #for i in range(len(dictExpenses)):
    #    row = [[sg.Text('  ')] + [sg.InputText(value, key=key+"_"+str(i), size=(14,1)) for key, value in dictExpenses[i].items()]]
    #    tab3_layout = tab3_layout + row

    for i in range(len(dictExpenses)):
        row = [[sg.Text('  ')] + [sg.InputText(value, key=key+"_"+str(i), size=(15,1)) for key, value in dictExpenses[i].items() if key in writableList]
        + [sg.Text(value, key=key+"_"+str(i), size=(15,1)) for key, value in dictExpenses[i].items() if key in inmutableList]]
        tab3_layout = tab3_layout + row

    tab3_layout = tab3_layout + [[sg.Submit(key='_REFRESH_')]]
    # tab3_layout = header + input_rows
    layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout),
                sg.Tab('Tab 3', tab3_layout)]])],
                  [sg.Button('Update Values!')]]
    windowNew = sg.Window('NEW WINDOWS!!').Layout(layout)
    window.close()
    button, values = windowNew.Read()
    window=windowNew

button, values = window.Read()
while True:
    print(button)
    print(values)
    if button is '_REFRESH_':
        printMatrixExpenses()
    else:
        button, values = window.Read()
# window = sg.Window('Hello hola!! Please, type in all your expenses').Layout(layout)
