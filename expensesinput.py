import sys
import PySimpleGUI as sg
import expenseJSONFile

# Very basic window.  Return values as a list
username = "Default"
filename = "/tmp/deleteme.txt"

categories = [[sg.Radio('Loging', "CAT", default=True, key="cat0"), sg.Radio('Transport', "CAT", key="cat1"), sg.Radio('Entertainemt', "CAT", key="cat2"), sg.Radio('Salary', "CAT", key="cat3")]]
#
# First tab layaout
#

tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)), sg.InputText('Expense Name', key='expenseName')],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText('$?', key='qty')],
          [sg.Text('Frequency', size=(15, 1)), sg.Radio('Monthly', "FREQ", key="freq0", default=True), sg.Radio('Yearly', "FREQ", key="freq1")],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText('../../..', key='date')],
          [sg.Text('Income/Outcome', size=(15, 1)), sg.Radio('Outcome', "INOUT", default=True, key='in'), sg.Radio('Income', "INOUT", key='out')],
          [sg.Submit(key='submitTab1'), sg.Cancel(key='Cancel')]
         ]

#
# Second tab layaout
#
tab2_layout = [[sg.T('This is inside tab 2')], [sg.In(key='in1')],
          [sg.Submit(key='submitTab2'), sg.Cancel(key='Cancel')]]


#
# Third tab layaout
#
tab3_layout = [[sg.T('This is inside tab 3')],
                      [sg.Submit(key='submitTab3'), sg.Cancel(key='Cancel')]]

layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout), sg.Tab('Expense Report', tab2_layout), sg.Tab('List of Expenses', tab3_layout)]])]]

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
