import tkinter as tk
from tkinter import ttk
import random

"""
    Tutorial link: https://youtu.be/jRpHmF-iuMI?si=Hp1kHA4heDFhb1CK
"""

# window
window = tk.Tk()
window.geometry('600x400')
window.title('Treeview')

# data
first_names = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Lisa', 'Anna', 'Lisa']
last_names = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']

# treeview
table = ttk.Treeview(window, columns=('first', 'last', 'email'), show='headings')
table.heading('first', text='First name')
table.heading('last', text='Surname')
table.heading('email', text='Email')
table.pack(fill='both', expand=True)

# insert values into a table
for i in range(100):
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f'{first[0]}{last}@email.com'
    data = (first, last, email)
    table.insert(parent='', index=0,values=data) 
    # index = 0 means insert new data to position 0, you can specify index = 1, 2, ... means insert in to position index 1, 2 ,..

# events
def item_select(_):
    print(table.selection())
    for i in table.selection():
        print(table.item(i)['values'])
    # table.item(table.selection())

def delete_items(_):
    print('delete')
    for i in table.selection():
        table.delete(i)

table.bind('<<TreeviewSelect>>', item_select)
table.bind('<Delete>', delete_items)


# run
window.mainloop()
