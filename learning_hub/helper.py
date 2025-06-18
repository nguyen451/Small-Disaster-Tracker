import requests
import csv
from prettytable import PrettyTable
import tkinter as tk
from tkinter import ttk

def get_js(year: int):              #____________________________________test throw exceptions__________________________________
    """
        @param: int year
        Get json data from url with related year
    """
    url = f"http://vndms.dmptc.gov.vn/EventDisaster/TotalEvent?year={year}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    # else raise exception

def to_csv_js(disasters : dict, outfile : str) -> None:  #_____________________________________________FILE NOT FOUND_____________________________________________
    file = outfile
    with open(file, 'w') as csvfile:
        fieldname = ["name", "kv_anhhuong", "time_start", "lon", "lat", "level", "disaster_level", "type"]
        writer = csv.DictWriter(csvfile, fieldnames= fieldname)

        writer.writeheader()
        writer.writerows(disasters)


def make_and_print_table(rows : list, fields : list, title : str):
    # print to terminal
    tb = PrettyTable()
    tb.field_names = fields
    for row in rows:
        tb.add_row([row[i] for i in range(len(row))])
    
    print(tb)

    # print to gui
    # window
    window = tk.Tk()
    window.geometry('600x400')
    window.title(title)

    # treeview
    table = ttk.Treeview(window, columns= fields, show = 'headings')
    for col in fields:
        table.heading(col, text=col)
    table.pack(fill='both', expand=True)

    # insert data to table:
    for row in rows:
        table.insert(parent='', index=0, values=row)

    window.mainloop()



