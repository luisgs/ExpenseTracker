import os.path
import PySimpleGUI as sg
import expensesinput

# Very basic window.  Return values as a list

layout = [
          [sg.Text('Please enter your information:')],
          [sg.Text('Name', size=(15, 1)),
            sg.InputText('name', key='_NAME_')],
          [sg.Text('Email', size=(15, 1)),
            sg.InputText('email@address.com', key='_EMAIL_')],
          [sg.Text('Password', size=(15, 1)),
            sg.InputText('1234', password_char='*', key='_PASSWORD_')],
          [sg.Text('Expense File location:', size=(15, 1)),
            sg.InputText('C:\\Users\\gomezlui\\Documents\\Personal\\PythonPersonalProjects\\ExpenseTracker\\json\\example.json', key='_FILEPATH_')],
          [sg.OK(tooltip='Click to submit this window'), sg.Cancel()]
         ]

window = sg.Window('Welcome to Expense Tracker').Layout(layout)

while True:
    button, values = window.Read()
    if (button=='OK'):
        if not (os.path.exists(values['_FILEPATH_'])):
            sg.popup("File DOES NOT EXIST!")
        else:
            if not (os.access(values['_FILEPATH_'], os.R_OK)):
                sg.popup("File CANNOT be READ!")
            elif not (os.access(values['_FILEPATH_'], os.W_OK)):
                sg.popup("File CANNOT be WRITTEN!")
            else:

                sg.popup("File exists and is readable!")
                window.close()
                expensesinput.main(values)
    elif (button == 'Cancel'):
        break

window.close()
print(button, values['_NAME_'], values['_EMAIL_'], values['_FILEPATH_'])
