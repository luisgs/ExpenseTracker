import sys
import logging
import PySimpleGUI as sg
import datetime
import expenseJSONFile

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#
# Default global variables
#
username = "Default"
email = "email@email.com"
password = "81dc9bdb52d04dc20036dbd8313ed055"
filename = "/tmp/deleteme.txt"

dictExpenses = {}

# Tabs preffix keys to differenciate submnittted values.
T1_KEY = 'TAB_1'
T2_KEY = 'TAB_2'
T3_KEY = 'TAB_3'

CAT = "_CAT_"
FREQ = "_FREQ_"

#
# First tab layaout
#
categories = [[sg.Radio('Loging', "CAT", default=True, key=T1_KEY+CAT+"Loging"),
                sg.Radio('Transport', "CAT", key=T1_KEY+CAT+"Transport"),
                sg.Radio('Entertainemt', "CAT", key=T1_KEY+CAT+"Entertainment"),
                sg.Radio('Salary', "CAT", key=T1_KEY+CAT+"Salary")]]

#
# CONTINUATION OF First tab layaout
# ..we use T1_key for labeling our inputs
tab1_layout =  [
          [sg.Text('Expense Name', size=(15, 1)),
            sg.InputText('Expense Name', key=T1_KEY+'_EXPENSENAME_')],
          [sg.Text('Quantity', size=(15, 1)), sg.InputText(100, key=T1_KEY+'_QTY_')],
          [sg.Text('Frequency', size=(15, 1)),
            sg.Radio('Monthly', "FREQ", key=T1_KEY+FREQ+"Monthly", default=True),
            sg.Radio('Yearly', "FREQ", key=T1_KEY+FREQ+"Yearly")],
          [sg.Frame("Categories", [[sg.Column(categories)]])],
          [sg.Text('Date', size=(15, 1)), sg.InputText(str(datetime.date.today()), key=T1_KEY+'_DATE_')],
          [sg.Text('Income/Outcome', size=(15, 1)),
            sg.Checkbox('Expense?', size=(10,1), default=True, key=T1_KEY+"_EXPENSE_")],
          [sg.Submit(key=T1_KEY+'_SUBMIT_'), sg.Cancel(key=T1_KEY+'_CANCEL_')]
         ]

#
# Second tab layaout
# WE HAVE TO USE KEY TAB_2
#
tab2_layout = [[sg.T('This is inside tab 2')], [sg.In(key=T2_KEY+'_IN_')],
          [sg.Submit(key=T2_KEY+'_SUBMIT_'), sg.Cancel(key=T2_KEY+'_CANCEL_')]]

#
# Third tab layaout
#
headings = ['ID', 'Name', 'Quantity','Frequency', 'Category', 'Date', 'Expense?']  # the text of the headings
header =  [[sg.Text('  ')] + [sg.Text(h, size=(14,1)) for h in headings]]  # build header layout
input_rows = [[sg.Input(size=(15,1), pad=(0,0)) for col in range(4)] for row in range(10)]
tab3_layout = header + input_rows

tab3_layout = [[sg.T('This is inside tab 3')],
                      [sg.Submit(key=T3_KEY+'_SUBMIT_'), sg.Cancel(key=T3_KEY+'_CANCEL_')]]



#
# ALL TABS' LAYOUTs TOGETHER
#
layout = [[sg.TabGroup([[sg.Tab('New Expense', tab1_layout),
            sg.Tab('Expense Report', tab2_layout),
            sg.Tab('List of Expenses', tab3_layout)]])]]

#
# valuesOfTab
# IN: We receive a tab preffix (string) and a dict of values (entries)
# OUT: We return ONLY a dict with key?values for this particular tab
def valuesOfTab(tab, allValues):
    logging.debug(allValues)
    logging.debug(tab)
    res = {key:val for key, val in allValues.items()
            if key.startswith(tab)}
    logging.debug("HERE ARE VALUES FOR "+tab)
    logging.debug(res)
    return res

def main(argv):
    # We bring global variables
    global username
    global email
    global password
    global filename
    global dictExpenses
    username = argv['_NAME_']
    email = argv['_EMAIL_']
    password = argv['_PASSWORD_']
    filename = argv['_FILEPATH_']

    # call external function to read our file
    data = expenseJSONFile.readJSON(filename)

    # email and password is correct?
    if not (expenseJSONFile.userAndPassCorrect(email, password, data["email"],data["password"])):
        sg.popup("USER AND/OR DO NOT MATCH!!!")
        exit()
    else:
        sg.popup("USER AND PASSWORD are MATCHING!")

    # send our window.layout out and wait for values
    window = sg.Window('Hello {}!! Please, type in all your expenses'.format(username)).Layout(layout)

    while True:
        button, values = window.Read()
        # logging.debug(button)
        # logging.debug(values)

        # Depending on which SUBMIT (tab) is pressed, we act
        # First tab
        if (button == T1_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 1")
            #expenseJSONFile.writeExpense(filename, data, expense):
            # we get ONLY values of this tab1
            res = valuesOfTab(T1_KEY, values)
            newExpense = expenseJSONFile.writeExpense(filename, res)
        elif (button == T2_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 2")
            # we get ONLY values of this tab2
            res = valuesOfTab(T2_KEY, values)
        elif (button == T3_KEY+'_SUBMIT_'):
            sg.popup("Submit layout 3")
            # we get ONLY values of this tab3
            res = valuesOfTab(T3_KEY, values)
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
    # We send them all arg minus first one. app name.
    main(sys.argv[1:])
