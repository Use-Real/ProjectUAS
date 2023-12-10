from os import linesep
import plotly.express as px

def plotBar(data, x, y):
    return px.bar(data_frame=data, x = x, y = y)
    
def plotLine(data, x, y):
    return px.line(data_frame=data, x = x, y = y)

def plotPie(data, labels):
    return px.pie(data_frame=data, labels=labels)   