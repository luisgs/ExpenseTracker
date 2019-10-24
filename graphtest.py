import math
import sys
import logging
import PySimpleGUI as sg
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Dicts with expenses
# Exmple = {'21': 5900.0, '22': -700.0}
dailyExpense={'21': 5900.0, '22': -700.0, '20': 5000.0}


# Varibles about Income Outcome
maxIncome = max(dailyExpense.values())
minIncome = min(dailyExpense.values())
logging.debug(maxIncome)
logging.debug(minIncome)
# Canvas canvas_size
wide = 650  # x
tall = 400  # y

# Graph Starting Point
xZero = int(wide*-0.85)
xEnd = abs(xZero)
yZero = int(tall*(-0.8))
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

# Origin of line!
pointA_X=xZero
pointA_Y=0
for key in range(1,31):
    logging.debug(key)
    logging.debug(str(key))
    if str(key) in dailyExpense:
        logging.debug(dailyExpense[str(key)]*yEnd/maxIncome)
        xValue=(2*xEnd/32) * (key - 15)
        logging.debug(xValue)
        graph.DrawCircle((xValue, dailyExpense[str(key)]*yEnd/maxIncome), 3,
                            fill_color='black',
                            line_color='black')
        graph.DrawLine((pointA_X, pointA_Y),
                            (xValue, dailyExpense[str(key)]*yEnd/maxIncome))
        pointA_X = xValue
        pointA_Y = dailyExpense[str(key)]*yEnd/maxIncome

graph.DrawLine((pointA_X, pointA_Y), (xEnd, pointA_Y))



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
