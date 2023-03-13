import json
import pypyodbc

# 
conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=.\access\db.accdb;")
cur = conn.cursor()

with open("json/db.json", encoding="utf-8") as filename:
    db = json.load(filename)

for i in range(len(db["objects"])):
    cur.execute(db["objects"][i]["ddl"])

    columns = []
    for a in range(len(db["objects"][i]["columns"])):
        columns.append(db["objects"][i]["columns"][a]["name"])

    for j in range(len(db["objects"][i]["rows"])):
        stroka = ""
        for x in range(len(db['objects'][i]['rows'][j])):
            if isinstance(db['objects'][i]['rows'][j][x], str):
                stroka += f"'{db['objects'][i]['rows'][j][x]}', "
            else:
                stroka += f"{db['objects'][i]['rows'][j][x]}, "
        cur.execute(f"INSERT INTO \"{db['objects'][i]['name']}\" ({', '.join(columns)})  VALUES  ({stroka[:-2]})")

cur.commit()
cur.close()
conn.close()