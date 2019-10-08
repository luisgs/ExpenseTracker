import sys, logging
import os.path
import PySimpleGUI as sg
import expensesinput, variables

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Layout at first
layout = [
          [sg.Text('Please enter your information:')],
          [sg.Text('Name', size=(15, 1)),
            sg.InputText(variables.username, key=variables.NAME)],
          [sg.Text('Email', size=(15, 1)),
            sg.InputText(variables.email, key=variables.EMAIL)],
          [sg.Text('Password', size=(15, 1)),
            sg.InputText(variables.clearPassword, password_char='*', key=variables.PASSWORD)],
          [sg.Text('Expense File location:', size=(15, 1)),
            sg.In(variables.defaultFilePath, key=variables.FILEPATH), sg.FileBrowse()],
          [sg.OK(tooltip='Click to submit this window'), sg.Cancel()]
         ]

window = sg.Window('Welcome to Expense Tracker').Layout(layout)

while True:
    button, values = window.Read()
    if (button=='OK'):
        if not (os.path.exists(values[variables.FILEPATH])):
            sg.popup("File DOES NOT EXIST!")
        else:
            if not (os.access(values[variables.FILEPATH], os.R_OK)):
                sg.popup("File CANNOT be READ!")
            elif not (os.access(values[variables.FILEPATH], os.W_OK)):
                sg.popup("File CANNOT be WRITTEN!")
            else:

                sg.popup("File exists and is readable!")
                window.close()
                username = values[variables.NAME]
                email = values[variables.EMAIL]
                filepath = values[variables.FILEPATH]
                expensesinput.main()
    elif (button == 'Cancel'):
        break

window.close()
logging.debug(button, values['_NAME_'], values['_EMAIL_'], values['_FILEPATH_'])
exit()
