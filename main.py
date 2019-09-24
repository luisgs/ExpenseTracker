import os.path
import PySimpleGUI as sg
import expensesinput

# Very basic window.  Return values as a list

layout = [
          [sg.Text('Please enter your information:')],
          [sg.Text('Name', size=(15, 1)), sg.InputText('name')],
          [sg.Text('Email', size=(15, 1)), sg.InputText('email@address.com')],
          [sg.Text('Password', size=(15, 1)), sg.InputText('Password', password_char='*')],
          [sg.Text('Expense File location:', size=(15, 1)), sg.InputText('C:\\Users\\gomezlui\\Downloads\\ExpenseReport.json')],
          [sg.OK(tooltip='Click to submit this window'), sg.Cancel()]
         ]

window = sg.Window('Welcome to Expense Tracker').Layout(layout)

while True:
    button, values = window.Read()
    if (button=='OK'):
        if not (os.path.exists(values[3])):
            sg.popup("File DOES NOT EXIST!")
        else:
            if not (os.access(values[3], os.R_OK)):
                sg.popup("File CANNOT be READ!")
            elif not (os.access(values[3], os.W_OK)):
                sg.popup("File CANNOT be WRITTEN!")
            else:
                sg.popup("File exists and is readable!")
                window.close()
                expensesinput.main(values)
    elif (button == 'Cancel'):
        break

window.close()
print(button, values[0], values[1], values[2])
