import math
import PySimpleGUI as sg

# Dicts with expenses
# Exmple = {'21': 5900.0, '22': -700.0}
dailyExpense={'21': 5900.0, '22': -700.0}


# Varibles about Income Outcome
maxIncome = max(dailyExpense, key=dailyExpense.get)
minIncome = min(dailyExpense, key=dailyExpense.get)

# Canvas canvas_size
wide = 650  # x
tall = 400  # y

# Graph Starting Point
xZero = -560
xEnd = abs(xZero)
yZero = -325
yEnd = abs(yZero)

layout = [[sg.Graph(canvas_size=(wide, tall),
                        graph_bottom_left=(-wide, -tall),
                        graph_top_right=(wide, tall),
                        background_color='white', key='graph',
                        tooltip='This is a cool graph!')],]

window = sg.Window('Graph of Sine Function', layout, grab_anywhere=True).Finalize()
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
    graph.DrawText(y, (xZero-20,y), color='green')

# HOrizontal line for Expense price
graph.DrawLine((xZero, 0), (xEnd, 0))
for x in range(xZero, xEnd, 35):
    graph.DrawLine((x,-5), (x,+5))


for key in range(1,31):
    if key in dailyExpense:
        graph.DrawCircle((75, dailyExpense[key]), 25,
                            fill_color='black',
                            line_color='white')

"""
DEBUG:root:{'21': 5900.0, '22': -700.0}

# Draw axis
graph.DrawLine((-100,0), (100,0))
graph.DrawLine((0,-100), (0,100))

for x in range(-100, 101, 20):
    graph.DrawLine((x,-3), (x,3))
    if x != 0:
        graph.DrawText( x, (x,-10), color='green')

for y in range(-100, 101, 20):
    graph.DrawLine((-3,y), (3,y))
    if y != 0:
        graph.DrawText( y, (-10,y), color='blue')

# Draw Graph
for x in range(-100,100):
    y = math.sin(x/20)*50
    graph.DrawCircle((x,y), 1, line_color='red', fill_color='red')
"""
event, values = window.Read()
