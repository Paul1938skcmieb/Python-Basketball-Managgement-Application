import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y, title, xlabel, ylabel):
    plt.switch_backend('AGG')
    plt.figure(figsize=(4,4))
    plt.title(title)
    plt.scatter(x, y)
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    for i, txt in enumerate(x):
        plt.annotate(txt, (x[i], y[i]))

    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot1(x,y):
    title = 'Players Field Goal %'
    xlabel = 'Players'
    ylabel = 'Field Goals Percentage'
    return get_plot(x, y, title, xlabel, ylabel)

def get_plot2(x,y):
    title = 'Players Points Per Game'
    xlabel = 'Players'
    ylabel = 'Points per game'
    return get_plot(x, y, title, xlabel, ylabel)

def get_plot3(x,y):
    title = 'Players Assists Per Game'
    xlabel = 'Players'
    ylabel = 'Assists Per Game'
    return get_plot(x, y, title, xlabel, ylabel)

def get_plot4(x,y):
    title = 'Three points percentage'
    xlabel = 'Players'
    ylabel = 'Three points %'
    return get_plot(x, y, title, xlabel, ylabel)

def get_plot5(x,y):
    title = 'Free throws percentage'
    xlabel = 'Players'
    ylabel = 'Free throws %'
    return get_plot(x, y, title, xlabel, ylabel)

def get_plot6(x,y):
    title = 'Rebounds Per Game'
    xlabel = 'Players'
    ylabel = 'Rebounds per game'
    return get_plot(x, y, title, xlabel, ylabel)
