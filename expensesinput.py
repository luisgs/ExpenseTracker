import sys
import PySimpleGUI as sg
import expenseJSONFile

#
# Default global variables
#
username = "Default"
filename = "/tmp/deleteme.txt"
T1_KEY = 'TAB_1'
T2_KEY = 'TAB_2'
T3_KEY = 'TAB_3'

#
# First tab layaout
#
categories = [[sg.Radio('Loging', "CAT", default=True, key=T1_KEY+"_CAT0_"),
                sg.Radio('Transport', "CAT", key=T1_KEY+"_CAT1_"),
                sg.Radio('Entertainemt', "CAT", key=T1_KEY+"_CAT2_"),
                sg.Radio('Salary', "CAT", key=T1_KEY+"_CAT3_")]]
#
# CONTINUATION OF First tab layaout
# ..we use T1_key for labeling our inputs
tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)),
            sg.InputText('Expense Name', key=T1_KEY+'_EXPENSENAME_')],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText('$?', key=T1_KEY+'_QTY_')],
          [sg.Text('Frequency', size=(15, 1)),
            sg.Radio('Monthly', "FREQ", key=T1_KEY+"_FREQ0_", default=True),
            sg.Radio('Yearly', "FREQ", key=T1_KEY+"_FREQ1_")],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText('../../..', key=T1_KEY+'_DATE_')],
          [sg.Text('Income/Outcome', size=(15, 1)),
            sg.Radio('Outcome', "INOUT", default=True, key=T1_KEY+'_IN_'),
            sg.Radio('Income', "INOUT", key=T1_KEY+'_OUT_')],
          [sg.Submit(key=T1_KEY+'_SUBMIT_'), sg.Cancel(key=T1_KEY+'_CANCEL_')]
         ]

#
# Second tab layaout
# WE HAVE TO USE KEY TAB_2
tab2_layout = [[sg.T('This is inside tab 2')], [sg.In(key=T2_KEY+'_IN_')],
          [sg.Submit(key=T2_KEY+'_SUBMIT_'), sg.Cancel(key=T2_KEY+'_CANCEL_')]]


#
# Third tab layaout
#
tab3_layout = [[sg.T('This is inside tab 3')],
                      [sg.Submit(key=T3_KEY+'_SUBMIT_'), sg.Cancel(key=T3_KEY+'_CANCEL_')]]

layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
            sg.Tab('Expense Report', tab2_layout),
            sg.Tab('List of Expenses', tab3_layout)]])]]

def main(argv):
    # print(argv)
    global username
    global filename
    username = argv[0]
    filename = argv[3]

    data=expenseJSONFile.readJSON(filename)

    window = sg.Window('Hello {}!! Please, type in all your expenses'.format(username)).Layout(layout)

    while True:
        button, values = window.Read()
        print(button)
        if button == "submitTab1":
            sg.popup("Submit layaout 1")
            newExpense = {}
            print(values)
            #expenseJSONFile.writeExpense(filename, data, expense):
        elif button == "submitTab2":
            sg.popup("Submit layaout 2")
        elif button == "submitTab3":
            sg.popup("Submit layaout 3")
        else:
            break
    window.close()
    exit()

if __name__=="__main__":
    # We send them all arg minus first one. app name.
    main(sys.argv[1:])
