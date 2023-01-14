import graphviz
import os
import json
from json import load

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
print(os.system("dot -V"))

s = 'C:\\Users\\kiril\\OneDrive\\Рабочий стол\\Python\\Bot_test\\TelegramBotData'
os.chdir(s)
adjacency_list = json.load(open('adjacency_list.json', 'r'))
button_list = json.load(open('button.json', 'r'))
text_list = json.load(open('text.json', 'r'))

node = 18
g = graphviz.Digraph('round-table', comment='The Round Table', format='png')


for i, h in enumerate(adjacency_list):
    for j in h:

        g.edge(text_list[i], text_list[j], label=button_list[i][j])

g.view()