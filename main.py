import sys, logging
import os.path
import PySimpleGUI as sg
import hashlib
import expensesinput, variables, expenseJSONFile

# Logging as output logging messages.
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

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
        # File does NOT exist, we create it new
        if not (os.path.exists(values[variables.FILEPATH])):
            sg.popup_error("File HAS NOTE BEEN FOUND! Do you want to create new one?")
            variables.username = values[variables.NAME]
            variables.email = values[variables.EMAIL]
            variables.password = hashlib.md5(values[variables.PASSWORD].encode('utf-8')).hexdigest()
            #sg.popup_error("File DOES NOT EXIST!")
            layout_newFile = [
                [sg.Text('Creating a new EXPENSE FILE with this info:')],
                [sg.Text('Name: {}'.format(values[variables.NAME]))],
                [sg.Text('Default path folder and filename:'),
                    sg.InputText(values[variables.FILEPATH], key=variables.FILEPATH)],
                [sg.OK(key='_CREATENEWFILE_'), sg.Cancel()]
                ]
            newwindow = sg.Window('Creating new Expense Report File').Layout(layout_newFile)
            button, values = newwindow.Read()
            variables.filepath = values[variables.FILEPATH]
            newwindow.close()
            #We create a new file with informatoin has been granted.
            if not expenseJSONFile.createNewExpenseFile():  # if CREATE fails:
                sg.popup_error("ERROR CREATING EXPENSE FILE!")
            else:   # if all is okay:
                window.close()
                expensesinput.main()
        elif not (os.access(values[variables.FILEPATH], os.R_OK)):
            sg.popup_error("File CANNOT be READ!")
        elif not (os.access(values[variables.FILEPATH], os.W_OK)):
            sg.popup_error("File CANNOT be WRITTEN!")
        else:
            sg.popup("File exists and is readable!")
            variables.username = values[variables.NAME]
            variables.email = values[variables.EMAIL]
            variables.password = hashlib.md5(values[variables.PASSWORD].encode('utf-8')).hexdigest()
            variables.filepath = values[variables.FILEPATH]
            window.close()
            expensesinput.main()
    elif (button == 'Cancel'):
        break

window.close()
logging.debug("MAIN:", button, values['_NAME_'], values['_EMAIL_'], values['_FILEPATH_'])
exit()
