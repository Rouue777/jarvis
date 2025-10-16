import sqlite3
import csv


con = sqlite3.connect('sexta-feira.db', check_same_thread=False)


cursor = con.cursor()




# Define the desired columns and their indices in the CSV
#desired_columns_indices = [0, 18]  # Indices for 'name' and 'mobile_no'

# # Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:

#    csvreader = csv.reader(csvfile)
#   for row in csvreader:
#        selected_data = []
#        for i in desired_columns_indices:
#            if i < len(row):
#                selected_data.append(row[i])
#            else:
#                selected_data.append("")  # Preenche com vazio se não existir
#        cursor.execute(
#            '''INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);''',
#            tuple(selected_data)
#        )

# # Commit changes and close connection
#con.commit()
#con.close()

#Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'lol', 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games\\League of Legends.lnk')"
#cursor.execute(query)
#con.commit()

#query = "INSERT INTO web_command VALUES (null,'instagram', 'https://www.instagram.com')"
#cursor.execute(query)
#con.commit()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

# testing module
#app_name = "lol"
#cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#results = cursor.fetchall()
#print(results[0][0])


query = 'breno'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])

#AIzaSyAkbk131y7_Uygf0e-tt2GyQVtgebYXLsc chave apigemini