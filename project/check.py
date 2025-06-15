import sqlite3
from prettytable import PrettyTable

cnn = sqlite3.connect('vieDisasters.db')
db = cnn.cursor()
db.execute('SELECT "province", COUNT("index") AS "count" FROM "disasters" GROUP BY "province" ORDER BY "count"')
disaster_by_types = db.fetchall()
dbt_tb = PrettyTable(["Disaster", "count"])
for row in disaster_by_types:
    dbt_tb.add_row(row)

print(dbt_tb)