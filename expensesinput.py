import sys
import PySimpleGUI as sg

# Very basic window.  Return values as a list
username = "Default"
filename = "/tmp/deleteme.txt"

categories = [[sg.Radio('Loging', "CAT", default=True), sg.Radio('Transport', "CAT"), sg.Radio('Entertainemt', "CAT"), sg.Radio('Salary', "CAT")]]
#
# First tab layaout
#

tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)), sg.InputText('Expense Name')],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText('$?')],
          [sg.Text('Frequency', size=(15, 1)), sg.Radio('Monthly', "FREQ", default=True), sg.Radio('Yearly', "FREQ")],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText('../../..')],
          [sg.Text('Income/Outcome', size=(15, 1)), sg.Radio('Outcome', "INOUT", default=True), sg.Radio('Income', "INOUT")],
          [sg.Submit(key='submitTab1'), sg.Cancel(key='Cancel')]
         ]

#
# Second tab layaout
#
tab2_layout = [[sg.T('This is inside tab 2')], [sg.In(key='in')],
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


    window = sg.Window('Hello {}!! Please, type in all your expenses'.format(username)).Layout(layout)

    while True:
        button, values = window.Read()
        print(button)
        if button == "Submit":
            sg.popup("Submit layaout 1?")
        elif (button == 'Cancel') or (button == 'None'):
            break

    window.close()
    exit()

if __name__=="__main__":
    # We send them all arg minus first one. app name.
    main(sys.argv[1:])
